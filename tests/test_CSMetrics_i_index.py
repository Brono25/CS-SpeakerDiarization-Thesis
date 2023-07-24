import pytest
import numpy as np
from pyannote.core import Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.transcript import Transcript  # noqa: E402
from src.cs_metrics import CSMetrics  # noqa: E402


def test_i_index():
    transcript = Transcript(uri="i-index test")
    transcript[Segment(0, 1)] = ("A", "1 2 3 4", "ENG")
    transcript[Segment(1, 2)] = ("B", "5 6 7", "SPA")
    transcript[Segment(2, 3)] = ("A", "8 9 10 11 12", "ENG")
    transcript[Segment(3, 4)] = ("A", "13", "SPA")
    transcript[Segment(4, 5)] = ("B", "14 15", "SPA")
    transcript[Segment(5, 6)] = ("B", "16 17", "ENG")
    transcript[Segment(6, 7)] = ("B", "18 19 20", "SPA")
    transcript[Segment(7, 8)] = ("A", "21", "ENG")
    transcript[Segment(8, 9)] = ("A", "22 23", "SPA")
    transcript[Segment(9, 10)] = ("A", "24 25 26 27", "ENG")
    transcript[Segment(10, 11)] = ("B", "28 29 30", "SPA")

    num_switch_point = 9
    total_words = 30
    i_index_expected = num_switch_point / (total_words - 1)
    analysis = CSMetrics(transcript=transcript)
    i_index_result = analysis.i_index()

    assert np.isclose(i_index_expected, i_index_result, rtol=1e-05, atol=1e-08)
