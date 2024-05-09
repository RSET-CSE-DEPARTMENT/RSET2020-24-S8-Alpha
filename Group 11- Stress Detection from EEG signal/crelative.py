import mne
import numpy as np
import csv
import hfda
from scipy.signal import welch,butter,filtfilt
import os

fs=500
frame_length=500
overlap=0
def compute_msc(frame1, frame2):
    # Compute MSC for a pair of frames
    fft_frame1 = np.fft.fft(frame1)
    fft_frame2 = np.fft.fft(frame2)

    cross_spectral_density = fft_frame1 * np.conj(fft_frame2)
    auto_spectral_density1 = fft_frame1 * np.conj(fft_frame1)
    auto_spectral_density2 = fft_frame2 * np.conj(fft_frame2)

    msc_value = np.sum(np.abs(cross_spectral_density)**2) / (np.sum(np.abs(auto_spectral_density1)) * np.sum(np.abs(auto_spectral_density2)))
    return msc_value

# Function to compute band-specific MSC values
def compute_band_msc(eeg_data_subset, band):
    # Apply bandpass filter
    filtered_data = bandpass_filter(eeg_data_subset, band[0], band[1], fs)
    
    # Compute MSC for filtered data
    num_frames = (len(filtered_data) - overlap) // max(1, (frame_length - overlap))
    if num_frames == 0:
        return np.zeros(1)  # Return an array of zeros if there are no frames
    msc_values = np.zeros(num_frames)
    for i in range(num_frames):
        start_index = i * max(1, (frame_length - overlap))
        end_index = start_index + frame_length
        frame = filtered_data[start_index:end_index]
        msc_values[i] = compute_msc(frame, frame)
    return msc_values

# Bandpass filter function
def bandpass_filter(data, lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    y = filtfilt(b, a, data)
    return y

# Directory containing EDF files
directory = "C:\\Users\\CHACKOCHAN SANJAI\\Downloads\\EDF\\"

# Iterate over files in the directory
for file_name in os.listdir(directory):
    if file_name.endswith(".edf"):
        file_path = os.path.join(directory, file_name)
        print("Processing file:", file_path)

        # Load EDF data
        raw = mne.io.read_raw_edf(file_path, preload=True)

        # Select channels for HFD calculation (user-defined)
        channels_to_read = ['EEG Fp1','EEG Fp2','EEG F3','EEG F4','EEG F7','EEG F8','EEG T3','EEG T4','EEG C3','EEG C4','EEG T5','EEG T6','EEG P3','EEG P4','EEG O1','EEG O2','EEG Fz','EEG Cz','EEG Pz','EEG A2-A1','ECG ECG']
        hfd_array=['EEG Fp1', 'EEG Fp2', 'EEG F3', 'EEG F4', 'EEG F7', 'EEG F8']
        rt_array=['EEG Fz','EEG F3','EEG F4','EEG Fp2','EEG Fp1']
        ra_array=['EEG O1','EEG P3','EEG Pz','EEG Fp2','EEG Fp1']
        msc_calc=['EEG Fp1', 'EEG Fp2']
        # Create a list to hold the results
        results = []

        # Iterate over each channel and calculate HFD
        for ch_name in channels_to_read:
            ch_data = raw[ch_name][0]  # Get the data of the channel
            sfreq = int(raw.info['sfreq'])  # Sampling frequency
            n_samples_first_minute = sfreq * 60
            data = ch_data[0][:n_samples_first_minute]  # Extract the data values
            n_samples = len(data)
            segment_length = sfreq * 2  # Length of each segment in samples
            overlap = segment_length // 2  # Overlapping segments

            # Iterate over the data in segments
            channel_results = []
            for start in range(0, n_samples - segment_length + 1, overlap):
                print(f"Processing segment {start} to {start + segment_length}")
                segment_data = data[start:start + segment_length]
                if hfd_array is None or ch_name in hfd_array:
                    hfd_value = hfda.measure(segment_data, k_max=10)
                    print(hfd_value)  # Calculate HFD using hfda.measure
                    if not channel_results:
                        channel_results.append('h' + ch_name)
                    channel_results.append(hfd_value)

            if channel_results:
                results.append(channel_results)

            channel_results = []
            for start in range(0, n_samples - segment_length + 1, overlap):
                print(f"Processing segment {start} to {start + segment_length}")
                segment_data = data[start:start + segment_length]
                if rt_array is None or ch_name in rt_array:
                    f, Pxx = welch(segment_data, fs=500, nperseg=500)
                    theta_indices = np.where((f >= 4) & (f <= 8))[0]
                    absolute_power_theta = np.trapz(Pxx[theta_indices])
                    gamma_indices = np.where((f >= 30) & (f <= 40))[0]
                    absolute_power_gamma = np.trapz(Pxx[gamma_indices])
                    beta_indices = np.where((f >= 13) & (f <= 30))[0]
                    absolute_power_beta = np.trapz(Pxx[beta_indices])
                    alpha_indices = np.where((f >= 8) & (f <= 13))[0]
                    absolute_power_alpha = np.trapz(Pxx[alpha_indices])
                    total_power = absolute_power_theta + absolute_power_alpha + absolute_power_beta + absolute_power_gamma
                    rp_theta = absolute_power_theta / total_power
                    if not channel_results:
                        channel_results.append('rt' + ch_name)
                    channel_results.append(rp_theta)

            if channel_results:
                results.append(channel_results)

            channel_results = []
            for start in range(0, n_samples - segment_length + 1, overlap):
                print(f"Processing segment {start} to {start + segment_length}")
                segment_data = data[start:start + segment_length]
                if ra_array is None or ch_name in ra_array:
                    f, Pxx = welch(segment_data, fs=500, nperseg=500)
                    theta_indices = np.where((f >= 4) & (f <= 8))[0]
                    absolute_power_theta = np.trapz(Pxx[theta_indices])
                    gamma_indices = np.where((f >= 30) & (f <= 40))[0]
                    absolute_power_gamma = np.trapz(Pxx[gamma_indices])
                    beta_indices = np.where((f >= 13) & (f <= 30))[0]
                    absolute_power_beta = np.trapz(Pxx[beta_indices])
                    alpha_indices = np.where((f >= 8) & (f <= 13))[0]
                    absolute_power_alpha = np.trapz(Pxx[alpha_indices])
                    total_power = absolute_power_theta + absolute_power_alpha + absolute_power_beta + absolute_power_gamma
                    rp_alpha = absolute_power_alpha / total_power
                    if not channel_results:
                        channel_results.append('ra' + ch_name)
                    channel_results.append(rp_alpha)

            if channel_results:
                results.append(channel_results)

            if msc_calc is None or ch_name in msc_calc:
                for start in range(0, n_samples - segment_length + 1, overlap):
                    print(f"Processing segment {start} to {start + segment_length}")
                    segment_data = data[start:start + segment_length]
                    alpha_msc = compute_band_msc(segment_data, (8, 12))
                    theta_msc = compute_band_msc(segment_data, (4, 8))
                    gamma_msc = compute_band_msc(segment_data, (30, 80))
                    if not channel_results:
                        channel_results.append('msc_alpha_' + ch_name)
                    
                        # channel_results.append('msc_theta_' + ch_name)
                        # channel_results.append('msc_gamma_' + ch_name)
                    channel_results.append(alpha_msc)
                    # channel_results.extend(theta_msc)
                    # channel_results.extend(gamma_msc)

            if channel_results:
                results.append(channel_results)     

        # Transpose results to have segments as rows and channels as columns
        results_transposed = list(map(list, zip(*results)))

        # Write results to CSV file
        output_filename = f"{file_name}_results.csv"
        output_file_path = os.path.join(directory, output_filename)
        with open(output_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(results_transposed)

        print(f"Results written to {output_filename}")
