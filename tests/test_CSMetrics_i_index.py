import pytest
import numpy as np
from pyannote.core import Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.functions.transcript import Transcript  # noqa: E402
from src.functions.cs_dataset_metrics import DatasetMetrics  # noqa: E402


def test_i_index():
    transcript = Transcript(uri="i-index test")
    transcript[Segment(0, 1)] = ("A", "ENG", "1 2 3 4")
    transcript[Segment(1, 2)] = ("B", "SPA", "5 6 7")
    transcript[Segment(2, 3)] = ("A", "ENG", "8 9 10 11 12")
    transcript[Segment(3, 4)] = ("A", "SPA", "13")
    transcript[Segment(4, 5)] = ("B", "SPA", "14 15")
    transcript[Segment(5, 6)] = ("B", "ENG", "16 17")
    transcript[Segment(6, 7)] = ("B", "SPA", "18 19 20")
    transcript[Segment(7, 8)] = ("A", "ENG", "21")
    transcript[Segment(8, 9)] = ("A", "SPA", "22 23")
    transcript[Segment(9, 10)] = ("A", "ENG", "24 25 26 27")
    transcript[Segment(10, 11)] = ("B", "SPA", "28 29 30")

    # Number of switch points based on language change
    num_switch_point = 9

    # Total time duration for this transcript is 11 seconds (from 0 to 11)
    total_time = 11

    # Calculate I-index based on time
    i_index_expected = num_switch_point / total_time
    
    analysis = DatasetMetrics(transcript=transcript)

    # Use i_index() function instead of i_index_token()
    i_index_result = analysis.i_index()

    assert np.isclose(i_index_expected, i_index_result, rtol=1e-05, atol=1e-08)
