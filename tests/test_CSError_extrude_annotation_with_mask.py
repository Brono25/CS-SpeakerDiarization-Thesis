import pytest
from pyannote.core import Annotation, Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.cs_error import CSError, Mask  # noqa: E402

URI = "test bench"


def test_extrude_annotation_with_mask():
    test = CSError(uri=URI)
    annotation = Annotation(uri=URI)
    annotation[Segment(0, 2)] = "A"
    annotation[Segment(3, 5)] = "A"
    annotation[Segment(3.5, 6)] = "B"
    tmp = Annotation(uri=URI)
    tmp[Segment(1, 4)] = "X"
    mask = Mask(tmp)
    result = test._extrude_annotation_with_mask(annotation, mask)

    answer = Annotation(uri=annotation.uri)
    answer[Segment(0, 1)] = "A"
    answer[Segment(4, 5)] = "A"
    answer[Segment(4, 6)] = "B"

    assert (
        isinstance(result, Annotation)
        and result == answer
        and result.uri == annotation.uri
    ), "Test failed: _extrude_annotation_from_map"
