import pytest
import numpy as np
from pyannote.core import Segment
import re

# Always use CS-SpeakerDiarization-Thesis as root
import sys

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.transcript import Transcript  # noqa: E402
from src.cs_metrics import CSMetrics  # noqa: E402

@pytest.mark.parametrize("segments, expected_spans", [
    ([
        (Segment(0, 1), "A", "1 2 3 4", "ENG"),
        (Segment(1, 2), "B", "1 2 3", "SPA"),
        (Segment(2, 3), "A", "1 2 3 4 5 6 7", "ENG"),
        (Segment(3, 4), "A", "1", "SPA"),
        (Segment(4, 5), "B", "2 3 4 5 6", "SPA"),
        (Segment(5, 6), "B", "1 2 3 4", "ENG"),
        (Segment(6, 7), "B", "1 2", "SPA"),
        (Segment(7, 8), "A", "1 2", "ENG"),
        (Segment(8, 9), "A", "3 4 5 6", "ENG"),
        (Segment(9, 10), "A", "7 8 9 10 11 12", "ENG"),
        (Segment(10, 11), "B", "1 2 3 4 5 6", "SPA")
    ], np.array([4, 3, 7, 6, 4, 2, 12, 6])),
    ([
        (Segment(0, 1), "A", "1 2 3 4", "ENG"),
        (Segment(1, 2), "B", "1 2 3", "SPA"),
        (Segment(2, 3), "A", "1 2 3 4 5 6 7", "ENG"),
        (Segment(3, 4), "A", "1", "SPA"),
        (Segment(4, 5), "B", "2 3 4 5 6", "SPA"),
        (Segment(5, 6), "B", "1 2 3 4", "ENG"),
        (Segment(6, 7), "B", "1 2", "SPA"),
        (Segment(7, 8), "A", "1 2", "ENG"),
        (Segment(8, 9), "A", "3 4 5 6", "ENG"),
        (Segment(9, 10), "A", "7 8 9 10 11 12", "ENG"),
        (Segment(10, 11), "B", "13 14 15 16 17 18", "ENG")
    ], np.array([4, 3, 7, 6, 4, 2, 18]))
])
def test_burstiness(segments, expected_spans):
    transcript = Transcript(uri="burstiness test")
    for segment in segments:
        transcript[segment[0]] = (segment[1], segment[2], segment[3])
    mean_spans = np.mean(expected_spans)
    std_spans = np.std(expected_spans)
    burstiness_expected = (std_spans - mean_spans) / (std_spans + mean_spans)
    analysis = CSMetrics(transcript=transcript)
    burstiness_result = analysis.burstiness()
    assert np.isclose(burstiness_expected, burstiness_result, rtol=1e-05, atol=1e-08)
