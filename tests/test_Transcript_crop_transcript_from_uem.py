import os
import pytest
from pyannote.core import Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.functions.transcript import Transcript  # noqa: E402
from src.functions.utilities import TEST_FILES  # noqa: E402


def build_transcript(input_array):
    tr = Transcript(uri="test")
    for entry in input_array:
        start, end, label, lang, text = entry
        tr[Segment(start, end)] = (label, lang, text)
    return tr


def compare_transcripts(tr1, tr2):
    if len(tr1.transcript) != len(tr2.transcript):
        return False
    for (a1, a2, a3, a4, a5), (b1, b2, b3, b4, b5) in zip(tr1.itertr(), tr2.itertr()):
        assert a1 == b1
        assert a2 == b2
        assert a3 == b3
        assert a4 == b4
        assert a5 == b5


def test_simple_overlap():
    input = [
        [0, 10, "A", "ENG", "Hello"],
        [5, 15, "B", "ENG", "World"],
    ]
    expected_output_list = [
        [0, 5, "A", "ENG", "Hello"],
        [10, 15, "B", "ENG", "World"],
    ]
    transcript = build_transcript(input)
    uem = transcript.get_transcript_speaker_overlap_timeline()
    expected_output = build_transcript(expected_output_list)
    result = transcript.crop_transcript_from_uem(uem)
    compare_transcripts(expected_output, result)


def test_simple_overlap_complete_covered():
    input = [
        [0, 10, "A", "ENG", "Hello"],
        [5, 8, "B", "ENG", "World"],
    ]
    expected_output_list = [
        [0, 5, "A", "ENG", "Hello"],
        [8, 10, "A", "ENG", "Hello"],
    ]
    transcript = build_transcript(input)
    uem = transcript.get_transcript_speaker_overlap_timeline()
    expected_output = build_transcript(expected_output_list)
    result = transcript.crop_transcript_from_uem(uem)
    compare_transcripts(expected_output, result)


def test_stacking_overlaps():
    input = [
        [0, 10, "A", "ENG", "Hello"],
        [2, 8, "B", "ENG", "World"],
        [4, 6, "C", "ENG", "World"],
    ]
    expected_output_list = [
        [0, 4, "A", "ENG", "Hello"],
        [2, 4, "B", "ENG", "World"],
        [6, 8, "B", "ENG", "World"],
        [6, 10, "A", "ENG", "Hello"],
    ]
    transcript = build_transcript(input)
    uem = transcript.get_transcript_speaker_overlap_timeline()
    expected_output = build_transcript(expected_output_list)
    result = transcript.crop_transcript_from_uem(uem)
    compare_transcripts(expected_output, result)


def test_change_language():
    input = [
        [0, 10, "A", "ENG", "Hello"],
        [10, 15, "A", "SPA", "Hola"],
        [5, 11, "B", "ENG", "World"],
    ]
    expected_output_list = [
        [0, 5, "A", "ENG", "Hello"],
        [11, 15, "A", "SPA", "Hola"],
    ]
    transcript = build_transcript(input)
    uem = transcript.get_transcript_speaker_overlap_timeline()
    expected_output = build_transcript(expected_output_list)
    result = transcript.crop_transcript_from_uem(uem)
    compare_transcripts(expected_output, result)



def test_change_language2():
    input = [
        [0, 10, "A", "ENG", "Hello"],
        [12, 15, "A", "SPA", "Hola"],
        [5, 11, "B", "ENG", "World"],
    ]
    expected_output_list = [
        [0, 5, "A", "ENG", "Hello"],
        [10, 11, "B", "ENG", "World"],
        [12, 15, "A", "SPA", "Hola"],
    ]
    transcript = build_transcript(input)
    uem = transcript.get_transcript_speaker_overlap_timeline()
    expected_output = build_transcript(expected_output_list)
    result = transcript.crop_transcript_from_uem(uem)
    compare_transcripts(expected_output, result)