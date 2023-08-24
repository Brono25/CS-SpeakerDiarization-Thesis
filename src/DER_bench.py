# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re
from pyannote.core import Annotation
from pyannote.database.util import load_rttm
from pyannote.metrics.diarization import DiarizationErrorRate
import matplotlib.pyplot as plt
root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)
from functions.utilities import plot_annotations
# local imports
from functions.transcript import (  # noqa: E402
    Transcript,
    convert_cha_to_transcript,
    reduce_transcript,
)
from functions.cs_diarization_metrics import (
    CSDiarizationMetrics,
    timeline_to_annotation,
)

# --------------------SETUP--------------------
uri = "sastre01"
DIR = "/Users/brono/GitHub/cs-dataset/code-switched/sastre01"
reference_rttm_file = f"{DIR}/ref_{uri}.rttm"
ref = load_rttm(reference_rttm_file)[uri]

hypothesis_rttm_file = f"{DIR}/pyannote/{uri}_pyannote.rttm"
hyp = load_rttm(hypothesis_rttm_file)[uri]

language_rttm_file = f"{DIR}/ref_lang_{uri}.rttm"
lang = load_rttm(language_rttm_file)[uri]


# --------------------FUNCTIONS--------------------
def perform_language_error_rates(ref, hyp, lang, uri):
    cs_metrics = CSDiarizationMetrics(
        reference=ref, hypothesis=hyp, language_annotation=lang, uri=uri
    )
    components = cs_metrics.compute_components()
    metric = cs_metrics.compute_metric(components)
    for k, v in metric.items():
        print(f"{k} = {v * 100:.2f}")


def perform_confusion_analysis(uri, ref, hyp, lang, output):
    cs_metrics = CSDiarizationMetrics(
        reference=ref, hypothesis=hyp, language_annotation=lang, uri=uri
    )
    confusion_tl = cs_metrics._get_confusion_timeline()
    confusion_ann = timeline_to_annotation(uri, confusion_tl, "CONF")
    with open(output, "w") as file:
        confusion_ann.write_rttm(file)


def perform_missed_analysis(uri, ref, hyp, lang, output):
    cs_metrics = CSDiarizationMetrics(
        reference=ref, hypothesis=hyp, language_annotation=lang, uri=uri
    )
    miss_tl = cs_metrics._get_confusion_timeline()
    miss_ann = timeline_to_annotation(uri, miss_tl, "MISS")
    with open(output, "w") as file:
        miss_ann.write_rttm(file)


def plot_ref_vs_hyp(ref, hyp):
    
    plot_annotations([(ref, "Reference"),(hyp, "Hypothesis")])

def print_detailed_der(reference, hypothesis):
    # Initialize DiarizationErrorRate metric
    metric = DiarizationErrorRate(skip_overlap=True, collar=0.5)
    components = metric.compute_components(reference, hypothesis)

    print("Missed Detection:", components['missed detection'])
    print("False Alarm:", components['false alarm'])
    print("Confusion:", components['confusion'])
    der = metric(reference, hypothesis)
    print("Overall DER:", der)



# --------------------ANALYSIS--------------------



perform_language_error_rates(ref=ref, hyp=hyp, lang=lang, uri=uri)

output = f"{DIR}/pyannote/{uri}_miss_pyannote.rttm"
perform_missed_analysis(uri=uri, ref=ref, hyp=hyp, lang=lang, output=output)
output = f"{DIR}/pyannote/{uri}_conf_pyannote.rttm"
perform_confusion_analysis(uri=uri, ref=ref, hyp=hyp,lang=lang,  output=output)

print_detailed_der(reference=ref, hypothesis=hyp)
