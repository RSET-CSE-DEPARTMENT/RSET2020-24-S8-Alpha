import sys
import os
import pandas as pd
import hfda
import mne

def calculate_hfd_for_files(file_paths, k_max):
    hfd_values = {}
    for file_path in file_paths:
        # Check if the file exists
        if not os.path.isfile(file_path):
            print(f"File not found: {file_path}")
            continue
        
        # Check if the file name ends with "_2.edf"
        if not file_path.endswith("_1.edf"):
            print(f"Skipping file: {file_path}. File name doesn't end with '_2.edf'.")
            continue

        # Load signals from the EDF file using mne
        raw = mne.io.read_raw_edf(file_path, preload=True)
        data = raw.get_data()

        # Extract EEG data and sampling frequency
        eeg_data, sfreq = data[:20], raw.info['sfreq']  # Take first 20 channels
        
        # Calculate HFD for each electrode
        for i, channel in enumerate(raw.ch_names[:20]):
            D = hfda.measure(eeg_data[i], k_max)

            # Store HFD value
            file_name = os.path.basename(file_path)
            if file_name not in hfd_values:
                hfd_values[file_name] = {}
            hfd_values[file_name][channel] = D

    return hfd_values

def main():
    # Check if file paths are provided as arguments
    if len(sys.argv) < 2:
        print("Usage: python hfd_relaxed.py <file1.edf> <file2.edf> ...")
        sys.exit(1)

    # Get file paths from command-line arguments
    file_paths = sys.argv[1:]

    # Define maximum k value
    k_max = 250

    # Calculate HFD values for the provided files
    hfd_results = calculate_hfd_for_files(file_paths, k_max)

    # Convert dictionary to DataFrame
    df = pd.DataFrame.from_dict(hfd_results, orient='index')

    # Define the path to the Features folder
    features_folder = 'Features'
    if not os.path.exists(features_folder):
        os.makedirs(features_folder)

    # Write DataFrame to CSV in the Features folder
    csv_file_path = os.path.join(features_folder, 'relaxed_hfd_values.csv')
    df.to_csv(csv_file_path)
    print(f"HFD values calculated and saved to '{csv_file_path}'.")

if __name__ == "__main__":
    main()
