import pytest
from pyannote.core import Annotation, Segment, Timeline

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.functions.cs_diarization_metrics import CSDiarizationMetrics  # noqa: E402

URI = "test bench"


def test_default_uem():
    ref = Annotation(uri=URI)
    ref[Segment(1, 11)] = "A"
    hyp = Annotation(uri=URI)
    hyp[Segment(0, 4)] = "A"
    hyp[Segment(3, 7)] = "B"
    hyp[Segment(7, 10)] = "A"

    answer = Timeline(uri=URI)
    answer.add(Segment(0, 11))
    test = CSDiarizationMetrics(uri=URI, reference=ref, hypothesis=hyp)
    uem = test._default_uem()

    assert uem.uri == ref.uri and answer == uem, "Test failed: _default_uem"
