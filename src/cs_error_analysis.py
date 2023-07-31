from pyannote.core import Annotation, Timeline, Segment
from pyannote.metrics.base import BaseMetric
from pyannote.metrics.errors.identification import IdentificationErrorAnalysis
import copy


class AnalysisSegment:
    def __init__(
        self, pre_lang: Segment, error_segment: Segment, post_segment: Segment
    ):
        self


def compute_switching_errors(
    error_annotation: Annotation,
    language_annotation: Annotation,
    label_annotation: Annotation,
):
    analysis_results = {
        "error_duration": None,
        "error_speaker_label": None,
        "error_language": None,
        "pre_speaker_label": None,
        "pre_language": None,
        "post_speaker_label": None,
        "post_language": None,
    }

    for seg in error_annotation.itersegments():
