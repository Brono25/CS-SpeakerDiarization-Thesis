# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re
from pyannote.database.util import load_rttm
from pyannote.metrics.diarization import DiarizationErrorRate
import matplotlib.pyplot as plt
import json 

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)
from functions.utilities import plot_annotations

from functions.cs_diarization_metrics import (
    CSDiarizationMetrics,
    timeline_to_annotation,
)

# --------------------SETUP--------------------
ROOT = "/Users/brono/GitHub/cs-dataset/code-switched/herring13"
uri = "herring13"
ref_rttm_path = "/Users/brono/GitHub/cs-dataset/code-switched/herring13/ref_herring13.rttm"
lang_rttm_path = "/Users/brono/GitHub/cs-dataset/code-switched/herring13/lang_herring13.rttm"
hyp_rttm_path = "/Users/brono/GitHub/cs-dataset/code-switched/herring13/pyannote/herring13_pyannote.rttm"


# ---------------------------------------------

info = {
    "uri": uri,
    "root": ROOT,
    "ref_rttm": load_rttm(ref_rttm_path)[uri],
    "lang_rttm": load_rttm(lang_rttm_path)[uri] if lang_rttm_path else None,
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
    output = f'{info["root"]}/der_{info["uri"]}.json'
    metric = DiarizationErrorRate(skip_overlap=True, collar=0.5)
    components = metric.compute_components(ref, hyp)
    der = metric(ref, hyp)

    der_details = {
        "diarization": {
            "der_pc": round(der * 100, 1),
            "confusion_sec": round(components['confusion'], 1),
            "missed_sec": round(components['missed detection'], 1),
            "false_sec": round(components['false alarm'], 1)
        }
    }

    with open(output, "w") as file:
        file.write(json.dumps(der_details, indent=4))

    print(f"DER details have been saved to {output}")





# --------------------ANALYSIS--------------------


if __name__ == "__main__":
    
    detailed_der(info)

    perform_language_error_rates(info)
    perform_confusion_analysis(info)
    perform_missed_analysis(info)