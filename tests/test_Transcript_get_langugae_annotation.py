import pytest
from pyannote.core import Annotation, Segment
import sys
import re

# Always use CS-SpeakerDiarization-Thesis as root
root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

from src.functions.transcript import Transcript  # noqa: E402


def test_get_language_annotation():
    expected_output = Annotation(uri="test")
    expected_output[Segment(0, 1)] = "ENG"

    input = Transcript(uri="test")
    input[Segment(0, 1)] = ("A", "ENG", "Text")
    result = input.get_language_annotation()

    for track in input.itertracks(yield_label=True):
        print(track)

    for track in expected_output.itertracks(yield_label=True):
        print(track)

    assert isinstance(result, Annotation)

    assert result == expected_output
    assert input != expected_output
