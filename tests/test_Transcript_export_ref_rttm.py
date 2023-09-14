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


def read_file_content(file_path):
    with open(file_path, "r") as f:
        return f.read()


def test_export_ref_rttm():
    transcript = Transcript(uri="test")
    transcript[Segment(0, 1)] = ("A", "ENG", "Hi")
    transcript[Segment(1, 2)] = ("B", "SPA", "Hola")
    transcript[Segment(2, 3)] = ("A", "ENG", "How are you")
    transcript[Segment(3, 4)] = ("A", "ENG", "going?")
    result_file = transcript.export_ref_rttm(support=False, output_path='./test')
    expected_output_file = f"{TEST_FILES}/export_ref_no_support.rttm"

    try:
        assert read_file_content(result_file) == read_file_content(expected_output_file)
    finally:
        os.remove(result_file)

    transcript = Transcript(uri="test")
    transcript[Segment(0, 1)] = ("A", "ENG", "Hi")
    transcript[Segment(1, 2)] = ("B", "SPA", "Hola")
    transcript[Segment(2, 3)] = ("A", "ENG", "How are you")
    transcript[Segment(3, 4)] = ("A", "ENG", "going?")
    result_file = transcript.export_ref_rttm(support=True, output_path='./test')
    expected_output_file = f"{TEST_FILES}/export_ref_support.rttm"
    try:
        assert read_file_content(result_file) == read_file_content(expected_output_file)
    finally:
        os.remove(result_file)
