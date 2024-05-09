import librosa
import librosa.display
from tensorflow.keras.models import load_model
import numpy as np
def add_noise(data,x):
    noise = np.random.randn(len(data))
    data_noise = data + x * noise
    return data_noise

def shift(data,x):
    return np.roll(data, x)

def stretch(data, r):
    data = librosa.effects.time_stretch(data, rate=r)
    return data

def gru_diagnosis_prediction(test_audio):
    model_path= "C:/Users/abujo/DjangoRDD/savedmodels/_GRU_CNN_2.h5"
    loaded_model = load_model(model_path)
    classes = ["COPD" ,"Bronchiolitis ", "Pneumonia", "URTI", "Healthy"]
    data_x, sampling_rate = librosa.load(test_audio)
    data_x = stretch (data_x,1.2)

    features = np.mean(librosa.feature.mfcc(y=data_x, sr=sampling_rate, n_mfcc=64).T,axis = 0)

    features = features.reshape(1,64)

    test_pred = loaded_model.predict(np.expand_dims(features, axis = 1))
    classpreds = classes[np.argmax(test_pred[0], axis=1)[0]]
    confidence = test_pred.T[test_pred[0].mean(axis=0).argmax()].mean()

    return classpreds , confidence