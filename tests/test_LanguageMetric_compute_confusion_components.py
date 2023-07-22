import pytest
from pyannote.core import Annotation, Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.metrics.language_metric import LanguageMetric  # noqa: E402

URI = "test bench"


def test_compute_confusion_components():
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

    answer = {
        "english_conf_error": 2.5,
        "english_total": 3,
        "spanish_conf_error": 1.5,
        "spanish_total": 5,
    }

    test = LanguageMetric(
        uri=URI, reference=ref, hypothesis=hyp, language_annotation=lang_map
    )
    result = test.compute_confusion_components()

    assert result == answer, "Test failed: compute_confusion_components"
