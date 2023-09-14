import pytest
from pyannote.core import Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

#local import
from src.functions.transcript import Transcript  # noqa: E402

def test_getitem():
    t = Transcript(uri='test')
    t[Segment(0, 1)] = ("A", "Hello World!", "ENG")
    t[Segment(1, 2)] = ("B", "Hola mundo", "SPA")

    assert t[Segment(0, 1)] == ("A", "Hello World!", "ENG")
    assert t[Segment(1, 2)] == ("B", "Hola mundo", "SPA")

    # Test a segment not in the transcript
    with pytest.raises(KeyError):
        t[Segment(2, 3)]

