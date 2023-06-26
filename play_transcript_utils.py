

import pyaudio
from pydub import AudioSegment
import matplotlib.pyplot as plt
import numpy as np

# time in milliseconds
def play_audio_slice(filename, start, end):
    # Load audio file
    audio = AudioSegment.from_file(filename, format="wav")

    # Slice audio
    sliced_audio = audio[start:end]

    # Initialize PyAudio
    p = pyaudio.PyAudio()

    # Open stream
    stream = p.open(format=p.get_format_from_width(sliced_audio.sample_width),
                    channels=sliced_audio.channels,
                    rate=sliced_audio.frame_rate,
                    output=True)

    # Play audio
    stream.write(sliced_audio.raw_data)

    # Close stream
    stream.stop_stream()
    stream.close()

    # Close PyAudio
    p.terminate()



def plot_slice(audio_data, start_ms, end_ms, sample_rate):
    # Convert start and end times from ms to sample indices
    start_index = int(start_ms / 1000 * sample_rate)
    end_index = int(end_ms / 1000 * sample_rate)

    # Extract the slice from the audio data
    audio_slice = audio_data[start_index:end_index]

    # Create time array
    t = np.linspace(start_ms / 1000, end_ms / 1000, len(audio_slice))

    # Plot the audio slice
    plt.figure(figsize=(14, 5))
    plt.plot(t, audio_slice)
    plt.xlabel('Time (s)')
    plt.ylabel('Amplitude')
    plt.show()
