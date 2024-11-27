import os
import pandas as pd
from datetime import datetime
import scipy.signal as signal
import librosa
import numpy as np
import audioread


def load_audio(file_path):
    try:
        audio, sr = librosa.load(file_path, sr=None)
    except audioread.NoBackendError:
        print(f"Error loading {file_path}: Format not recognized")
        return None, None
    return audio, sr

def extract_info_from_path(file_path):
    # Extracting parts from the file path
    print(file_path)
    parts = file_path.split('/')
    turbine_id = parts[1]  # Assuming 'data' is always the root folder
    filename = parts[-1]
    # Extracting datetime from the filename
    datetime_str = filename.split('Windrover')[0].strip()
    print(datetime_str)
    print(datetime_str)
    try:
        datetime_obj = datetime.strptime(datetime_str, "%Y-%m-%d %H_%M_%S.%f")
        print(datetime_obj)
    except ValueError:
        datetime_obj = datetime.strptime(datetime_str, "%Y_%m_%d_%H_%M_%S")
        print(datetime_obj)
    return turbine_id, datetime_obj, filename

# def process_audio_fft(file_path):
#     audio, sr = librosa.load(file_path, sr=None)
#     # Apply a high-pass filter
#     sos = signal.butter(10, 400, 'hp', fs=sr, output='sos')
#     filtered_audio = signal.sosfilt(sos, audio)
#     # Compute the FFT
#     fft_result = np.fft.rfft(filtered_audio)
#     fft_frequencies = np.fft.rfftfreq(len(filtered_audio), d=1/sr)

#     freq_bins = [(400, 2000), (2000, 8000), (8000, 22050)]
#     amplitude_bins = []

#     # Calculate average amplitude for each frequency bin
#     for low, high in freq_bins:
#         bin_mask = (fft_frequencies >= low) & (fft_frequencies <= high)
#         # bin_amplitudes = np.abs(fft_result[bin_mask])
#         bin_amplitudes = np.abs(fft_result[bin_mask])
#         avg_amplitude = np.mean(bin_amplitudes) if bin_amplitudes.size > 0 else 0
#         amplitude_bins.append(avg_amplitude)

#     return amplitude_bins

def process_audio_fft(file_path):
    try:
        audio, sr = librosa.load(file_path, sr=None)
        
        # Apply a high-pass filter
        sos = signal.butter(10, 400, 'hp', fs=sr, output='sos')
        filtered_audio = signal.sosfilt(sos, audio)
        
        # Compute the FFT
        fft_result = np.fft.rfft(filtered_audio)
        fft_frequencies = np.fft.rfftfreq(len(filtered_audio), d=1/sr)

        freq_bins = [(400, 2000), (2000, 8000), (8000, 22050)]
        loudness_bins = []

        # Calculate loudness (in dB) for each frequency bin
        for low, high in freq_bins:
            bin_mask = (fft_frequencies >= low) & (fft_frequencies <= high)
            bin_amplitudes = np.abs(fft_result[bin_mask]) # Magnitude of the complex number recevied from the FFT
            if bin_amplitudes.size > 0:
                rms = np.sqrt(np.mean(bin_amplitudes**2)) # !Root Mean Square of the Magnitude which corresponds to the pressure of the sound or the power sound?
                loudness_db = 10 * np.log10(rms/1e-12)  #1e-12 is the reference pressure in W
                print(loudness_db)
            else:
                loudness_db = float('-inf')  # if no frequencies in this bin
            loudness_bins.append(loudness_db)
        
        return loudness_bins
    except Exception as e:
        print(e)
        return [float('-inf'), float('-inf'), float('-inf')]

def process_audio_fft_average_loudness(file_path):
    audio, sr = librosa.load(file_path, sr=None)
    
    # Apply a high-pass filter
    sos = signal.butter(10, 400, 'hp', fs=sr, output='sos')
    filtered_audio = signal.sosfilt(sos, audio)
    
    # Compute the FFT
    fft_result = np.fft.rfft(filtered_audio)
    fft_frequencies = np.fft.rfftfreq(len(filtered_audio), d=1/sr)

    freq_bins = [(400, 2000), (2000, 8000), (8000, 22050)]
    loudness_bins = []

    # Calculate loudness (in dB) for each frequency bin
    for low, high in freq_bins:
        bin_mask = (fft_frequencies >= low) & (fft_frequencies <= high)
        bin_amplitudes = np.abs(fft_result[bin_mask])  # Magnitudes of the complex numbers

        if bin_amplitudes.size > 0:
            # Calculate loudness for each amplitude and then average
            loudness_values = 20 * np.log10(bin_amplitudes / 32767)  # Convert each amplitude to dB
            avg_loudness_db = np.mean(loudness_values)  # Average the loudness values in dB
        else:
            avg_loudness_db = float('-inf')  # if no frequencies in this bin
        
        loudness_bins.append(avg_loudness_db)
    
    return loudness_bins

def process_audio_fft_average_amplitude(file_path):
    audio, sr = librosa.load(file_path, sr=None)
    
    # Apply a high-pass filter
    sos = signal.butter(10, 400, 'hp', fs=sr, output='sos')
    filtered_audio = signal.sosfilt(sos, audio)
    
    # Compute the FFT
    fft_result = np.fft.rfft(filtered_audio)
    fft_frequencies = np.fft.rfftfreq(len(filtered_audio), d=1/sr)

    freq_bins = [(400, 2000), (2000, 8000), (8000, 22050)]
    loudness_bins = []

    # Calculate loudness (in dB) for each frequency bin
    for low, high in freq_bins:
        bin_mask = (fft_frequencies >= low) & (fft_frequencies <= high)
        bin_amplitudes = np.abs(fft_result[bin_mask])  # Magnitudes of the complex numbers
        avg_amplitudes = np.mean(bin_amplitudes) if bin_amplitudes.size > 0 else 0
        if avg_amplitudes.size > 0:
            # Calculate loudness for each amplitude and then average
            loudness_values = 20 * np.log10(avg_amplitudes / 32767)  # Convert each amplitude to dB
        else:
            loudness_values = float('-inf')  # if no frequencies in this bin
        
        loudness_bins.append(loudness_values)
    
    return loudness_bins

def process_audio_fft_average_loudness_min_max(file_path):
    audio, sr = librosa.load(file_path, sr=None)
    
    # Apply a high-pass filter
    sos = signal.butter(10, 400, 'hp', fs=sr, output='sos')
    filtered_audio = signal.sosfilt(sos, audio)
    
    # Compute the FFT
    fft_result = np.fft.rfft(filtered_audio)
    fft_frequencies = np.fft.rfftfreq(len(filtered_audio), d=1/sr)

    freq_bins = [(400, 2000), (2000, 8000), (8000, 22050)]
    average_loudness_bins = []
    min_loudness_bins = []
    max_loudness_bins = []
    
    # Calculate loudness (in dB) for each frequency bin
    for low, high in freq_bins:
        bin_mask = (fft_frequencies >= low) & (fft_frequencies <= high)
        bin_amplitudes = np.abs(fft_result[bin_mask])  # Magnitudes of the complex numbers

        if bin_amplitudes.size > 0:
            # Calculate loudness for each amplitude and then average
            loudness_values = 20 * np.log10(bin_amplitudes / 32767)  # Convert each amplitude to dB
            min_loudness_db = np.min(loudness_values)  # Average the loudness values in dB
            avg_loudness_db = np.mean(loudness_values)  # Average the loudness values in dB
            max_loudness_db = np.max(loudness_values)
        else:
            avg_loudness_db = float('-inf')  # if no frequencies in this bin
        
        average_loudness_bins.append(avg_loudness_db)
        min_loudness_bins.append(min_loudness_db)
        max_loudness_bins.append(max_loudness_db)
    
    return min_loudness_bins, average_loudness_bins, max_loudness_bins


def analyze_files(directory, process_audio_fn):
    data = []
    error_log = []

    # Walk through all files in the directory subtree
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".wav"):
                file_path = os.path.join(root, file)
                try:
                    turbine_id, datetime_obj, filename = extract_info_from_path(file_path)
                    power_bins = process_audio_fn(file_path)
                    print(f"Processed file: {filename}")
                    # Append the data to the list
                    data.append([filename, turbine_id, datetime_obj] + power_bins)
                except Exception as e:
                    error_message = f"Error processing file {file_path}: {e}"
                    print(error_message)
                    error_log.append(error_message)
    
    # If no files were processed, raise an exception
    if not data:
        raise FileNotFoundError("No valid '.wav' files found in the directory or processing failed for all files.")
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=['Filename', 'Turbine ID', 'Datetime', 'Bin1 Power', 'Bin2 Power', 'Bin3 Power'])

    # If there are errors, log them to a file (optional)
    if error_log:
        with open('error_log.txt', 'w') as f:
            for error in error_log:
                f.write(f"{error}\n")
        print("Errors encountered during processing. See 'error_log.txt' for details.")
    
    return df
def analyze_files_min_max(directory, process_audio_fn=process_audio_fft_average_loudness_min_max):
    data = []
    # Walk through all files in the directory subtree
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".wav"):
                file_path = os.path.join(root, file)
                turbine_id, datetime_obj, filename = extract_info_from_path(file_path)
                min_power_bins, average_power_bins, max_power_bins = process_audio_fn(file_path)
                difference = []
                for i in range(3):
                    difference_i = average_power_bins[i] - min_power_bins[i]
                    difference.append(difference_i)
                # Append the data to the list
                data.append([filename, turbine_id, datetime_obj] + min_power_bins + average_power_bins + max_power_bins + difference)
    
    # Create DataFrame
    df = pd.DataFrame(data, columns=['Filename', 'Turbine ID', 'Datetime',
                                    'Min Bin1 Power', 'Min Bin2 Power', 'Min Bin3 Power',
                                    'Average Bin1 Power', 'Average Bin2 Power', 'Average Bin3 Power',
                                    'Max Bin1 Power', 'Max Bin2 Power', 'Max Bin3 Power',
                                    'Difference Bin1 Power', 'Difference Bin2 Power', 'Difference Bin3 Power'])
    return df

def main():
    directory = 'data'  # Starting directory
    result_df = analyze_files(directory, process_audio_fft_average_loudness)
    # result_df_average_amplitude = analyze_files(directory, process_audio_fft_average_amplitude)
    result_df.to_csv('output-average-loudness.csv', index=False)
    # result_df_average_amplitude.to_csv('output-average-amplitude.csv', index=False)
    # result_df_min_max = analyze_files_min_max(directory)
    # result_df_min_max.to_csv('output-min-max.csv', index=False)
    print("CSV file has been saved.")

if __name__ == "__main__":
    main()
