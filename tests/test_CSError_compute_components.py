import pytest
from pyannote.core import Annotation, Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.functions.cs_diarization_metrics import CSDiarizationMetrics  # noqa: E402
URI = "test bench"


def test_compute_components():
    ref = Annotation(uri=URI)
    hyp = Annotation(uri=URI)
    lang_map = Annotation(uri=URI)

    # Confusion Errors
    ref[Segment(0, 5)] = "A"
    ref[Segment(0, 2)] = "B"
    hyp[Segment(0, 2)] = "A"
    hyp[Segment(2, 4)] = "B"
    hyp[Segment(4, 5)] = "A"
    lang_map[Segment(0, 2.5)] = "ENG"
    lang_map[Segment(0, 1)] = "ENG"
    lang_map[Segment(1, 2)] = "SPA"
    lang_map[Segment(2.5, 4.5)] = "SPA"
    lang_map[Segment(4.5, 5)] = "ENG"
    ref[Segment(5, 10)] = "B"
    hyp[Segment(5, 8)] = "B"
    hyp[Segment(8, 10)] = "A"
    lang_map[Segment(5, 8)] = "SPA"
    lang_map[Segment(8, 10)] = "ENG"

    # Miss Detection
    ref[Segment(10, 20)] = "A"
    ref[Segment(15, 16)] = "B"
    ref[Segment(19, 30)] = "B"
    hyp[Segment(10, 12)] = "A"
    hyp[Segment(18, 22)] = "A"
    hyp[Segment(25, 30)] = "B"
    lang_map[Segment(10, 13)] = "ENG"
    lang_map[Segment(13, 17)] = "SPA"
    lang_map[Segment(15, 16)] = "SPA"
    lang_map[Segment(15.5, 6)] = "ENG"
    lang_map[Segment(17, 20)] = "ENG"
    lang_map[Segment(19, 21)] = "SPA"
    lang_map[Segment(21, 26)] = "ENG"
    lang_map[Segment(26, 30)] = "SPA"

    answer = {
        "english_conf_error": 3.5,
        "english_total": 13,
        "spanish_conf_error": 2.5,
        "spanish_total": 13,
        "english_miss_error": 5,
        "spanish_miss_error": 3,
    }

    test = CSDiarizationMetrics(
        uri=URI, reference=ref, hypothesis=hyp, language_annotation=lang_map
    )
    result = test.compute_components()

    assert result == answer, "Test failed: compute_components"
