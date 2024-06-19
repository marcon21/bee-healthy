import numpy as np
import scipy.fft
import wave
import matplotlib.pyplot as plt
from copy import deepcopy
from scipy.signal import savgol_filter

# from dotenv import load_dotenv


# load_dotenv()


# Function to read a WAV file
def read_wav(file_path):
    with wave.open(file_path, "rb") as wav_file:
        # Extract audio parameters
        num_channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        frame_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()

        # Read audio data
        audio_data = wav_file.readframes(num_frames)

        # Convert audio data to numpy array
        audio_array = np.frombuffer(audio_data, dtype=np.int16)

        # If stereo, take only one channel
        if num_channels == 2:
            audio_array = audio_array[::2]

        return audio_array, frame_rate


# Function to compute and plot FFT
def compute_fft(audio_data, frame_rate, show_plot=True):
    # Compute the real FFT
    fft_result = scipy.fft.rfft(audio_data)

    # Compute the frequencies corresponding to the FFT result
    fft_freqs = scipy.fft.rfftfreq(len(audio_data), d=1 / frame_rate)

    if show_plot:
        plot_fft(fft_result, fft_freqs)

    return fft_result, fft_freqs


def plot_fft(fft_result, fft_freqs):
    # Plot the FFT result
    plt.figure(figsize=(12, 6))
    plt.plot(fft_freqs, np.abs(fft_result))
    plt.title("Original FFT of Audio Signal")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")
    plt.grid()
    plt.show()


def plot_time_domain(audio_data):
    # Plot the original audio signal in time domain

    plt.figure(figsize=(12, 6))
    if len(audio_data) == 2:
        a = deepcopy(audio_data[0])
        b = deepcopy(audio_data[1])
        a = abs(a)
        b = -abs(b)
        # smooth the signal
        a = np.convolve(a, np.ones(100) / 100, mode="same")
        b = np.convolve(b, np.ones(100) / 100, mode="same")

        plt.plot(a, label="Original Audio Signal")
        plt.plot(b, label="Filtered Audio Signal")

    plt.title("Original Audio Signal in Time Domain")
    plt.xlabel("Sample Index")
    plt.ylabel("Amplitude")
    plt.grid()
    plt.show()


# Function to apply band-pass filter in the frequency domain
def band_pass_filter(fft_result, fft_freqs, low_cutoff, high_cutoff):
    # Zero out frequencies outside the desired range
    filtered_fft = np.where(
        (fft_freqs >= low_cutoff) & (fft_freqs <= high_cutoff), fft_result, 0
    )

    return filtered_fft


# Function to compute and plot the inverse FFT
def compute_ifft(filtered_fft, show_plot=True):
    # Compute the inverse FFT
    filtered_audio_data = scipy.fft.irfft(filtered_fft)

    if show_plot:
        # Plot the filtered audio signal in time domain
        plot_time_domain(filtered_audio_data)

    return filtered_audio_data


if __name__ == "__main__":
    file_path = "chunks/audio001/chunk_0017.wav"
    audio_data, frame_rate = read_wav(file_path)

    # Compute the FFT of the original audio data
    fft_result, fft_freqs = compute_fft(audio_data, frame_rate, show_plot=False)

    # Apply band-pass filter
    low_cutoff = 10000  # Low cutoff frequency in Hz
    high_cutoff = 30000  # High cutoff frequency in Hz
    filtered_fft = band_pass_filter(fft_result, fft_freqs, low_cutoff, high_cutoff)

    # Compute the inverse FFT to get the filtered audio signal
    filtered_audio_data = compute_ifft(filtered_fft, show_plot=False)

    plot_time_domain([audio_data, filtered_audio_data])

    filtered_audio_data = np.int16(
        filtered_audio_data * (2**15 - 1) / np.max(np.abs(filtered_audio_data))
    )
    with wave.open("filtered_audio.wav", "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)  # 2 bytes for int16
        wav_file.setframerate(frame_rate)
        wav_file.writeframes(filtered_audio_data.tobytes())
