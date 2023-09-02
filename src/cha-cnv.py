import sys
import re
import os
import json

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

from functions.cha_conversion import (
    convert_cha_to_transcript_str_format,
    reduce_transcript,
    write_transcript_format_to_file,
)

DATABASE = "/Users/brono/GitHub/CS-SpeakerDiarization-Thesis/src/data/database.json"


def get_uri():
    for file in sys.argv[1:]:
        if file != "None":
            file_path = file
            break
    else:
        return
    filename = os.path.splitext(os.path.basename(sys.argv[1]))[0]
    match = re.search(r"_?([a-z]+[0-9]{1,2})_?", file_path)
    print(filename)
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


def get_prim_lang(uri):
    with open(DATABASE, "r") as f:
        data = json.load(f)
        prim_lang = data[uri]["primary_language"]
        return prim_lang


def convert_cha_to_transcript(info):
    transcript = convert_cha_to_transcript_str_format(
        uri=info["uri"], cha_file=info["cha_file"], prim_lang=info["prim_lang"]
    )
    write_transcript_format_to_file(
        trancript=transcript, output=f"{info['root']}/unreduced_{info['uri']}.tr"
    )
    print(f"saving {info['root']}/unreduced_{info['uri']}.tr")
    reduced_tr = reduce_transcript(transcript, support=0.25)
    write_transcript_format_to_file(
        trancript=reduced_tr, output=f"{info['root']}/reduced_{info['uri']}.tr"
    )
    print(f"saving {info['root']}/reduced_{info['uri']}.tr")


if __name__ == "__main__":
    file_path = sys.argv[1]

    if not os.path.isfile(file_path) or not file_path.endswith(".cha"):
        print(f"Error: invalid file {file_path}")
        sys.exit(1)

    uri = get_uri()
    root = get_root_dir()
    prim_lang = get_prim_lang(uri)
    cha_file = sys.argv[1]

    info = {
        "uri": uri,
        "root": root,
        "cha_file": cha_file,
        "prim_lang": prim_lang,
    }
    convert_cha_to_transcript(info)
