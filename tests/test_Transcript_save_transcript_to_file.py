import os
import pytest
from pyannote.core import Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)


# local imports
from src.transcript import save_transcript_to_file, Transcript
from src.utilities import ROOT_DIR, get_uri_of_file

@pytest.fixture
def sample_transcript():
    uri = "test_sample"
    transcript = Transcript(uri=uri)
    transcript[Segment(0.47, 2.107)] = ("KAY", "ENG", "! so")
    transcript[Segment(0.471, 2.106)] = ("KAY", "SPA", "! sí@s hay@s un@s")
    transcript[Segment(0.472, 2.105)] = ("KAY", "ENG", "! range")
    transcript[Segment(0.473, 2.104)] = ("KAY", "SPA", "! ahí@s")
    transcript[Segment(2.180, 2.490)] = ("VAL", "ENG", "mhm")
    transcript[Segment(2.181, 4.321)] = ("KAY", "SPA", "_SPA donde los policías e practican")
    transcript[Segment(4.293, 7.486)] = ("KAY", "SPA", "! y@s y@s la@s gente@s que@s están@s los@s")
    transcript[Segment(4.294, 7.485)] = ("KAY", "ENG", "! trainees the police trainees")
    transcript[Segment(7.387, 8.618)] = ("KAY", "ENG", "they do it every day")
    transcript[Segment(8.575, 10.783)] = ("KAY", "ENG", "so when you come here dont be afraid if you hear it")
    transcript[Segment(11.095, 12.193)] = ("KAY", "ENG", "because you know theyre practicing")
    transcript[Segment(12.064, 14.786)] = ("VAL", "ENG", "yeah yeah they have to put these earphones")
    transcript[Segment(14.900, 16.643)] = ("VAL", "SPA", "_SPA porque si no se puede quedar uno sordo")
    transcript[Segment(16.433, 16.794)] = ("KAY", "ENG", "really")

    return transcript

def test_save_transcript_to_file(sample_transcript):
    output_file = save_transcript_to_file(sample_transcript)
    
    # path to expected output
    expected_output_file = f"{ROOT_DIR}/tests/test_files/test_sastre09.tr"

    assert os.path.exists(output_file), "Output file was not created"
    
    with open(output_file, 'r') as file:
        output_content = file.readlines()
    
    with open(expected_output_file, 'r') as file:
        expected_content = file.readlines()
    
    assert output_content == expected_content, "Output content does not match the expected content"
    #os.remove(output_file)











