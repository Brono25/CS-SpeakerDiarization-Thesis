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


uri_list = get_uri_list()
data = pd.DataFrame()
m_min = 0
m_max = 0
i_min = 0
i_max = 0
b_min = 0
b_max = 0
data = defaultdict(dict)
for uri in uri_list:
    cha_file = f"{CHA_FILES_DIR}/{uri}.cha"
    transcript = convert_cha_to_transcript(cha_file=cha_file)
    metrics = CSMetrics(transcript=transcript)
    m_index = metrics.m_index() 
    i_index = metrics.i_index() 
    burstiness = metrics.burstiness() 

    # --collecting data
    span, density = metrics.get_switchpoint_span_density()
    data[uri] = {
        "span": span,
        "density": density,
        "m-index": m_index,
        "i-index": i_index,
        "burstiness": burstiness,
    }

    if m_index > m_max:
        m_max = m_index
    elif m_min > m_index:
        m_min = m_index

    if i_index > i_max:
        i_max = i_index
    elif i_min > i_index:
        i_min = i_index

    if burstiness > b_max:
        b_max = burstiness
    elif b_min > burstiness and burstiness != -1:
        b_min = burstiness


print(f"m-index range: {m_min:.2f}, {m_max:.2f}")
print(f"i-index range: {i_min:.2f}, {i_max:.2f}")
print(f"b-index range: {b_min:.2f}, {b_max:.2f}")

""" with open("src/data/density_data.json", "w") as f:
    json.dump(data, f, indent=4)
 """


# create lists for the audio tracks, i-index values, and burstiness values
tracks = list(data.keys())
i_index = [data[uri]["i-index"] for uri in tracks]
burstiness = [data[uri]["burstiness"] for uri in tracks]

# sort both i_index and burstiness based on i_index in ascending order
sorted_values = sorted(zip(i_index, burstiness), key=lambda x: x[1])
i_index, burstiness = zip(*sorted_values)  # unzip the sorted pairs
i_index = list(i_index)[1:]  # removes the first value
burstiness = list(burstiness)[1:]  # removes the first value
tracks = list(tracks)[1:]
# create a figure and a set of subplots

fig, ax1 = plt.subplots(figsize=(6, 6))
plt.title("I-index and Burstiness of Each Audio File", fontsize=14)
# plot the i-index values on the left y-axis
ax1.plot(range(len(tracks)), i_index, 'bo')
ax1.set_xlabel('Audio Track Number', fontsize=14)
ax1.set_ylabel('I-index', color='b', fontsize=14)
ax1.tick_params('y', colors='b')

# create a second y-axis sharing the same x-axis
ax2 = ax1.twinx()

# plot the burstiness values on the right y-axis
ax2.plot(range(len(tracks)), burstiness, 'ro')
ax2.set_ylabel('Burstiness', color='r', fontsize=14)
ax2.tick_params('y', colors='r')
ax2.set_ylim([0,0.6]) 
plt.show()