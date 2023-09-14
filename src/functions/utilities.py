import matplotlib.pylab as plt
import json
from pyannote.core import notebook
from pyannote.core import Annotation, Segment
from pathlib import Path
import sys

ROOT_DIR_NAME = "CS-SpeakerDiarization-Thesis"
ROOT_DIR = Path(__file__).parent.parent.parent
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

CHA_FILES_DIR = f"{ROOT_DIR}/cha_files"
TRANSCRIPTION_FILES_DIR = f"{ROOT_DIR}/transcription_files"
WAV_FILES_DIR = f"{ROOT_DIR}/wav_files"
REF_RTTM_DIR = f"{ROOT_DIR}/rttm_files/ref_rttm"
HYP_RTTM_DIR = f"{ROOT_DIR}/rttm_files/hyp_rttm"
LANG_RTTM_DIR = f"{ROOT_DIR}/rttm_files/lang_rttm"
CONFUSION_RTTM_DIR = f"{ROOT_DIR}/rttm_files/confusion_rttm"
MISSED_RTTM_DIR = f"{ROOT_DIR}/rttm_files/missed_rttm"
DATABASE_PATH = f"{ROOT_DIR}/src/data/database.json"
TEST_FILES = f"{ROOT_DIR}/tests/test_files"
LOG_FILES = f"{ROOT_DIR}/logs"

HERRING_LIST = [
    "herring06",
    "herring07",
    "herring08",
    "herring09",
    "herring10",
    "herring13",
    "herring15",
    "herring16",
    "herring17",
]
SASTRE_LIST = [
    "sastre01",
    "sastre02",
    "sastre03",
    "sastre04",
    "sastre05",
    "sastre06",
    "sastre07",
    "sastre08",
    "sastre09",
    "sastre10",
    "sastre11",
    "sastre12",
    "sastre13",
]
ZELEDON_LIST = [
    "zeledon01",
    "zeledon02",
    "zeledon03",
    "zeledon04",
    "zeledon05",
    "zeledon06",
    "zeledon07",
    "zeledon08",
    "zeledon09",
    "zeledon11",
    "zeledon13",
    "zeledon14",
]


def get_uri_list():
    with open(DATABASE_PATH, "r") as f:
        database = json.load(f)

    uri_list = [x for x in list(database.keys()) if "tmp" not in x]
    return uri_list


def get_uri_of_file(filename: str):
    with open(DATABASE_PATH, "r") as f:
        database = json.load(f)
    print(ROOT_DIR)
    for key in database.keys():
        if key in filename:
            return key
    raise ValueError(f"No URI found in filename {filename}")


def get_primary_language_of_file(uri: str):
    with open(DATABASE_PATH, "r") as f:
        database = json.load(f)

    if uri not in database:
        raise KeyError(f"URI '{uri}' not found in database")
    return database[uri]["primary_language"]


def plot_annotations(annotations_with_legends):
    num_subplots = len(annotations_with_legends)
    fig, axs = plt.subplots(num_subplots, 1, figsize=(5, 3 * num_subplots), sharex=True)
    if num_subplots == 1:
        axs = [axs]

    for idx, (annotation, legend) in enumerate(annotations_with_legends):
        notebook.plot_annotation(annotation, ax=axs[idx])
        axs[idx].set_title(legend)


def plot_timelines(timelines_with_legends):
    num_subplots = len(timelines_with_legends)
    fig, axs = plt.subplots(num_subplots, 1, figsize=(5, 3 * num_subplots), sharex=True)

    if num_subplots == 1:
        axs = [axs]

    for idx, (timeline, legend) in enumerate(timelines_with_legends):
        notebook.plot_timeline(timeline, ax=axs[idx])
        axs[idx].set_title(legend)


def combine_annotations(*annotations):
    combined_annotation = Annotation()
    offset = 0

    for annotation in annotations:
        for segment, track in annotation.itertracks():
            new_segment = Segment(segment.start + offset, segment.end + offset)
            combined_annotation[new_segment] = annotation[segment, track]

        offset += annotation.get_timeline().extent().duration

    return combined_annotation


def save_dict_to_json(input_dict, filename):
    with open(filename, "w") as f:
        json.dump(input_dict, f, indent=4)


def debug_transcript_comparison(*transcripts: "Transcript"):  # noqa: F821
    """
    Given one or more transcripts, this function iterates over each transcript segment
    and prints them line by line in parallel. It also checks if each label, utterance,
    and language are equal across all transcripts.

    This function is intended for debugging purposes, where comparing transcripts side by
    side can help identify discrepancies or anomalies.

    Each printed line includes the transcript number, segment details (start and end time),
    language, speaker label, and the spoken text.

    Parameters
    ----------
    *transcripts : "Transcript"
        Variable number of Transcript objects.

    Examples
    --------
    >>> debug_transcript_comparison(transcript1, transcript2)
    Transcript 1 - Segment: [ 00:00:00.470 -->  00:00:02.107], Language: ENG : KAY Hello
    Transcript 2 - Segment: [ 00:00:00.470 -->  00:00:02.107], Language: ENG : KAY Hello
    """
    for i, transcript in enumerate(transcripts):
        print(f"Transcript {i+1} - URI: {transcript.uri}")

    iterators = [transcript.itersegments() for transcript in transcripts]
    for segment_group in zip(*iterators):
        labels, langs, texts = [], [], []
        for i, segment in enumerate(segment_group):
            label, lang, text = transcripts[i][segment]
            labels.append(label)
            texts.append(text)
            langs.append(lang)
            print(
                f"Transcript {i+1} - Segment: {segment} = ({label} : {lang} : {text})"
            )

        if len(set(labels)) > 1:
            print(f"Discrepancy detected in labels: {labels}")
        if len(set(texts)) > 1:
            print(f"Discrepancy detected in utterances: {texts}")
        if len(set(langs)) > 1:
            print(f"Discrepancy detected in languages: {langs}")
