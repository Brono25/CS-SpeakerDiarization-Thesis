import pytest
from pyannote.core import Annotation, Segment, Timeline

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.cs_error import CSError  # noqa: E402

URI = "test bench"


def test_get_missed_timeline():
    ref = Annotation(uri=URI)
    ref[Segment(0, 3)] = "A"
    ref[Segment(3, 6)] = "B"
    ref[Segment(6, 10)] = "A"

    hyp = Annotation(uri=URI)
    hyp[Segment(0, 4)] = "A"
    hyp[Segment(7, 11)] = "A"

    test = CSError(uri=URI, reference=ref, hypothesis=hyp)
    answer = Timeline(uri=URI)
    answer.add(Segment(4, 7))
    result = test._get_missed_timeline()

    assert (
        ref.uri == result.uri and answer == result
    ), "Test failed: _get_missed_timeline"
