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
    def test_language_missed_annotation(self):
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
        test = CSDiarizationMetrics(
            uri=URI,
            reference=ref,
            hypothesis=hyp,
            language_annotation=language_annotation,
        )
        result = test.language_missed_annotation()

        answer = Annotation(uri=URI)
        answer[Segment(2, 3)] = "ENG"
        answer[Segment(3, 5)] = "SPA"
        answer[Segment(6, 7)] = "SPA"
        answer[Segment(7, 8)] = "ENG"
        answer[Segment(12, 15)] = "ENG"

        assert isinstance(result, Annotation), "Result is not an Annotation instance."
        assert result == answer, "Mismatch in Annotation."
        assert result.uri == ref.uri, "URI mismatch."
