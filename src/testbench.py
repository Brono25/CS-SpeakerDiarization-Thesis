from pyannote.core import Annotation, Segment
import os
import matplotlib.pyplot as plt
# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

from src.transcript import Transcript, convert_cha_to_transcript
from src.utilities import plot_annotations, get_uri_list, CHA_FILES_DIR, ZELEDON_LIST, HERRING_LIST, SASTRE_LIST
from src.cs_metrics import CSMetrics


uri_list = get_uri_list()
data = pd.DataFrame()
m_min = 0
m_max = 0
i_min = 0
i_max = 0
b_min = 0
b_max = 0
for uri in ZELEDON_LIST:
    print(f"---------{uri}---------")
    cha_file = f"{CHA_FILES_DIR}/{uri}.cha"
    transcript = convert_cha_to_transcript(cha_file=cha_file)
    metrics = CSMetrics(transcript=transcript)
    m_index = metrics.m_index() * 100
    i_index = metrics.i_index() * 100
    burstiness = metrics.burstiness() * 100
    print(f"I-Index: {i_index:.2f}%")
    print(f"M-Index: {m_index:.2f}%")
    print(f"Burstiness: {burstiness:.2f}%")
    #--collecting data
    span, density = metrics.get_switchpoint_span_density()
    df = pd.DataFrame({
        'span_lengths': span,
        'counts': density,
        'uri': [uri]*len(span)  # create a new column for uri
    })
    data = pd.concat([data, df])
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
    elif b_min > burstiness:
        b_min = burstiness


# Plotting
plt.figure(figsize=(10, 6))
for uri in data.uri.unique():
    subset = data[data.uri == uri]
    sns.kdeplot(data=subset, x="span_lengths", label=uri)
plt.legend(title='URI')
plt.xlim(-10, 200) 
plt.ylim(0, 0.02) 
plt.show()


print(f"m-index range: {m_min:.2f}, {m_max:.2f}")
print(f"i-index range: {i_min:.2f}, {i_max:.2f}")
print(f"b-index range: {b_min:.2f}, {b_max:.2f}")