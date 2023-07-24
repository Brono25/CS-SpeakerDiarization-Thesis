import matplotlib.pylab as plt
import json
from pyannote.core import notebook
from pyannote.core import Annotation, Segment
from pathlib import Path
import sys

root_dir_name = "CS-SpeakerDiarization-Thesis"
root_dir = Path(__file__).parent.parent
if root_dir not in sys.path:
    sys.path.append(root_dir)



cha_files_dir = f"{root_dir}/cha_files"
transcription_files_dir = f"{root_dir}/transcription_files"
wav_files_dir = f"{root_dir}/wav_files"
ref_rttm_dir = f"{root_dir}/rttm_files/ref_rttm"
hyp_rttm_dir = f"{root_dir}/rttm_files/hyp_rttm"
lang_rttm_dir = f"{root_dir}/rttm_files/lang_rttm"
confusion_rttm_dir = f"{root_dir}/rttm_files/confusion_rttm"
missed_rttm_dir = f"{root_dir}/rttm_files/missed_rttm"
database_path = f"{root_dir}/src/database.json"



def get_uri_of_file(filename: str):
    with open(database_path, 'r') as f:  
        database = json.load(f)

    for key in database.keys():
        if key in filename:
            return key
    raise ValueError(f"No URI found in filename {filename}")

def get_primary_language_of_file(uri: str):
    with open(database_path, 'r') as f:  
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
    with open(filename, 'w') as f:
        json.dump(input_dict, f, indent=4)



def print_transcript_comparison(*transcripts: "Transcript"):  # noqa: F821
    iterators = [transcript.itersegments() for transcript in transcripts]
    for segment_group in zip(*iterators):
        for i, segment in enumerate(segment_group):
            label, text, lang = transcripts[i][segment]
            print(f"Transcript {i+1} - Segment: {segment}, Language: {lang} : {label} {text}")
            
