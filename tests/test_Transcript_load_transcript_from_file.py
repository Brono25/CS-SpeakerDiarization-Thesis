import os
import pytest
from pyannote.core import Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.transcript import load_transcript_from_file, Transcript  # noqa: E402
from src.utilities import TEST_FILES, get_uri_of_file, debug_transcript_comparison

@pytest.fixture
def expected_transcript():
    expected_output = Transcript(uri="sastre09")
    expected_output[Segment(0.47, 2.107)] = ("KAY", "! so", "ENG")
    expected_output[Segment(0.471, 2.106)] = ("KAY", "! sí@s hay@s un@s", "SPA")
    expected_output[Segment(0.472, 2.105)] = ("KAY", "! range", "ENG")
    expected_output[Segment(0.473, 2.104)] = ("KAY", "! ahí@s", "SPA")
    expected_output[Segment(2.180, 2.490)] = ("VAL", "mhm", "ENG")
    expected_output[Segment(2.181, 4.321)] = ("KAY", "_SPA donde los policías e practican", "SPA")
    expected_output[Segment(4.293, 7.486)] = ("KAY", "! y@s y@s la@s gente@s que@s están@s los@s", "SPA")
    expected_output[Segment(4.294, 7.485)] = ("KAY", "! trainees the police trainees", "ENG")
    expected_output[Segment(7.387, 8.618)] = ("KAY", "they do it every day", "ENG")
    expected_output[Segment(8.575, 10.783)] = ("KAY", "so when you come here dont be afraid if you hear it", "ENG")
    expected_output[Segment(11.095, 12.193)] = ("KAY", "because you know theyre practicing", "ENG")
    expected_output[Segment(12.064, 14.786)] = ("VAL", "yeah yeah they have to put these earphones", "ENG")
    expected_output[Segment(14.900, 16.643)] = ("VAL", "_SPA porque si no se puede quedar uno sordo", "SPA")
    expected_output[Segment(16.433, 16.794)] = ("KAY", "really", "ENG")
    return expected_output

def test_load_transcript_from_file(expected_transcript):
    file = f"{TEST_FILES}/test_sastre09.tr"
    transcript = load_transcript_from_file(file)
    assert transcript == expected_transcript, "Loaded transcript does not match the expected transcript"