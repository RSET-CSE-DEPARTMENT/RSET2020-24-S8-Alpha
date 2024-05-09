import sys
import os
import mne
import numpy as np
import pandas as pd
from scipy import signal

# Function to calculate PSD for a given file
def calculate_psd(file_path):
    # Load the EEG data
    raw = mne.io.read_raw_edf(file_path, preload=True)
    # Extract EEG data and sampling frequency
    eeg_data, sfreq = raw.get_data(), raw.info['sfreq']
    
    # Take only the first 60 seconds of data
    eeg_data = eeg_data[:, :int(60 * sfreq)]
    
    # Remove Channel 21
    eeg_data = np.delete(eeg_data, 20, axis=0)
    
    # Get the names of the channels (electrodes)
    channel_names = raw.ch_names[:20]
    
    # Calculate PSD for each electrode within the frequency range of 0 to 15 Hz
    psd_data = {}
    for i, channel in enumerate(channel_names):
        f, S = signal.welch(eeg_data[i], fs=sfreq, nperseg=4096)
        f_idx = np.where((f >= 0) & (f <= 30))[0]  # Filter frequencies from 0 to 30 Hz
        psd_data[channel] = S[f_idx]*10e12
    
    return psd_data

# Function to calculate peak value within a frequency band
def calculate_peak_value(data, band):
    if band == 'Delta':
        freq_range = (0, 4)
    elif band == 'Theta':
        freq_range = (4, 8)
    elif band == 'Alpha':
        freq_range = (8, 12)
    elif band == 'Beta':
        freq_range = (12, 30)
    else:
        raise ValueError("Invalid frequency band")
    
    peak_values = {}
    for electrode, psd_values in data.items():
        f = np.linspace(0, 30, len(psd_values))
        band_indices = np.where((f >= freq_range[0]) & (f < freq_range[1]))[0]
        peak_values[electrode] = np.max(psd_values[band_indices])
    
    return peak_values

# Function to calculate mean value within a frequency band
def calculate_mean_value(data, band):
    if band == 'Delta':
        freq_range = (0, 4)
    elif band == 'Theta':
        freq_range = (4, 8)
    elif band == 'Alpha':
        freq_range = (8, 12)
    elif band == 'Beta':
        freq_range = (12, 30)
    else:
        raise ValueError("Invalid frequency band")
    
    mean_values = {}
    for electrode, psd_values in data.items():
        f = np.linspace(0, 30, len(psd_values))
        band_indices = np.where((f >= freq_range[0]) & (f < freq_range[1]))[0]
        mean_values[electrode] = np.mean(psd_values[band_indices])
    
    return mean_values

def main():
    # Check if file paths are provided as arguments
    if len(sys.argv) < 2:
        print("Usage: python psd_calculation.py <file1.edf> <file2.edf> ...")
        sys.exit(1)

    # Get file paths from command-line arguments
    file_paths = sys.argv[1:]

    # Create a Features folder if it doesn't exist
    features_folder = 'Features'
    if not os.path.exists(features_folder):
        os.makedirs(features_folder)

    # Separate files for stressed and relaxed conditions
    conditions = {'Relaxed': [], 'Stressed': []}

    # Process each .edf file
    for file_path in file_paths:
        subject_name, condition = os.path.splitext(os.path.basename(file_path))[0].split('_')[0], "Relaxed" if file_path.endswith("_1.edf") else "Stressed"
        conditions[condition].append(subject_name)
        
        # Calculate PSD for the current file
        psd_data = calculate_psd(file_path)
        
        # Calculate peak and mean values for each band
        for band in ['Delta', 'Theta', 'Alpha', 'Beta']:
            # Peak values
            peak_values = calculate_peak_value(psd_data, band)
            peak_df = pd.DataFrame(peak_values, index=[subject_name])
            peak_file_name = os.path.join(features_folder, f"{condition}_{band}_peak_values.csv")
            if os.path.exists(peak_file_name):
                peak_df.to_csv(peak_file_name, mode='a', header=False)
            else:
                peak_df.to_csv(peak_file_name)

            # Mean values
            mean_values = calculate_mean_value(psd_data, band)
            mean_df = pd.DataFrame(mean_values, index=[subject_name])
            mean_file_name = os.path.join(features_folder, f"{condition}_{band}_mean_values.csv")
            if os.path.exists(mean_file_name):
                mean_df.to_csv(mean_file_name, mode='a', header=False)
            else:
                mean_df.to_csv(mean_file_name)

    # Print confirmation
    print("PSD CSV files generated successfully.")

if __name__ == "__main__":
    main()