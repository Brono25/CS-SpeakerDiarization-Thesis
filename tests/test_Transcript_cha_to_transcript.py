import pytest
from pyannote.core import Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.transcript import cha_to_transcript, Transcript  # noqa: E402
from src.utilities import root_dir, get_uri_of_file, debug_transcript_comparison # noqa: E402

def test_cha_to_transcript():
    test_file = f"{root_dir}/tests/test_files/test_sastre09.cha"
    uri = get_uri_of_file(test_file)
    print(f"uri = {uri}")
    expected_output = Transcript(uri=uri)
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

    output = cha_to_transcript(test_file)

    debug_transcript_comparison(output, expected_output)



    assert output == expected_output


test_cha_to_transcript()