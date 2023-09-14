import pytest
from pyannote.core import Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.functions.transcript import Transcript  # noqa: E402

def test_transcript():
    a = Transcript(uri="test")
    a[Segment(0, 1)] = ("A", "EN", "Hello world")
    seg, (label, language, text) = next(a.items())  

    assert a.uri == "test"
    assert label == 'A'
    assert text == "Hello world"
    assert language == "EN"
    assert seg == Segment(0, 1)
