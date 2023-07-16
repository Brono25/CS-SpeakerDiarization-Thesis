import time

import matplotlib.pyplot as plt
from pyannote.core import notebook
from pyannote.database.util import load_rttm
from pyannote.metrics.diarization import DiarizationErrorRate
from pydub import AudioSegment
from pydub.playback import play


def plot_segments(ref, hyp):
    fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    notebook.plot_annotation(ref, ax=axs[0], time=False)
    axs[0].set_title('Reference Annotation')
    notebook.plot_annotation(hyp, ax=axs[1], time=False)
    axs[1].set_title('Hypothesis Annotation')
    plt.tight_layout()
    plt.show()

def play_audio_segment(start_time_sec, end_time_sec, file_path):
    start_time_ms = start_time_sec * 1000 
    end_time_ms = end_time_sec * 1000
    audio = AudioSegment.from_file(file_path)
    segment = audio[start_time_ms:end_time_ms]
    play(segment)

ref_sastre09_1 = load_rttm("./ref_rttm/ref_sastre09_1.rttm")["sastre09_1"]
hyp_sastre09_1 = load_rttm("./hyp_rttm/hyp_sastre09_1.rttm")["sastre09_1"]

metric = DiarizationErrorRate(skip_overlap=True, collar=0.0)
der = metric(reference=ref_sastre09_1, hypothesis=hyp_sastre09_1) * 100
print(f"The DER is {der:.2f}%")

#plot_segments(ref_sastre09_1, hyp_sastre09_1)

# Assuming you have an audio file named audio_file.mp3
audio_file = "./wav/sastre09_1.wav"

for segment, _, label in hyp_sastre09_1.itertracks(yield_label=True):
    start_time_sec, end_time_sec = segment.start, segment.end
    print(f"Speaker {label}: Playing audio from {start_time_sec} to {end_time_sec}")
    play_audio_segment(start_time_sec, end_time_sec, audio_file)
    time.sleep(2)
