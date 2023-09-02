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


def get_uri():
    filename = os.path.splitext(os.path.basename(sys.argv[1]))[0]
    match = re.search(r"_?([a-z]+[0-9]{1,2})_?", sys.argv[1])
    if not match:
        print(f"ERROR: couldn't extract uri from {filename}")
        sys.exit(1)
    uri = match.group(1)
    return uri



def create_ref_rttm(info):
    if not os.path.exists(info["transcript_file"]):
        print("File not found")
        return
    transcript = load_transcript_from_file(
        uri=info["uri"], file=info["transcript_file"]
    )
    transcript.export_ref_rttm(info["ref_rttm"])


def create_lang_rttm(info):
    if not os.path.exists(info["transcript_file"]):
        print("File not found")
        return
    transcript = load_transcript_from_file(
        uri=info["uri"], file=info["transcript_file"]
    )
    transcript.export_lang_rttm(info["lang_rttm"])


def get_root_dir():
    for file in sys.argv[1:]:
        if file != "None":
            root = os.path.dirname(file)
            return root

if __name__ == "__main__":

    ref_opt = bool(int(sys.argv[2]))
    lang_opt = bool(int(sys.argv[3]))
    uri = get_uri()
    root = get_root_dir()
    transcript_file = sys.argv[1]
    info = {
        "uri": uri,
        "root": root,
        "ref_rttm": f"{root}/ref_{uri}.rttm",
        "lang_rttm": f"{root}/lang_{uri}.rttm",
        "transcript_file": transcript_file,
    }


    if ref_opt:
        print("Creating reference rttm")
        create_ref_rttm(info)
    if lang_opt:
        print("Creating language rttm")
        create_lang_rttm(info)
