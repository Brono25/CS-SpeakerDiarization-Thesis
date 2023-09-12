# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re
from pyannote.database.util import load_rttm
from pyannote.metrics.diarization import DiarizationErrorRate
import matplotlib.pyplot as plt
import json
import os
import time

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

from functions.cs_diarization_metrics import (
    CSDiarizationMetrics,
    timeline_to_annotation,
)
from functions.transcript import load_transcript_from_file
from functions.cs_dataset_metrics import DatasetMetrics


def get_uri():
    for file in sys.argv[1:]:
        if file != "None":
            file_path = file
            break
    else:
        return
    filename = os.path.splitext(os.path.basename(sys.argv[1]))[0]
    match = re.search(r"_?([a-z]+[0-9]{1,2})_?", file_path)
    if not match:
        print(f"ERROR: couldn't extract uri from {filename}")
        sys.exit(1)
    uri = match.group(1)
    return uri


def get_root_dir():
    for file in sys.argv[1:]:
        if file != "None":
            root = os.path.dirname(file)
            return root


def load_info_from_args(ref, hyp, lang, transcript):
    root = get_root_dir()
    uri = get_uri()
    if ref != "None":
        ref = load_rttm(ref)[uri]
    else:
        ref = None
    if hyp != "None":
        hyp = load_rttm(hyp)[uri]
    else:
        hyp = None
    if lang != "None":
        lang = load_rttm(lang)[uri]
    else:
        lang = None
    if transcript != "None":
        transcript = load_transcript_from_file(uri=uri, file=transcript)
    else:
        transcript = None
    info = {
        "uri": uri,
        "root": root,
        "ref": ref,
        "hyp": hyp,
        "lang": lang,
        "transcript": transcript,
    }
    return info


# --------------------SETUP--------------------


def get_output_filename(root, uri, suffix):
    output_path = f"{root}/der_{uri}{suffix}"
    if os.path.exists(output_path):
        timestamp = time.strftime("%Y%m%d%H%M%S")
        output_path = f"{root}/der_{uri}_{timestamp}{suffix}"
    return output_path


def detailed_der(info):
    ref = info["ref"]
    hyp = info["hyp"]
    output = get_output_filename(info["root"], info["uri"], ".json")

    metric = DiarizationErrorRate(skip_overlap=True, collar=0.5)
    components = metric.compute_components(ref, hyp)
    der = metric(ref, hyp)

    der_details = {
        "diarization": {
            "der_pc": round(der * 100, 1),
            "confusion_sec": round(components["confusion"], 1),
            "missed_sec": round(components["missed detection"], 1),
            "false_sec": round(components["false alarm"], 1),
        }
    }

    with open(output, "w") as file:
        file.write(json.dumps(der_details, indent=4))

    print(f"DER details saved to {output}")


def perform_confusion_analysis(info):
    uri = info["uri"]
    ref = info["ref"]
    hyp = info["hyp"]
    lang = info["lang"]

    cs_metrics = CSDiarizationMetrics(
        reference=ref, hypothesis=hyp, language_annotation=lang, uri=uri
    )
    confusion_tl = cs_metrics._get_confusion_timeline()
    confusion_ann = timeline_to_annotation(uri, confusion_tl, "CONF")
    with open(f"{info['root']}/conf_{info['uri']}.rttm", "w") as file:
        confusion_ann.write_rttm(file)


def perform_missed_analysis(info):
    uri = info["uri"]
    ref = info["ref"]
    hyp = info["hyp"]
    lang = info["lang"]
    cs_metrics = CSDiarizationMetrics(
        reference=ref, hypothesis=hyp, language_annotation=lang, uri=uri
    )
    miss_tl = cs_metrics._get_missed_timeline()
    miss_ann = timeline_to_annotation(uri, miss_tl, "MISS")
    with open(f"{info['root']}/miss_{info['uri']}.rttm", "w") as file:
        miss_ann.write_rttm(file)


def perform_language_error_rates(info):
    uri = info["uri"]
    ref = info["ref"]
    hyp = info["hyp"]
    lang = info["lang"]

    cs_metrics = CSDiarizationMetrics(
        reference=ref, hypothesis=hyp, language_annotation=lang, uri=uri
    )
    components = cs_metrics.compute_components()
    metric = cs_metrics.compute_metric(components)

    # Convert metric to percentages and round to 3 decimal places
    metric_percentage = {k: round(v * 100, 1) for k, v in metric.items()}

    # Predefined keys for both languages
    error_rates = {
        "error_rates": {
            "english_conf_error_rate": None,
            "spanish_conf_error_rate": None,
            "english_miss_error_rate": None,
            "spanish_miss_error_rate": None,
            "english_error_rate": None,
            "spanish_error_rate": None,
        }
    }

    # Populate error_rates with values from metric_percentage
    for key in error_rates["error_rates"].keys():
        error_rates["error_rates"][key] = metric_percentage.get(key, None)

    with open(f"{info['root']}/eer_{info['uri']}.json", "w") as file:
        json.dump(error_rates, file, indent=4)


def get_dataset_metrics(info):
    tr = info["transcript"]
    metrics = DatasetMetrics(transcript=tr)

    m_index = metrics.m_index()
    i_index = metrics.i_index()
    burstiness = metrics.burstiness()
    output = f'{info["root"]}/metric_{info["uri"]}.json'

    with open(output, "w") as file:
        metric = {
            "cs_metrics": {
                "i-index": float(f"{i_index:.3f}"),
                "m-index": float(f"{m_index:.3f}"),
                "burstiness": float(f"{burstiness:.3f}"),
            }
        }
        file.write(json.dumps(metric, indent=4))
    print(f"Metrics have been saved to {output}")


if __name__ == "__main__":
    info = load_info_from_args(
        ref=sys.argv[1], hyp=sys.argv[2], lang=sys.argv[3], transcript=sys.argv[4]
    )
    if len(sys.argv) != 5:
        print("Invalid arguments")
        sys.exit(1)

    if info["ref"] and info["hyp"]:
        detailed_der(info)
        if info["lang"]:
            perform_missed_analysis(info)
            perform_confusion_analysis(info)
            perform_language_error_rates(info)

    if info["transcript"]:
        get_dataset_metrics(info)
