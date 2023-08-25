import sys
import re
import os

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

from functions.transcript import Transcript, load_transcript_from_file
from functions.cha_conversion import (
    convert_cha_to_transcript_str_format,
    reduce_transcript,
    write_transcript_format_to_file,
)
from functions.cs_dataset_metrics import DatasetMetrics

# --------------------SETUP--------------------
ROOT = "/Users/brono/GitHub/cs-dataset/english/sastre13"
uri = "sastre13"
prim_lang = "ENG"
# ---------------------------------------------

info = {
    "uri": uri,
    "root": ROOT,
    "cha_file": f"{ROOT}/other_files/{uri}.cha",
    "output_transcript": f"{ROOT}/{uri}.tr",
    "output_reduced_tr": f"{ROOT}/reduced_{uri}.tr",
    "prim_lang": prim_lang,
    "ref_rttm": f"{ROOT}/ref_{uri}.rttm",
    "lang_rttm": f"{ROOT}/lang_{uri}.rttm",
    "transcript_file": f"{ROOT}/{uri}.tr",
}


def convert_cha_to_transcript(info):
    transcript = convert_cha_to_transcript_str_format(
        uri=info["uri"], cha_file=info["cha_file"], prim_lang=info["prim_lang"]
    )
    write_transcript_format_to_file(
        trancript=transcript, output=f"{info['root']}/unreduced_transcript.tr"
    )
    reduced_tr = reduce_transcript(transcript, support=0.25)
    write_transcript_format_to_file(
        trancript=reduced_tr, output=info["output_transcript"]
    )


def create_rttm_files(info):
    if not os.path.exists(info["transcript_file"]):
        print("File not found")
        return
    transcript = load_transcript_from_file(
        uri=info["uri"], file=info["transcript_file"]
    )
    transcript.export_ref_rttm(info["ref_rttm"])
    transcript.export_lang_rttm(info["lang_rttm"])


def get_dataset_metrics(info):
    tr = load_transcript_from_file(uri=info["uri"], file=info["transcript_file"])
    metrics = DatasetMetrics(transcript=tr)

    m_index = metrics.m_index()
    i_index = metrics.i_index()
    burstiness = metrics.burstiness()

    metrics_file_path = os.path.join(info["root"], f"{info['uri']}_metrics.txt")

    with open(metrics_file_path, "w") as file:
        file.write(f"M-Index: {m_index:.3f}\n")
        file.write(f"I-Index: {i_index:.3f}\n")
        file.write(f"Burstiness: {burstiness:.3f}\n")

    print(f"Metrics have been saved to {metrics_file_path}")


if __name__ == "__main__":
    #convert_cha_to_transcript(info)
    #create_rttm_files(info)
    get_dataset_metrics(info)
