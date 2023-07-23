import pytest
from pyannote.core import Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.transcript import Transcript  # noqa: E402


def test_transcript():
    a = Transcript()
    a[Segment(0, 1)] = ("A", "Hello world", "EN")

    text = a.get_text(Segment(0, 1))
    assert text == "Hello world"

    language = a.get_language(Segment(0, 1))
    assert language == "EN"
