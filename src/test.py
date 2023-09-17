from pyannote.core import Annotation
from pyannote.core import Segment
import os
import time
from datetime import datetime

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re
import copy

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)




from src.functions.transcript import Transcript, transcript_duration
tr = Transcript(uri='test')

tr[Segment(0, 10)] = ('A', 'ENG', 'Hello world.')
tr[Segment(3, 5)] = ('B', 'ENG', 'Hello again.')
tr[Segment(8, 11)] = ('C', 'SPA', 'goodbye.')

ol = tr.get_transcript_speaker_overlap_timeline()
cropped_tr = tr.crop_transcript_from_uem(ol)
print(ol)


for start, end, label, lang, text in cropped_tr.itertr():
    print(start, end, label, lang, text)