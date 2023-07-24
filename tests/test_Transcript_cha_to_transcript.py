import pytest
from pyannote.core import Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.transcript import cha_to_transcript, Transcript  # noqa: E402
from src.utilities import ROOT_DIR, get_uri_of_file # noqa: E402

def test_cha_to_transcript():
    test_file = f"{ROOT_DIR}/tests/test_files/test_sastre09.cha"
    uri = get_uri_of_file(test_file)
    expected_output = Transcript(uri=uri)
    expected_output[Segment(0.47, 2.107)] = ("ENG", "KAY", "! so")
    expected_output[Segment(0.471, 2.106)] = ("SPA", "KAY", "! sí@s hay@s un@s")
    expected_output[Segment(0.472, 2.105)] = ("ENG", "KAY", "! range")
    expected_output[Segment(0.473, 2.104)] = ("SPA", "KAY", "! ahí@s")
    expected_output[Segment(2.180, 2.490)] = ("ENG", "VAL", "mhm")
    expected_output[Segment(2.181, 4.321)] = ("SPA", "KAY", "_SPA donde los policías e practican")
    expected_output[Segment(4.293, 7.486)] = ("SPA", "KAY", "! y@s y@s la@s gente@s que@s están@s los@s")
    expected_output[Segment(4.294, 7.485)] = ("ENG", "KAY", "! trainees the police trainees")
    expected_output[Segment(7.387, 8.618)] = ("ENG", "KAY", "they do it every day")
    expected_output[Segment(8.575, 10.783)] = ("ENG", "KAY", "so when you come here dont be afraid if you hear it")
    expected_output[Segment(11.095, 12.193)] = ("ENG", "KAY", "because you know theyre practicing")
    expected_output[Segment(12.064, 14.786)] = ("ENG", "VAL", "yeah yeah they have to put these earphones")
    expected_output[Segment(14.900, 16.643)] = ("SPA", "VAL", "_SPA porque si no se puede quedar uno sordo")
    expected_output[Segment(16.433, 16.794)] = ("ENG", "KAY", "really")


    output = cha_to_transcript(test_file)

    assert output == expected_output
