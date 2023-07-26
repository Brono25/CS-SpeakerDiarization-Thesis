import pytest
from pyannote.core import Annotation, Segment
import sys
import re

# Always use CS-SpeakerDiarization-Thesis as root
root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

from src.transcript import Transcript  # noqa: E402


def test_get_language_annotation():
    extpected_output = Annotation(uri="test")
    extpected_output[Segment(0, 1)] = "ENG"

    input = Transcript(uri="test")
    input[Segment(0, 1)] = ("A", "ENG", "Text")
    result = input.get_language_annotation()

    assert extpected_output == result
    assert input != extpected_output
