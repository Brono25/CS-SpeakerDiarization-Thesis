from pyannote.core import Annotation, Segment
import os
from pyannote.database.util import load_rttm
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.transcript import (  # noqa: E402
    Transcript,
    convert_cha_to_transcript,
)  # noqa: E402
from src.utilities import (  # noqa: E402
    ROOT_DIR,
    CHA_FILES_DIR,
    HYP_RTTM_DIR,
    debug_transcript_comparison,
)
from src.cs_metrics import CSMetrics
from cs_error import CSError

# Process files one at a time
uri = "sastre09"



#--------------
cha_file = f"{CHA_FILES_DIR}/{uri}.cha"
if not os.path.isfile(cha_file):
    print(f"{cha_file} not found.")


# --------------Create Transcript and RTTM files-------------- #
transcript = convert_cha_to_transcript(cha_file=cha_file)
transcript.save_transcript_to_file()
transcript.export_ref_rttm(support=True)
transcript.export_lang_rttm(support=True)
ref = transcript.get_ref_annotation(support=True)
lang = transcript.get_language_annotation(support=True)
hyp = load_rttm(f"{HYP_RTTM_DIR}/hyp_{uri}_1.rttm")[uri + '_1']


# --------------Code-Switching Metrics-------------- #
metrics = CSMetrics(transcript=transcript)
print(f"I-Index: {metrics.i_index() * 100:.2f}%")
print(f"M-Index: {metrics.m_index()* 100:.2f}%")
print(f"Burstiness: {metrics.burstiness()* 100:.2f}%")
#--plot
span, density = metrics.get_switchpoint_span_density()
data = pd.DataFrame({
    'span_lengths': span,
    'counts': density
})
sns.kdeplot(data=data, x="span_lengths")
plt.show()
sys.exit()


# --------------Language Errors-------------- #
analysis = LanguageError(
    uri=uri, reference=ref, hypothesis=hyp, language_annotation=lang
)
components = analysis.compute_components()
results = analysis.compute_metric(components=components)
for k, v in results.items():
    print(f"{k} = {v * 100:.2f} %")