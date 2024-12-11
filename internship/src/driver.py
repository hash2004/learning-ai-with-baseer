import numpy as np
import soundfile as sf
import argparse
import os
import sys

def load_audio(file_path):
    """
    Load an audio file and convert it to mono if it's stereo.

    Parameters:
    - file_path (str): Path to the audio file.

    Returns:
    - audio (np.ndarray): Audio signal.
    - sample_rate (int): Sampling rate of the audio file.
    """
    try:
        audio, sample_rate = sf.read(file_path)
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)  # Convert to mono by averaging channels
        return audio, sample_rate
    except Exception as e:
        print(f"Error loading audio file {file_path}: {e}")
        sys.exit(1)

def calculate_average_loudness(audio, sample_rate, frame_size=2048, hop_size=512):
    """
    Calculate the average RMS loudness in decibels (dB).

    Parameters:
    - audio (np.ndarray): Audio signal.
    - sample_rate (int): Sampling rate of the audio.
    - frame_size (int): Number of samples per frame.
    - hop_size (int): Number of samples to skip between frames.

    Returns:
    - average_loudness (float): Average loudness in dB.
    """
    rms_values = []
    for start in range(0, len(audio) - frame_size + 1, hop_size):
        frame = audio[start:start + frame_size]
        rms = np.sqrt(np.mean(frame**2))
        rms_db = 20 * np.log10(rms + 1e-12)
        rms_values.append(rms_db)
    
    if not rms_values:
        return float("-inf")  
    average_loudness = np.mean(rms_values)
    return average_loudness

def is_microphone_disconnected(loudness, threshold=-50):
    """
    Determine if the microphone is disconnected based on loudness.

    Parameters:
    - loudness (float): Average loudness in dB.
    - threshold (float): Loudness threshold in dB.

    Returns:
    - (bool): True if microphone is disconnected, False otherwise.
    """
    return loudness < threshold

def main():
    parser = argparse.ArgumentParser(description="Detect if the microphone was disconnected based on audio file loudness.")
    parser.add_argument("audio_file", type=str, help="Path to the input audio file (e.g., WAV, FLAC, etc.)")
    parser.add_argument("--threshold", type=float, default=-50.0, help="Loudness threshold in dB to determine disconnection (default: -50 dB)")
    args = parser.parse_args()

    audio_file = args.audio_file
    threshold = args.threshold

    if not os.path.isfile(audio_file):
        print(f"Error: File '{audio_file}' does not exist.")
        sys.exit(1)

    audio, sample_rate = load_audio(audio_file)
    if audio is None:
        print("Failed to load audio.")
        sys.exit(1)

    average_loudness = calculate_average_loudness(audio, sample_rate)
    print(f"Average Loudness: {average_loudness:.2f} dB")

    if is_microphone_disconnected(average_loudness, threshold):
        return True # if the microphone is disconnected
    else:
        return False

if __name__ == "__main__":
    connected = main()
    if connected == True :
        print("The microphone is disconnected")
    else:
        print("The microphone is connected")
