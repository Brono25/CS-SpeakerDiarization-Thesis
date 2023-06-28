import play_transcript_utils as ptu
import re
import time
import matplotlib.pyplot as plt
import librosa
import numpy as np

AUDIO_PATH = "/Users/brono/Desktop/thesis-dataset.tmp/clean-audio-441"

transcript_file = "/Users/brono/Desktop/thesis-dataset.tmp/time-fixed-trans/sastre03_fixed.txt"
filename = re.match(r".*/(.*)_fixed\.txt", transcript_file).group(1)
audio_file = f"{AUDIO_PATH}/p_mono-{filename}.wav"
print(audio_file)

with open(transcript_file, 'r') as f:
    content = f.readlines()

inject_at = 501

# Load audio file using librosa
audio_data, sample_rate = librosa.load(audio_file)


for i, line in enumerate(content):

    match = re.search(r"(\d+)_(\d+)", line)
    if match and i >= inject_at:
        start, end = map(int, match.groups())
        print(f"{i}/{len(content)}: {line}")
        
        

        ptu.play_audio_slice(audio_file, start, end)
        ptu.plot_slice(audio_data, start, end, sample_rate)
      



