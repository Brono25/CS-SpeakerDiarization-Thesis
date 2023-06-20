import sys
import pyaudio
from pydub import AudioSegment

def play_audio(filename, start, duration):
    # Load audio file
    audio = AudioSegment.from_file(filename, format="mp3")

    # Convert start and duration to milliseconds
    start *= 1000
    duration *= 1000

    # Slice audio
    sliced_audio = audio[start:start+duration]

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
    start = float(sys.argv[2])  # change to float
    duration = float(sys.argv[3])  # change to float

    play_audio(filename, start, duration)
