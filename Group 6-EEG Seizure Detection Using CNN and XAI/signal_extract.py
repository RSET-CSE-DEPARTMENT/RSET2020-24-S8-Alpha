#Necessary Libraries
import numpy as np
import os
import wfdb
import glob
import random
import gc
import mne
import re
import tqdm
import logging


#########Data Conversion
#Defines a list of EEG channel labels.
get_channel_labels = ['FP1-F7', 'F7-T7', 'T7-P7', 'P7-O1', 'FP1-F3', 'F3-C3', 'C3-P3','P3-O1',
             'FP2-F4', 'F4-C4', 'C4-P4', 'P4-O2', 'FP2-F8', 'F8-T8', 'T8-P8', 'P8-O2',
             'FZ-CZ', 'CZ-PZ']

#Prints the EEG channel labels and their data type.
print(get_channel_labels)
print(type(get_channel_labels))

#Finds the patients' IDs from folder names and prints them.
raw_data = 'Data/chb-mit-scalp-eeg-database-1.0.0'

folders = sorted(glob.glob(raw_data+'/*/'))
get_patient_count = [m[-2:] for m in [l.rsplit('/', 2)[-2] for l in folders]]
print("\n")
print(*get_patient_count)


#Randomly divides patients into training and test sets and prints them.
random.seed(2023)

train_ratio = 0.8
train_patient_str = sorted(random.sample(get_patient_count, round(train_ratio*len(get_patient_count))))
test_patient_str = sorted([l for l in get_patient_count if l not in train_patient_str])
print('Train Data: ', *train_patient_str)
print('Test Data: ', *test_patient_str)


#Collects file names for training and test data.
train_files = []
for l in train_patient_str:
    train_files = train_files + glob.glob(raw_data+'/chb{}/*.edf'.format(l))

test_files = []
for l in test_patient_str:
    test_files = test_files + glob.glob(raw_data+'/chb{}/*.edf'.format(l))


###### Signal Extraction for training data
'''Each 8 second signals of 18 channels are extracted, sliding forward by 4 seconds.  
Each set of signals are labeled with the ratio of seizure in the time window. 
i.e. a set of signals are labeled 1.0 if it is in the middle of seizure. ''' 

#Sets logging parameters and creates a logger.
mne.set_log_level(verbose='ERROR')

logger = logging.getLogger(__name__)
fh = logging.FileHandler('read_files.log')
logger.addHandler(fh)

#Defines time window and step size for signal extraction.
time_window = 8
time_step = 4

#Checks if preprocessed data exists, if not, preprocesses the data.
if os.path.exists('Data/signal_samples.npy')&os.path.exists('Data/is_sz.npy'):
    array_signals=np.load('Data/signal_samples.npy')
    array_is_sz=np.load('Data/is_sz.npy')
else:
    #Signal Processing (if not loaded)
    #Iterates through the training files and checks if channel labels match the predefined ones.
    p = 0.01  
    counter = 0
    for temp_f in train_files:
        temp_edf =  mne.io.read_raw_edf(temp_f)
        temp_labels = temp_edf.ch_names
        if sum([any([0 if re.match(c, l)==None else 1 for l in temp_edf.ch_names]) for c in get_channel_labels])==len(get_channel_labels):
            
            #Sets time-related parameters for signal processing.
            time_window = 8
            time_step = 4
            fs = int(1/(temp_edf.times[1]-temp_edf.times[0]))
            step_window = time_window*fs
            step = time_step*fs
            
            #Creates an array for seizure annotations and extracts the length of the signal.
            temp_is_sz = np.zeros((temp_edf.n_times,))
            if os.path.exists(temp_f+'.seizures'):
                temp_annotation = wfdb.rdann(temp_f, 'seizures')
                for i in range(int(temp_annotation.sample.size/2)):
                    temp_is_sz[temp_annotation.sample[i*2]:temp_annotation.sample[i*2+1]]=1
            temp_len = temp_edf.n_times
            
            #Calculates the ratio of seizure in each time window.
            temp_is_sz_ind = np.array(
                [temp_is_sz[i*step:i*step+step_window].sum()/step_window for i in range((temp_len-step_window)//step)]
            )

            #Calculates the number of samples for each class (seizure and non-seizure).
            temp_0_sample_size = round(p*np.where(temp_is_sz_ind==0)[0].size)
            temp_1_sample_size = np.where(temp_is_sz_ind>0)[0].size

            #Updates the counter with the total number of samples.
            counter = counter + temp_0_sample_size + temp_1_sample_size
        temp_edf.close()

    #Initializes arrays to store signals and labels.
    array_signals = np.zeros((counter, len(get_channel_labels), step_window), dtype=np.float32)
    array_is_sz = np.zeros(counter, dtype=bool)

    #Resets the counter.
    counter = 0

    #Iterates through the training files with a progress bar.
    for n, temp_f in enumerate(tqdm.tqdm(train_files)):

        #Logs the progress and reads the EDF file.
        to_log = 'No. {}: Reading. '.format(n)
        temp_edf =  mne.io.read_raw_edf(temp_f)
        temp_labels = temp_edf.ch_names

        #Checks if channel labels match the predefined ones.
        n_label_match = sum([any([0 if re.match(c, l)==None else 1 for l in temp_edf.ch_names]) for c in get_channel_labels])
        if n_label_match==len(get_channel_labels):

            #Maps channel labels to the predefined ones.
            ch_mapping = {sorted([l for l in temp_edf.ch_names if re.match(c, l)!=None ])[0]:c for c in get_channel_labels}
            temp_edf.rename_channels(ch_mapping)
            #temp_edf = temp_edf.pick(get_channel_labels)

            #Initializes an array for seizure annotations and extracts signals.
            temp_is_sz = np.zeros((temp_edf.n_times,))
            temp_signals = temp_edf.get_data(picks=get_channel_labels)*1e6

            #Checks if seizure annotations exist.
            if os.path.exists(temp_f+'.seizures'):
                to_log = to_log+'sz exists.'
                temp_annotation = wfdb.rdann(temp_f, 'seizures')
                for i in range(int(temp_annotation.sample.size/2)):
                    temp_is_sz[temp_annotation.sample[i*2]:temp_annotation.sample[i*2+1]]=1
            else:
                to_log = to_log+'No sz.'

            #Calculates the ratio of seizure in each time window and deletes the seizure array.
            temp_len = temp_edf.n_times

            time_window = 8
            time_step = 4
            fs = int(1/(temp_edf.times[1]-temp_edf.times[0]))
            step_window = time_window*fs
            step = time_step*fs

            temp_is_sz_ind = np.array(
                [temp_is_sz[i*step:i*step+step_window].sum()/step_window for i in range((temp_len-step_window)//step)]
            )
            del temp_is_sz


            #Calculates the number of samples for each class (seizure and non-seizure).
            temp_0_sample_size = round(p*np.where(temp_is_sz_ind==0)[0].size)
            temp_1_sample_size = np.where(temp_is_sz_ind>0)[0].size


            #Stores seizure samples in the signal array and updates the counter.
            # sz data
            temp_ind = list(np.where(temp_is_sz_ind>0)[0])
            for i in temp_ind:
                array_signals[counter, :, :] = temp_signals[:, i*step:i*step+step_window]
                array_is_sz[counter] = True
                counter = counter+1

            #Stores non-seizure samples in the signal array and updates the counter.
            # no sz data
            temp_ind = random.sample(list(np.where(temp_is_sz_ind==0)[0]), temp_0_sample_size)
            for i in temp_ind:
                array_signals[counter, :, :] = temp_signals[:, i*step:i*step+step_window]
                array_is_sz[counter] = False
                counter = counter+1

            #Logs the number of signals added.
            to_log += '{} signals added: {} w/o sz, {} w/ sz.'.format(
                temp_0_sample_size+temp_1_sample_size, temp_0_sample_size, temp_1_sample_size
            )

        else:
            #Logs if channel labels are not appropriate.
            to_log += 'Not appropriate channel labels. Reading skipped.'.format(n)
        
        #Logs the progress and closes the EDF file.
        logger.info(to_log)
        temp_edf.close()

        #Performs garbage collection.
        if n%10==0:
            gc.collect()
    gc.collect()
    
    #Saves the preprocessed data.
    np.save('signal_samples', array_signals)
    np.save('is_sz', array_is_sz)