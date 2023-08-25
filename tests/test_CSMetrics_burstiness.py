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
from functions.cs_metrics import CSMetrics  # noqa: E402


@pytest.mark.parametrize(
    "segments, expected_spans",
    [
        (
            [
                (Segment(0, 1), "A", "ENG", "1 2 3 4"),
                (Segment(1, 2), "B", "SPA", "1 2 3"),
                (Segment(2, 3), "A", "ENG", "1 2 3 4 5 6 7"),
                (Segment(3, 4), "A", "SPA", "1"),
                (Segment(4, 5), "B", "SPA", "2 3 4 5 6"),
                (Segment(5, 6), "B", "ENG", "1 2 3 4"),
                (Segment(6, 7), "B", "SPA", "1 2"),
                (Segment(7, 8), "A", "ENG", "1 2"),
                (Segment(8, 9), "A", "ENG", "3 4 5 6"),
                (Segment(9, 10), "A", "ENG", "7 8 9 10 11 12"),
                (Segment(10, 11), "B", "SPA", "1 2 3 4 5 6"),
            ],
            np.array([4, 3, 7, 6, 4, 2, 12, 6]),
        ),
        (
            [
                (Segment(0, 1), "A", "ENG", "1 2 3 4"),
                (Segment(1, 2), "B", "SPA", "1 2 3"),
                (Segment(2, 3), "A", "ENG", "1 2 3 4 5 6 7"),
                (Segment(3, 4), "A", "SPA", "1"),
                (Segment(4, 5), "B", "SPA", "2 3 4 5 6"),
                (Segment(5, 6), "B", "ENG", "1 2 3 4"),
                (Segment(6, 7), "B", "SPA", "1 2"),
                (Segment(7, 8), "A", "ENG", "1 2"),
                (Segment(8, 9), "A", "ENG", "3 4 5 6"),
                (Segment(9, 10), "A", "ENG", "7 8 9 10 11 12"),
                (Segment(10, 11), "B", "ENG", "13 14 15 16 17 18"),
            ],
            np.array([4, 3, 7, 6, 4, 2, 18]),
        ),
    ],
)
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
