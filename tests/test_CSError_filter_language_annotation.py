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


def test_filter_language_annotation():
    test = CSDiarizationMetrics(uri=URI)
    language_annotation = Annotation(uri=URI)
    language_annotation[Segment(0, 2)] = "ENG"
    language_annotation[Segment(3, 5)] = "SPA"
    language_annotation[Segment(3.5, 6)] = "ENG"
    spanish = test._filter_language_annotation(language_annotation, "SPA")
    english = test._filter_language_annotation(language_annotation, "ENG")

    eng_answer = Annotation(uri=language_annotation.uri)
    eng_answer[Segment(0, 2)] = "ENG"
    eng_answer[Segment(3.5, 6)] = "ENG"
    spa_answer = Annotation(uri=language_annotation.uri)
    spa_answer[Segment(3, 5)] = "SPA"

    assert (
        isinstance(english, Annotation)
        and english == eng_answer
        and spanish == spa_answer
        and language_annotation.uri == english.uri
    ), "Test failed: _filter_language_annotation"
