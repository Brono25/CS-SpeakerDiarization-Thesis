import sys
import pyaudio
from pydub import AudioSegment

def play_audio(filename, start_ms, end_ms):
    # Load audio file
    audio = AudioSegment.from_file(filename, format="mp3")

    # Slice audio
    sliced_audio = audio[start_ms:end_ms]

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

if __name__ == "__main__":
    filename = sys.argv[1]
    timestamps = sys.argv[2].split('_')
    start_ms = int(timestamps[0])  # change to int for milliseconds
    end_ms = int(timestamps[1])  # change to int for milliseconds

    play_audio(filename, start_ms, end_ms)
