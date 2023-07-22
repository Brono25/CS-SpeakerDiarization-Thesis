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


class TestLanguageMetric:
    def test_language_confusion_annotation(self):
        ref = Annotation(uri=URI)
        ref[Segment(0, 10)] = "A"
        ref[Segment(9, 11)] = "B"
        hyp = Annotation(uri=URI)
        hyp[Segment(0, 4)] = "A"
        hyp[Segment(3, 8)] = "B"
        hyp[Segment(8, 11)] = "A"
        language_annotation = Annotation(uri=URI)
        language_annotation[Segment(0, 4)] = "ENG"
        language_annotation[Segment(4, 7.5)] = "SPA"
        language_annotation[Segment(7.5, 11)] = "ENG"

        test = LanguageMetric(
            uri=URI,
            reference=ref,
            hypothesis=hyp,
            language_annotation=language_annotation,
        )
        result = test.language_confusion_annotation()

        answer = Annotation(uri=URI)
        answer[Segment(4, 7.5)] = "SPA"
        answer[Segment(7.5, 8)] = "ENG"
        answer[Segment(10, 11)] = "ENG"

        assert isinstance(result, Annotation), "Result is not an Annotation instance."
        assert result == answer, "Mismatch in Annotation."
        assert result.uri == ref.uri, "URI mismatch."
