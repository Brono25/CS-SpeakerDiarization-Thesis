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


class TestLanguageMetric:
    def test_compute_miss_components(self):
        ref = Annotation(uri=URI)
        ref[Segment(0, 10)] = "A"
        ref[Segment(5, 6)] = "B"
        ref[Segment(9, 20)] = "B"
        hyp = Annotation(uri=URI)
        hyp[Segment(0, 2)] = "A"
        hyp[Segment(8, 12)] = "A"
        hyp[Segment(15, 20)] = "B"
        language_annotation = Annotation(uri=URI)
        language_annotation[Segment(0, 3)] = "ENG"
        language_annotation[Segment(3, 7)] = "SPA"
        language_annotation[Segment(5, 5.5)] = "SPA"
        language_annotation[Segment(5.5, 6)] = "ENG"
        language_annotation[Segment(7, 10)] = "ENG"
        language_annotation[Segment(9, 11)] = "SPA"
        language_annotation[Segment(11, 16)] = "ENG"
        language_annotation[Segment(16, 20)] = "SPA"

        answer = {
            "english_miss_error": 5,
            "english_total": 10,
            "spanish_miss_error": 3,
            "spanish_total": 8,
        }
        test = CSDiarizationMetrics(
            uri=URI, reference=ref, hypothesis=hyp, language_annotation=language_annotation
        )
        result = test.compute_miss_components()

        assert result == answer, "FAIL: compute_miss_components"
