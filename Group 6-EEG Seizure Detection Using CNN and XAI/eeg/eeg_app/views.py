from django.shortcuts import render
from django.core import serializers
from .models import *
from django.db.models import Count
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.db.models import Count
from django.views.decorators.cache import never_cache
from django.core.files.storage import FileSystemStorage
import os
from datetime import date
from datetime import datetime
import re
from datetime import datetime,timedelta
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
import warnings
warnings.filterwarnings("ignore")
# Create your views here.

value=0
get_channel_labels = ['FP1-F7', 'F7-T7', 'T7-P7', 'P7-O1', 'FP1-F3', 'F3-C3', 'C3-P3','P3-O1',
             'FP2-F4', 'F4-C4', 'C4-P4', 'P4-O2', 'FP2-F8', 'F8-T8', 'T8-P8', 'P8-O2',
             'FZ-CZ', 'CZ-PZ']


build_cnn_model = tf.keras.models.load_model('Model/CNN_model.h5')


def get_tips():
	recommended_tips=['Stay Calm','Ensure Safety']

	suggested_tip = random.choice(recommended_tips)
	return suggested_tip



@never_cache
def display_login(request):
	return render(request, "login.html", {})

@never_cache
def check_login(request):
	username = request.POST.get("name")
	password = request.POST.get("pass")

	if username == "admin" and password == "admin":
		request.session['uid'] = "admin"
		return HttpResponse("<script>alert('Login Successful');window.location.href='/show_home_user/';</script>")
	else:
		return HttpResponse("<script>alert('Invalid');window.location.href='/display_login/';</script>")
##########################################################################################
#Admin

@never_cache
def logout(request):
	if 'uid' in request.session:
		del request.session['uid']
	return render(request, 'login.html')


#Boat
@never_cache
def show_home_user(request):
	if 'uid' in request.session:
		return render(request, 'home_user.html')
	else:
		return render(request, 'login.html')


def get_influence_factors():
	factors=['Sleep Deprivation: Lack of sleep can lower seizure threshold.',
'Stress and Anxiety: Emotional stress or anxiety can trigger seizures in some individuals.',
'Alcohol and Substance Use: Certain substances like alcohol or drugs can provoke seizures.',
'Medication Non-Adherence: Skipping or irregularly taking prescribed medications can increase seizure risk.',
'Flashing Lights: For individuals with photosensitive epilepsy, exposure to certain light patterns can trigger seizures.',
'Illness or Infection: Fever or other illnesses can lower seizure threshold.',
'Environmental Factors: Certain environmental triggers like loud noises or extreme temperatures may precipitate seizures in susceptible individuals.'
'Specific Activities: Certain activities like playing video games or watching TV for extended periods may trigger seizures in some people.']

	random_factors = random.sample(factors, 3)
	###print(random_factors)

	return random_factors

@never_cache
def display_upload_data(request):
	if 'uid' in request.session:
		return render(request, 'upload_data.html')
	else:
		return render(request, 'login.html')

@never_cache
def display_result(request):
	if 'uid' in request.session:
		if value==0:
	
			images_dir ='eeg_app/static/Results/'# os.path.join(settings.STATIC_ROOT, 'Results')

			# Get a list of all filenames in the directory
			image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]

			# Pass the list of image filenames to the template context
			return render(request, 'results_no.html', {'image_files': image_files})
		else:
			images_dir ='eeg_app/static/Results/'# os.path.join(settings.STATIC_ROOT, 'Results')

			# Get a list of all filenames in the directory
			image_files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f))]


			seizure_influence=get_influence_factors()
			tips=get_tips()

			# Pass the list of image filenames to the template context
			return render(request, 'results.html', {'image_files': image_files,'factors':seizure_influence,'tips':tips})
	else:
		return render(request, 'login.html')



def sampling_data_pred(f, verbose=True):
    list_signals = []
    list_is_sz = []
    #n_sample = 40
    if verbose==True:
        print('{}: Reading. '.format(f))
    temp_edf =  mne.io.read_raw_edf(f)
    temp_labels = temp_edf.ch_names
    if sum([any([0 if re.match(c, l)==None else 1 for l in temp_edf.ch_names]) for c in get_channel_labels])==len(get_channel_labels):
        ch_mapping = {sorted([l for l in temp_edf.ch_names if re.match(c, l)!=None ])[0]:c for c in get_channel_labels}
        temp_edf.rename_channels(ch_mapping)
        #temp_edf = temp_edf.pick(get_channel_labels)

        temp_is_sz = np.zeros((temp_edf.n_times,))
        temp_signals = temp_edf.get_data(picks=get_channel_labels)*1e6

        if os.path.exists(f+'.seizures'):
            if verbose==True:
                print('sz exists.', end=' ')
            temp_annotation = wfdb.rdann(f, 'seizures')
            for i in range(int(temp_annotation.sample.size/2)):
                temp_is_sz[temp_annotation.sample[i*2]:temp_annotation.sample[i*2+1]]=1
        #else:
            #print('No sz.', end=' ')

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


def moving_ave(a, n):
    if len(a.shape)!=1:
        print('Not 1 dimension array. return nothing.')
        return
    temp = np.zeros(a.size-n)
    for i in range(n):
        temp = temp+a[i:-n+i]
    temp = temp/n
    
    return temp



@never_cache
def upload_file(request):

	global value
	value=0
	directory = 'eeg_app/static/Results/'

	# Loop through all files in the directory and delete them
	for filename1 in os.listdir(directory):
		file_path1 = os.path.join(directory, filename1)
		try:
			os.remove(file_path1)
		except Exception as e:
			print(f"Failed to delete: {file_path1} - {e}")

	directory1 = 'eeg_app/static/Test_EEG/'

	# Loop through all files in the directory and delete them
	for filename2 in os.listdir(directory1):
		file_path2 = os.path.join(directory1, filename2)
		try:
			os.remove(file_path2)
		except Exception as e:
			print(f"Failed to delete: {file_path2} - {e}")

	file1 = request.FILES["upl"]
	file_name=file1.name
	print("file_name : ",file_name)

	fs = FileSystemStorage("eeg_app/static/Test_EEG/")
	fs.save(file_name, file1)

		
	# files_test=['Test/chb10_20.edf']
	get_file_path="eeg_app/static/Test_EEG/"+file_name
	# get signals and labels from test data.
	n=0 #100
	array_signals, array_is_sz = sampling_data_pred(get_file_path)#files_test[n]

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
	plt.savefig("eeg_app/static/Results/output.png.")
	plt.close(fig)
	## plt.show()




	if pred_peaks.size==0:
		print('\nNo seizure detected.')
	else:

		#f = files_test[n]
		f=get_file_path
		temp_edf =  mne.io.read_raw_edf(f)
		temp_labels = temp_edf.ch_names
		if sum([any([0 if re.match(c, l)==None else 1 for l in temp_edf.ch_names]) for c in get_channel_labels])==len(get_channel_labels):
			ch_mapping = {sorted([l for l in temp_edf.ch_names if re.match(c, l)!=None ])[0]:c for c in get_channel_labels}
			temp_edf.rename_channels(ch_mapping)
			#temp_edf = temp_edf.pick(get_channel_labels)

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
			filename = f"plot_{n_peak + 1}.png"  # Unique name for each plot
			filepath = os.path.join("eeg_app/static/Results/", filename)  # Provide the path to save the plots
			plt.savefig(filepath)

			plt.close(fig)
			## plt.show()

		temp_edf.close()
		value=1
		print('\nSeizure detected.')
	

	
	return HttpResponse("<script>alert('EEG Seizure Prediction Successful');window.location.href='/display_result/'</script>")



###################################################################################################################
###################################################################################################################


