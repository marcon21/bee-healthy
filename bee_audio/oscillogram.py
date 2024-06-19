import wave
import numpy as np
import matplotlib.pyplot as plt


def read_wav_file(filename):
    with wave.open(filename, "r") as wav_file:
        # Extract Raw Audio from Wav File
        signal = wav_file.readframes(-1)
        signal = np.frombuffer(signal, dtype=np.int16)

        # Get the frame rate
        framerate = wav_file.getframerate()
        print(f"Frame rate: {framerate} frames/second")

        # Get the number of channels
        channels = wav_file.getnchannels()
        print(f"Number of channels: {channels}")

    return signal, framerate, channels


def plot_oscillogram(signal, framerate, channels):
    # If stereo, we need to split the channels
    if channels == 2:
        signal = signal[::2]

    # Create a time axis in seconds
    times = np.linspace(0, len(signal) / framerate, num=len(signal))

    plt.figure(figsize=(15, 5))
    plt.plot(times, signal)
    plt.title("Oscillogram")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.show()


if __name__ == "__main__":
    filename = "chunks/audio001/chunk_0017.wav"
    signal, framerate, channels = read_wav_file(filename)
    plot_oscillogram(signal, framerate, channels)
