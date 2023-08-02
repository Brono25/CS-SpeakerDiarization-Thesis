from pyannote.core import Annotation, Segment
import os
import matplotlib.pyplot as plt
import json
from collections import defaultdict, OrderedDict

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

from src.transcript import Transcript, convert_cha_to_transcript
from src.utilities import (
    plot_annotations,
    get_uri_list,
    CHA_FILES_DIR,
    ZELEDON_LIST,
    HERRING_LIST,
    SASTRE_LIST,
)
from src.cs_metrics import CSMetrics


uri = "zeledon14"

cha_file = f"{CHA_FILES_DIR}/{uri}.cha"
transcript = convert_cha_to_transcript(cha_file=cha_file)
metrics = CSMetrics(transcript=transcript)


spans = metrics.get_spans_between_switchpoints_seconds()

language = spans["language"]
durations = spans["time"]
combined = zip(spans["time"], spans["language"])
sorted_combined = sorted(combined, key=lambda x: x[0], reverse=True)
i= 0
total_spa = 0
total_eng = 0
for duration, lang in sorted_combined:
    

    if lang == "SPA":
        total_spa += duration
    else:
        total_eng += duration


    if i < 16:
        print(f"{lang} {duration:.0f}|", end = " ")
    i += 1
print()
print(f"Eng approx: {total_eng / 60:.1f} minutes")
print(f"Spa approx: {total_spa / 60:.1f} minutes")