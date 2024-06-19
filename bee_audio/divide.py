import os
import wave


def split_wav_file(input_file: str, chunk_size: int, output_dir: str):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with wave.open(input_file, "rb") as wav:
        params = wav.getparams()
        n_channels = params.nchannels
        sampwidth = params.sampwidth
        framerate = params.framerate
        n_frames = params.nframes
        comptype = params.comptype
        compname = params.compname

        # Calculate the number of frames in each chunk
        frames_per_chunk = int(chunk_size * framerate)

        # Create the output subdirectory for the chunks
        output_dir = os.path.join(output_dir, input_file.split(".")[0])
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        else:
            # Clear the output directory if it already exists
            for file in os.listdir(output_dir):
                os.remove(os.path.join(output_dir, file))

        # Read and write the chunks
        chunk_num = 0
        while True:
            frames = wav.readframes(frames_per_chunk)
            if len(frames) == 0:
                break

            chunk_file = os.path.join(output_dir, f"chunk_{chunk_num:04d}.wav")
            with wave.open(chunk_file, "wb") as chunk_wav:
                chunk_wav.setnchannels(n_channels)
                chunk_wav.setsampwidth(sampwidth)
                chunk_wav.setframerate(framerate)
                chunk_wav.setcomptype(comptype, compname)
                chunk_wav.writeframes(frames)

            chunk_num += 1


if __name__ == "__main__":
    input_file = "audio001.wav"  # Path to the input WAV file
    chunk_size = 60  # Chunk size in seconds
    output_dir = "chunks"  # Directory to save the chunks

    split_wav_file(input_file, chunk_size, output_dir)
