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


def test_get_confusion_timeline():
    ref = Annotation(uri=URI)
    ref[Segment(0, 10)] = "A"
    ref[Segment(9, 11)] = "B"
    hyp = Annotation(uri=URI)
    hyp[Segment(0, 4)] = "A"
    hyp[Segment(3, 7)] = "C"
    hyp[Segment(7, 11)] = "A"

    test = CSError(uri=URI, reference=ref, hypothesis=hyp)
    answer = Timeline(uri=URI)
    answer.add(Segment(4, 7))
    answer.add(Segment(10, 11))
    result = test._get_confusion_timeline()

    assert (
        ref.uri == result.uri and answer == result
    ), "Test failed: _get_confusion_timeline"
