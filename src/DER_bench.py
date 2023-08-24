# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re
from pyannote.database.util import load_rttm
from pyannote.metrics.diarization import DiarizationErrorRate
import matplotlib.pyplot as plt

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)
from functions.utilities import plot_annotations

from functions.cs_diarization_metrics import (
    CSDiarizationMetrics,
    timeline_to_annotation,
)

# --------------------SETUP--------------------
ROOT = "/Users/brono/GitHub/cs-dataset/code-switched/sastre01"
uri = "sastre01"
ref_rttm_path = f"{ROOT}/ref_sastre01.rttm"
lang_rttm_path = f"{ROOT}/lang_sastre01.rttm"
hyp_rttm_path = f"{ROOT}/pyannote/sastre01_pyannote.rttm"


# ---------------------------------------------

info = {
    "uri": uri,
    "root": ROOT,
    "ref_rttm": load_rttm(ref_rttm_path)[uri],
    "lang_rttm": load_rttm(lang_rttm_path)[uri],
    "hyp_rttm": load_rttm(hyp_rttm_path)[uri],
}


# --------------------FUNCTIONS--------------------
def perform_language_error_rates(info):  # ref and hyp need matching labels
    uri = info["uri"]
    ref = info["ref_rttm"]
    hyp = info["hyp_rttm"]
    lang = info["lang_rttm"]

    cs_metrics = CSDiarizationMetrics(
        reference=ref, hypothesis=hyp, language_annotation=lang, uri=uri
    )
    components = cs_metrics.compute_components()
    metric = cs_metrics.compute_metric(components)
    for k, v in metric.items():
        print(f"{k} = {v * 100:.3f}")


def perform_confusion_analysis(info):  # ref and hyp need matching labels
    uri = info["uri"]
    ref = info["ref_rttm"]
    hyp = info["hyp_rttm"]
    lang = info["lang_rttm"]

    cs_metrics = CSDiarizationMetrics(
        reference=ref, hypothesis=hyp, language_annotation=lang, uri=uri
    )
    confusion_tl = cs_metrics._get_confusion_timeline()
    confusion_ann = timeline_to_annotation(uri, confusion_tl, "CONF")
    with open(f"{info['root']}/conf_{info['uri']}.rttm", "w") as file:
        confusion_ann.write_rttm(file)


def perform_missed_analysis(info):  # ref and hyp need matching labels
    uri = info["uri"]
    ref = info["ref_rttm"]
    hyp = info["hyp_rttm"]
    lang = info["lang_rttm"]
    cs_metrics = CSDiarizationMetrics(
        reference=ref, hypothesis=hyp, language_annotation=lang, uri=uri
    )
    miss_tl = cs_metrics._get_missed_timeline()
    miss_ann = timeline_to_annotation(uri, miss_tl, "MISS")
    with open(f"{info['root']}/miss_{info['uri']}.rttm", "w") as file:
        miss_ann.write_rttm(file)


def plot_ref_vs_hyp(ref, hyp):
    plot_annotations([(ref, "Reference"), (hyp, "Hypothesis")])


def detailed_der(info):
    ref = info["ref_rttm"]
    hyp = info["hyp_rttm"]
    output = f'{info["root"]}/der_{info["uri"]}.txt'
    metric = DiarizationErrorRate(uriskip_overlap=True, collar=0.5)
    components = metric.compute_components(ref, hyp)

    with open(output, "w") as file:
        file.write(f"Missed Detection: {components['missed detection']:.1f}\n")
        file.write(f"False Alarm: {components['false alarm']:.1f}\n")
        file.write(f"Confusion: {components['confusion']:.1f}\n")
        der = metric(ref, hyp)
        file.write(f"Overall DER %: {der * 100:.1f}\n")

    print(f"DER details have been saved to {output}")



# --------------------ANALYSIS--------------------


if __name__ == "__main__":
    
    #detailed_der(info)

    perform_language_error_rates(info)
    perform_confusion_analysis(info)
    perform_missed_analysis(info)