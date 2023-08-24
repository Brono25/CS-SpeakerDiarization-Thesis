# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re
import os

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from functions.transcript import (  # noqa: E402
    Transcript,
    convert_cha_to_transcript,
    reduce_transcript,
    load_transcript_from_file
)

ROOT = "/Users/brono/GitHub/cs-dataset/code-switched/sastre01"
uri = "sastre01"
prim_lang = "SPA"


"""
For converting CHA files to transcripts
"""


info = {
    "uri": uri,
    "root": ROOT,
    "cha_file": f"{ROOT}/{uri}.cha",
    "output_transcript": f"{ROOT}/{uri}.tr",
    "output_reduced_tr": f"{ROOT}/reduced_{uri}.tr",
    "prim_lang": prim_lang,
    "ref_rttm": f"{ROOT}/ref_{uri}.rttm",
    "lang_rttm": f"{ROOT}/lang_{uri}.rttm",
    "transcript_file": f"{ROOT}/{uri}.tr",
}


def convert_cha_to_transcript(info):
    transcript = convert_cha_to_transcript(
        uri=info["uri"], cha_file=info["cha_file"], prim_lang=info["prim_lang"]
    )
    transcript.save_transcript_to_file(info["output_transcript"])
    transcript = reduce_transcript(transcript, support=0.25)
    transcript.save_transcript_to_file(info["output_reduced_tr"])


def create_rttm_files(info):

    if not os.path.exists(info["transcript_file"]):
        print("File not found")
        return
    transcript = load_transcript_from_file(uri=info["uri"], file=info["transcript_file"])
    transcript.export_ref_rttm(info["ref_rttm"])
    transcript.export_lang_rttm(info["lang_rttm"])


if __name__ == "__main__":

    #convert_cha_to_transcript(info)
    create_rttm_files(info)