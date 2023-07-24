import pytest
from pyannote.core import Annotation, Segment, Timeline

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.language_error import LanguageError, Mask  # noqa: E402

URI = "test bench"


def test_crop_annotation_with_mask():
    test = LanguageError(uri=URI)
    annotation = Annotation(uri=URI)
    annotation[Segment(0, 2)] = "A"
    annotation[Segment(3, 5)] = "A"
    annotation[Segment(3.5, 6)] = "B"
    tmp = Timeline(uri=URI)
    tmp.add(Segment(1, 4))
    mask = Mask(tmp)
    result = test._crop_annotation_with_mask(annotation, mask)

    answer = Annotation(uri=annotation.uri)
    answer[Segment(1, 2)] = "A"
    answer[Segment(3, 4)] = "A"
    answer[Segment(3.5, 4)] = "B"

    assert (
        isinstance(result, Annotation)
        and result == answer
        and result.uri == annotation.uri
    ), "Test failed: _keep_annotation_sections"


test_crop_annotation_with_mask()
