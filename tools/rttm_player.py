
import sys
import re 
import time
from pydub import AudioSegment
from pydub.playback import play

def play_audio_segment(start_time_ms, end_time_ms, file_path):
    # Load audio file
    audio = AudioSegment.from_file(file_path)

    # Slice audio
    segment = audio[start_time_ms:end_time_ms]

    # Play audio segment
    play(segment)



def read_file_line_by_line(filename):
    with open(filename, 'r') as file:
        for line in file:

            match = re.search(r"(\d+\.\d+) (\d+\.\d+) <NA> <NA> ([a-zA-Z0-9_]+)", line)
            if not match:
                print("Error: Something went wrong", file=sys.stderr)
                sys.exit(1)
            start = int(float(match.group(1)) * 1000)
            duration = int(float(match.group(2)) * 1000)
            end = start + duration
            speaker = match.group(3)

            print(f"{speaker}: {start} : {end}")
            play_audio_segment(start, end, "/Users/brono/GitHub/database/clean-audio-441/p_mono-sastre09_part1.wav")
            time.sleep(2)



if len(sys.argv) > 1:  # check if a command-line argument was provided
    filename = sys.argv[1]  # get the filename from the command-line argument
    read_file_line_by_line(filename)
else:
    print("Please provide a filename as a command-line argument.")
