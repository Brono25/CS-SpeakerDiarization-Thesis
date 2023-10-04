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
from functions.cs_metrics import CSMetrics


with open("src/data/density_data.json", "r") as file:
    data = json.load(file)

plt.figure(figsize=(6, 6))
for uri, values in data.items():
    if (
        uri == "sastre08"
        or uri == "zeledon02"
        #or uri == "zeledon14"
        #or uri == "herring07"
    ):
        sns.kdeplot(
            x=values["span"], weights=values["density"], color="darkblue", lw=3, alpha=0.6
        )
    else:
        sns.kdeplot(
            x=values["span"],
            weights=values["density"],
            color="lightgrey",
            lw=1.5,
            alpha=1,
            linestyle="--",
        )

plt.title("Density Distributions of CS Span Lengths per Audio File",fontsize=14)
plt.xlim(-10, 100)
plt.ylim(0, 0.037)
plt.xlabel("Span Length (words)", fontsize=14)
plt.ylabel("Density", fontsize=14)
# Displaying the plot
plt.show()


# max  sastre08   min: zeledon02
