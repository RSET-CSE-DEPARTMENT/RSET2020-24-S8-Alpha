import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pywt
from scipy.signal import welch
import os
import mne
import sys


def calculate_absolute_power_theta(eeg_data_first_91000, fs=500,frame_size=500):
    """
    Calculate the absolute power of theta wave (4~8Hz) from EEG data.

    Parameters:
    - eeg_data: 1D numpy array, EEG data for a single channel.
    - fs: Sampling frequency of the EEG data.

    Returns:
    - absolute_power_theta: Absolute power of theta wave.
    """

    # Calculate power spectral density using Welch method
    f, Pxx = welch(eeg_data_first_91000, fs=fs, nperseg=frame_size)

    # Find the indices corresponding to the theta frequency range (4~8Hz)
    theta_indices = np.where((f >= 4) & (f <= 8))[0]

    # Calculate the absolute power in the theta range
    absolute_power_theta = np.trapz(Pxx[theta_indices])

    return absolute_power_theta

def calculate_relative_power(theta_power, alpha_power, beta_power, gamma_power):
    """
    Calculate relative power of the theta wave.

    Parameters:
    - theta_power: Absolute power of the theta wave.
    - alpha_power: Absolute power of the alpha wave.
    - beta_power: Absolute power of the beta wave.
    - gamma_power: Absolute power of the gamma wave.

    Returns:
    - rp_theta: Relative power of the theta wave.
    """

    # Calculate total power
    total_power = theta_power + alpha_power + beta_power + gamma_power

    # Calculate relative power of the theta wave
    rp_theta = theta_power / total_power

    return rp_theta

def calculate_absolute_power_gamma(eeg_data_first_91000, fs=500, frame_size=500):
    """
    Calculate the absolute power of gamma wave (30~40Hz) from EEG data.

    Parameters:
    - eeg_data: 1D numpy array, EEG data for a single channel.
    - fs: Sampling frequency of the EEG data.
    - frame_size: Size of each segment for computing the power spectral density.

    Returns:
    - absolute_power_gamma: Absolute power of gamma wave.
    """

    # Calculate power spectral density using Welch method
    f, Pxx = welch(eeg_data_first_91000, fs=fs, nperseg=frame_size)

    # Find the indices corresponding to the gamma frequency range (30~40Hz)
    gamma_indices = np.where((f >= 30) & (f <= 40))[0]

    # Calculate the absolute power in the gamma range
    absolute_power_gamma = np.trapz(Pxx[gamma_indices])

    return absolute_power_gamma

def calculate_absolute_power_beta(eeg_data_first_91000, fs=500, frame_size=500):
    """
    Calculate the absolute power of beta wave (13~30Hz) from EEG data.

    Parameters:
    - eeg_data: 1D numpy array, EEG data for a single channel.
    - fs: Sampling frequency of the EEG data.
    - frame_size: Size of each segment for computing the power spectral density.

    Returns:
    - absolute_power_beta: Absolute power of beta wave.
    """

    # Calculate power spectral density using Welch method
    f, Pxx = welch(eeg_data_first_91000, fs=fs, nperseg=frame_size)

    # Find the indices corresponding to the beta frequency range (13~30Hz)
    beta_indices = np.where((f >= 13) & (f <= 30))[0]

    # Calculate the absolute power in the beta range
    absolute_power_beta = np.trapz(Pxx[beta_indices])

    return absolute_power_beta

def calculate_absolute_power_alpha(eeg_data_first_91000, fs=500, frame_size=500):
    """
    Calculate the absolute power of alpha wave (8~13Hz) from EEG data.

    Parameters:
    - eeg_data: 1D numpy array, EEG data for a single channel.
    - fs: Sampling frequency of the EEG data.
    - frame_size: Size of each segment for computing the power spectral density.

    Returns:
    - absolute_power_alpha: Absolute power of alpha wave.
    """

    # Calculate power spectral density using Welch method
    f, Pxx = welch(eeg_data_first_91000, fs=fs, nperseg=frame_size)

    # Find the indices corresponding to the alpha frequency range (8~13Hz)
    alpha_indices = np.where((f >= 8) & (f <= 13))[0]

    # Calculate the absolute power in the alpha range
    absolute_power_alpha = np.trapz(Pxx[alpha_indices])

    return absolute_power_alpha

def read_edf_file(file_path):
    raw_data = mne.io.read_raw_edf(file_path, preload=True)
    return raw_data.get_data()


def main():
    if len(sys.argv) < 2:
        print("Usage: python psd_calculation.py <file1.edf> <file2.edf> ...")
        sys.exit(1)

    # Get file paths from command-line arguments
    file_paths = sys.argv[1:]

    fs = 500
    num_electrodes = 21

    # Initialize DataFrames for results
    results_df_1 = pd.DataFrame()  # For files ending with '_1.edf'
    results_df_2 = pd.DataFrame()  # For files ending with '_2.edf'

    # Process each file
    for file_path in file_paths:
        if file_path.endswith('_1.edf'):
            try:
                # Extract file name from file path and remove extension
                file_name = os.path.splitext(os.path.basename(file_path))[0]

                # Read EEG data
                eeg_data = mne.io.read_raw_edf(file_path, preload=False)
                channel_names = eeg_data.ch_names
                
                # Process EEG data
                rp_theta_list = []  # List to store rp_theta values for dataset
                for electrode in range(num_electrodes):
                    eeg_data_electrode = eeg_data.get_data()[electrode, :]
                    absolute_power_theta = calculate_absolute_power_theta(eeg_data_electrode, fs=fs)
                    absolute_power_alpha = calculate_absolute_power_alpha(eeg_data_electrode, fs=fs)
                    absolute_power_beta = calculate_absolute_power_beta(eeg_data_electrode, fs=fs)
                    absolute_power_gamma = calculate_absolute_power_gamma(eeg_data_electrode, fs=fs)
                    rp_theta = calculate_relative_power(absolute_power_theta, absolute_power_alpha, absolute_power_beta,
                                                        absolute_power_gamma)
                    rp_theta_list.append(rp_theta)

                # Construct row data
                row_data = {'Patient_ID': file_name, **{channel_name: val for channel_name, val in zip(channel_names, rp_theta_list)}}
                results_df_1 = results_df_1._append(row_data, ignore_index=True)

            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")

        elif file_path.endswith('_2.edf'):
            try:
                # Extract file name from file path and remove extension
                file_name = os.path.splitext(os.path.basename(file_path))[0]

                # Read EEG data
                eeg_data = mne.io.read_raw_edf(file_path, preload=False)
                channel_names = eeg_data.ch_names
                
                # Process EEG data
                rp_theta_list = []  # List to store rp_theta values for dataset
                for electrode in range(num_electrodes):
                    eeg_data_electrode = eeg_data.get_data()[electrode, :]
                    absolute_power_theta = calculate_absolute_power_theta(eeg_data_electrode, fs=fs)
                    absolute_power_alpha = calculate_absolute_power_alpha(eeg_data_electrode, fs=fs)
                    absolute_power_beta = calculate_absolute_power_beta(eeg_data_electrode, fs=fs)
                    absolute_power_gamma = calculate_absolute_power_gamma(eeg_data_electrode, fs=fs)
                    rp_theta = calculate_relative_power(absolute_power_theta, absolute_power_alpha, absolute_power_beta,
                                                        absolute_power_gamma)
                    rp_theta_list.append(rp_theta)

                # Construct row data
                row_data = {'Patient_ID': file_name, **{channel_name: val for channel_name, val in zip(channel_names, rp_theta_list)}}
                results_df_2 = results_df_2._append(row_data, ignore_index=True)

            except Exception as e:
                print(f"Error processing file {file_path}: {str(e)}")

    # Write results to CSV files
    try:
        results_df_1.to_csv('Features/relaxed_theta_power.csv', index=False)  # For files ending with '_1.edf'
        print("CSV file for _1.edf files created successfully.")
    except Exception as e:
        print(f"Error writing CSV file for _1.edf files: {str(e)}")

    try:
        results_df_2.to_csv('Features/stressed_theta_power.csv', index=False)  # For files ending with '_2.edf'
        print("CSV file for _2.edf files created successfully.")
    except Exception as e:
        print(f"Error writing CSV file for _2.edf files: {str(e)}")

if __name__ == "__main__":
    main()
