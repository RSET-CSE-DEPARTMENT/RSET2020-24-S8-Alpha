import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import glob
import random
import gc
from scipy.signal import find_peaks
import re
import mne
import wfdb
import tqdm
import logging
from sklearn import model_selection
import tensorflow as tf
from sklearn.decomposition import PCA
from tensorflow.keras.models import Model
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
# import warnings
# warnings.filterwarnings("ignore")


#Load Data and Labels
array_signals=np.load('Data/signal_samples.npy')
array_is_sz=np.load('Data/is_sz.npy')

print("******************")
print(array_signals)
print(array_is_sz)
print("******************")
print(array_signals.shape)
print(array_is_sz.shape)
print("******************")
print(type(array_signals))
print(type(array_is_sz))


## preprocess
#### Signals frequencies are originally 256 Hz, but resampled to 128 Hz for simplification of the data.
array_signals = array_signals[:, :, ::2]

# show a sample of extracted signals (the last one)
vertical_width = 250
signals = array_signals[-1, :, :]
fs = 128

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.callbacks import ReduceLROnPlateau, EarlyStopping

def CNN_model(X_train):
    model = keras.models.Sequential()

    model.add(layers.Conv2D(filters=64, kernel_size=(2, 4), padding='same', activation='relu', input_shape=X_train.shape[1:]))
    model.add(layers.Conv2D(filters=64, kernel_size=(2, 4), strides=(1, 2),padding='same', activation='relu'))
    model.add(layers.MaxPooling2D((1, 2)))

    model.add(layers.Conv2D(filters=128, kernel_size=(2, 4), padding='same', activation='relu'))
    model.add(layers.Conv2D(filters=128, kernel_size=(2, 4), strides=(1, 2), padding='same', activation='relu'))
    model.add(layers.MaxPooling2D((2, 2)))

    model.add(layers.Conv2D(filters=256, kernel_size=(4, 4), padding='same', activation='relu'))
    model.add(layers.Conv2D(filters=256, kernel_size=(4, 4), strides=(1, 2), padding='same', activation='relu'))
    model.add(layers.MaxPooling2D((1, 2)))

    model.add(layers.GlobalAveragePooling2D())
    #model.add(layers.Flatten())
    model.add(layers.Dense(256, activation='relu'))
    model.add(layers.Dropout(0.25))
    model.add(layers.Dense(128, activation='relu'))
    model.add(layers.Dense(64, activation='relu'))
    model.add(layers.Dropout(0.25))
    model.add(layers.Dense(1, activation='sigmoid'))

    return model

# Checking Extracted signals and how much of signals have seizure inside.
array_n = np.where(array_is_sz>.0)[0]
print("\n Information")
print('Number of all the extracted signals: {}'.format(array_is_sz.size))
print('Number of signals with seizures: {}'.format(array_n.size))
print('Ratio of signals with seizures: {:.3f}'.format(array_n.size/array_is_sz.size))


# CNN will be used. Channel dimension is added.
array_signals = array_signals[:, :, :, np.newaxis]

print(array_signals.shape)

# splitting training data into training & validation data.
X_train, X_val, y_train, y_val = model_selection.train_test_split(
    array_signals, array_is_sz, test_size=0.2,
    stratify=(array_is_sz>0))

del array_signals, array_is_sz

print("\nTraining Set")
print(X_train.shape)
print(y_train.shape)
print("\nTesting Set")
print(X_val.shape)
print(y_val.shape)


# build_cnn_model=CNN_model(X_train)

# print(build_cnn_model.summary())


# LEARNING_RATE = 1e-4
# OPTIMIZER = tf.keras.optimizers.Adam(learning_rate=LEARNING_RATE)

# build_cnn_model.compile(optimizer=OPTIMIZER, loss='binary_crossentropy', metrics=['accuracy'])

# hist = build_cnn_model.fit(
#     x=X_train, y=y_train,
#     validation_data=(X_val, y_val),
#     epochs=1,
#     batch_size=32
# )


#######build_cnn_model.save('Model/CNN_model.h5')


build_cnn_model = tf.keras.models.load_model('Model/CNN_model.h5')


# Get the weights of the CNN layers
layer_weights = build_cnn_model.get_weights()

# Assuming you are interested in the weights of the first Conv2D layer
conv1_weights = layer_weights[0]

# # Visualize the importance of features using the weights
# plt.figure(figsize=(10, 6))
# plt.imshow(conv1_weights[:, :, 0, 0], cmap='viridis', aspect='auto')
# plt.colorbar()
# plt.title('Importance of Features in First Conv2D Layer')
# plt.xlabel('Feature Index')
# plt.ylabel('Filter Index')
# plt.show()

# Choose a sample image from your dataset for visualization
sample_image = X_val[1]  # Adjust this according to your dataset

# Define a function to generate Grad-CAM heatmap
def generate_grad_cam(model, img_array, layer_name):
    grad_model = Model(
        [model.inputs], 
        [model.get_layer(layer_name).output, model.output]
    )
    with tf.GradientTape() as tape:
        conv_output, predictions = grad_model(img_array)
        class_index = tf.argmax(predictions[0])
        loss = predictions[:, class_index]

    output = conv_output[0]
    grads = tape.gradient(loss, conv_output)[0]

    gate_f = tf.cast(output > 0, 'float32')
    gate_r = tf.cast(grads > 0, 'float32')
    guided_grads = gate_f * gate_r * grads

    weights = tf.reduce_mean(guided_grads, axis=(0, 1))
    cam = np.dot(output, weights)

    cam = np.maximum(cam, 0)
    cam /= np.max(cam)

    return cam

# Generate Grad-CAM heatmap
cam = generate_grad_cam(build_cnn_model, np.expand_dims(sample_image, axis=0), 'conv2d')  # Adjust the layer name as per your model

# Resize the heatmap to match the dimensions of the input image
heatmap = tf.image.resize(np.expand_dims(cam, axis=-1), (sample_image.shape[0], sample_image.shape[1]))


# Define the height ratios for the subplots
height_ratios = [1, 2]  # Ratio of heights for the two subplots

# Create subplots with specified height ratios
fig, axs = plt.subplots(2, 1, figsize=(14, 14), gridspec_kw={'height_ratios': height_ratios})

axs[0].imshow(sample_image[:,:,0], cmap='gray')
axs[0].set_title('Original Image')
axs[0].axis('off')

axs[1].imshow(sample_image[:,:,0], cmap='gray')
axs[1].imshow(heatmap[:,:,0], cmap='jet', alpha=0.5)
axs[1].set_title('Grad-CAM')
axs[1].axis('off')

plt.tight_layout()  # Adjust the layout to prevent overlapping
plt.show()








######################################################################################################
# Plot the original image with Grad-CAM heatmap overlay
# plt.figure(figsize=(14, 7))
# plt.subplot(1, 2, 1)
# plt.imshow(sample_image[:,:,0], cmap='gray')
# plt.title('Original Image')
# plt.axis('off')
# plt.subplot(1, 2, 2)
# plt.imshow(sample_image[:,:,0], cmap='gray')
# plt.imshow(heatmap[:,:,0], cmap='jet', alpha=0.5)
# plt.title('Grad-CAM')
# plt.axis('off')
# plt.show()


# plt.figure(figsize=(20, 10))  # Increase the figure size

# plt.subplot(1, 2, 1)
# plt.imshow(sample_image[:,:,0], cmap='gray')
# plt.title('Original Image')
# plt.axis('off')

# plt.subplot(1, 2, 2)
# plt.imshow(sample_image[:,:,0], cmap='gray')
# plt.imshow(heatmap[:,:,0], cmap='jet', alpha=0.5)
# plt.title('Grad-CAM')
# plt.axis('off')

# plt.tight_layout()  # Adjust the layout to prevent overlapping
# plt.show()
