import os
import pytest
from pyannote.core import Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.functions.transcript import load_transcript_from_file, Transcript  # noqa: E402
from src.functions.utilities import TEST_FILES

@pytest.fixture
def expected_transcript():
    expected_output = Transcript(uri="sastre09")
    expected_output[Segment(0.47, 2.107)] = ("KAY", "ENG", "! so")
    expected_output[Segment(0.471, 2.106)] = ("KAY", "SPA", "! sí@s hay@s un@s")
    expected_output[Segment(0.472, 2.105)] = ("KAY", "ENG", "! range")
    expected_output[Segment(0.473, 2.104)] = ("KAY", "SPA", "! ahí@s")
    expected_output[Segment(2.180, 2.490)] = ("VAL", "ENG", "mhm")
    expected_output[Segment(2.181, 4.321)] = ("KAY", "SPA", "_SPA donde los policías e practican")
    expected_output[Segment(4.293, 7.486)] = ("KAY", "SPA", "! y@s y@s la@s gente@s que@s están@s los@s")
    expected_output[Segment(4.294, 7.485)] = ("KAY", "ENG", "! trainees the police trainees")
    expected_output[Segment(7.387, 8.618)] = ("KAY", "ENG", "they do it every day")
    expected_output[Segment(8.575, 10.783)] = ("KAY", "ENG", "so when you come here dont be afraid if you hear it")
    expected_output[Segment(11.095, 12.193)] = ("KAY", "ENG", "because you know theyre practicing")
    expected_output[Segment(12.064, 14.786)] = ("VAL", "ENG", "yeah yeah they have to put these earphones")
    expected_output[Segment(14.900, 16.643)] = ("VAL", "SPA", "_SPA porque si no se puede quedar uno sordo")
    expected_output[Segment(16.433, 16.794)] = ("KAY", "ENG", "really")

    return expected_output

def test_load_transcript_from_file(expected_transcript):
    file = f"{TEST_FILES}/test_sastre09.tr"
    transcript = load_transcript_from_file(file, 'sastre09')
    assert transcript == expected_transcript, "Loaded transcript does not match the expected transcript"
