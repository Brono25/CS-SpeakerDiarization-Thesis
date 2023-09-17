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




from src.functions.transcript import Transcript, load_transcript_from_file
tr = Transcript(uri='herring06')

file = "/Users/brono/GitHub/cs-dataset/code-switched/herring06/herring06.tr"
tr = load_transcript_from_file(uri='herring06', file=file)

uem = tr.get_transcript_speaker_overlap_timeline()
tr_no_ol = tr.crop_transcript_from_uem(uem)

a,b = tr.duration()
print(a, b)