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
# import warnings
# warnings.filterwarnings("ignore")

from model import *



get_channel_labels = ['FP1-F7', 'F7-T7', 'T7-P7', 'P7-O1', 'FP1-F3', 'F3-C3', 'C3-P3','P3-O1',
             'FP2-F4', 'F4-C4', 'C4-P4', 'P4-O2', 'FP2-F8', 'F8-T8', 'T8-P8', 'P8-O2',
             'FZ-CZ', 'CZ-PZ']



build_cnn_model = tf.keras.models.load_model('Model/CNN_model1.h5')



###############################################################
files_test=['Test/chb08_13.edf']

def sampling_data_pred(f, verbose=True):
    list_signals = []
    list_is_sz = []
    n_sample = 40
    if verbose==True:
        print('{}: Reading. '.format(f))
    temp_edf =  mne.io.read_raw_edf(f)
    temp_labels = temp_edf.ch_names
    if sum([any([0 if re.match(c, l)==None else 1 for l in temp_edf.ch_names]) for c in get_channel_labels])==len(get_channel_labels):
        ch_mapping = {sorted([l for l in temp_edf.ch_names if re.match(c, l)!=None ])[0]:c for c in get_channel_labels}
        temp_edf.rename_channels(ch_mapping)
        temp_edf = temp_edf.pick(get_channel_labels)

        temp_is_sz = np.zeros((temp_edf.n_times,))
        temp_signals = temp_edf.get_data(picks=get_channel_labels)*1e6

        if os.path.exists(f+'.seizures'):
            if verbose==True:
                print('sz exists.', end=' ')
            temp_annotation = wfdb.rdann(f, 'seizures')
            for i in range(int(temp_annotation.sample.size/2)):
                temp_is_sz[temp_annotation.sample[i*2]:temp_annotation.sample[i*2+1]]=1
        else:
            print('No sz.', end=' ')

        temp_len = temp_edf.n_times

        time_window = 8
        time_step = 4
        fs = int(1/(temp_edf.times[1]-temp_edf.times[0]))
        step_window = time_window*fs
        step = time_step*fs

         # sampling all signals
        temp_array_signals = np.array([temp_signals[:, i*step:i*step+step_window] for i in range((temp_len-step_window)//step)])
        temp_is_sz_ind = np.array([temp_is_sz[i*step:i*step+step_window].sum()/step_window for i in range((temp_len-step_window)//step)])
    else:
        if verbose==True:
            print('EEG {}: Not appropriate channel labels. Reading skipped.'.format(n))

    return temp_array_signals, temp_is_sz_ind



for i, f in enumerate(files_test):
    if os.path.exists(f+'.seizures'):
        print('Index = {} has seizures: {}'.format(i, f))


def moving_ave(a, n):
    if len(a.shape)!=1:
        print('Not 1 dimension array. return nothing.')
        return
    temp = np.zeros(a.size-n)
    for i in range(n):
        temp = temp+a[i:-n+i]
    temp = temp/n
    
    return temp

 # get signals and labels from test data.
n=0 #100
array_signals, array_is_sz = sampling_data_pred(files_test[n])

 # preprocess
array_signals=array_signals[:, :, ::2, np.newaxis]

 # use deep learning model
pred = build_cnn_model.predict(array_signals)


time_window = 8
time_step = 4
mv_win = 3

fig, ax = plt.subplots(figsize=(12, 2))

ax.plot(np.arange(pred.size)*time_step, pred.flatten(), alpha=0.7, label='deep learning model pred')
ax.plot(np.arange(pred.size)*time_step, array_is_sz, alpha=.7, label='True label')

pred_moving_ave = moving_ave(pred.flatten(), mv_win)
pred_peaks, _ = find_peaks(pred_moving_ave, height=.95, distance=6)
ax.plot(np.arange(pred.size-mv_win)*time_step, pred_moving_ave,
        alpha=.9, label='pred - moving ave', color='tab:pink', zorder=0)
ax.scatter(pred_peaks*time_step, pred_moving_ave[pred_peaks], s=20, color='tab:red')

ax.set_xlabel('time (s)')
ax.set_ylabel('p')
ax.set_xlim(0, pred.size*time_step+500)
ax.legend(loc='upper right')
plt.show()




if pred_peaks.size==0:
    print('No seizure detected.')
else:
    f = files_test[n]
    temp_edf =  mne.io.read_raw_edf(f)
    temp_labels = temp_edf.ch_names
    if sum([any([0 if re.match(c, l)==None else 1 for l in temp_edf.ch_names]) for c in get_channel_labels])==len(get_channel_labels):
        ch_mapping = {sorted([l for l in temp_edf.ch_names if re.match(c, l)!=None ])[0]:c for c in get_channel_labels}
        temp_edf.rename_channels(ch_mapping)
        temp_edf = temp_edf.pick(get_channel_labels)

        temp_is_sz = np.zeros((temp_edf.n_times,))
        temp_signals = temp_edf.get_data(picks=get_channel_labels)*1e6

    fs = int(1/(temp_edf.times[1]-temp_edf.times[0]))
    for n_peak in range(pred_peaks.size):
        ind_peak = pred_peaks[n_peak]*time_step*fs
        backward_steps = 30*fs
        forward_steps = 15*fs
        vertical_width=500

        fig, ax = plt.subplots(figsize=(10, 6))
        for i in range(temp_signals.shape[0]):
            ax.plot(np.arange(ind_peak-backward_steps, ind_peak+forward_steps)/fs,
                    temp_signals[i, ind_peak-backward_steps:ind_peak+forward_steps]+i*vertical_width, linewidth=0.5, color='tab:blue')
            ax.annotate(get_channel_labels[i], xy=((ind_peak-backward_steps)/fs, i*vertical_width))
        ax.axvline(x=ind_peak/fs, color='tab:red', alpha=0.5, label='Seizure detection point')
        ax.invert_yaxis()
        ax.legend(loc='upper right')
        plt.show()
    ax.set_xlim(0, 8)
    # Convert peak indices to time values
    peak_times = pred_peaks * time_step

    # Define duration before and after each peak (in seconds)
    backward_duration = 30
    forward_duration = 15

    # Convert duration to samples
    backward_samples = backward_duration * fs
    forward_samples = forward_duration * fs

    # Iterate over each peak to find start and end points
    for peak_time in peak_times:
        # Convert peak time to sample index
        peak_index = int(peak_time * fs)

        # Calculate start and end points
        start_index = peak_index - backward_samples
        end_index = peak_index + forward_samples

        # Convert start and end points to time values
        start_time = start_index / fs
        end_time = end_index / fs

        # Print start and end times
        print("Seizure Event:")
        print("Start Time:", start_time, "seconds")
        print("End Time:", end_time, "seconds")
        print()
   

    temp_edf.close()
# ##############################################################################################