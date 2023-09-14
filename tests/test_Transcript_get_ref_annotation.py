import pytest
from pyannote.core import Annotation, Segment
import sys
import re

# Always use CS-SpeakerDiarization-Thesis as root
root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

from src.functions.transcript import Transcript  # noqa: E402

#The 'A' is needed as when support() is called in pyannote it defaults to track = 'A'
def test_get_ref_annotation():
    extpected_output = Annotation(uri="test")
    extpected_output[Segment(0, 1), 'A'] = "Tom" 

    input = Transcript(uri="test")
    input[Segment(0, 1)] = ("Tom", "ENG", "Text")
    result = input.get_ref_annotation(support=True)

    assert extpected_output == result
    assert input != extpected_output
