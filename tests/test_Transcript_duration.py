import os
import pytest
from pyannote.core import Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.functions.transcript import Transcript  # noqa: E402
from src.functions.utilities import TEST_FILES  # noqa: E402


def test_transcript_duration():
    tr = Transcript(uri='test')
    tr[Segment(1, 4)] = ('a', 'eng', 'hello')
    tr[Segment(3, 6)] = ('b', 'eng', 'world')
    tr[Segment(8, 10)] = ('a', 'eng', '!')

    expected_total_duration = 10
    expected_no_overlap_duration = 9
    
    total_duration_result, duration_no_overlap_result = tr.duration()

    assert total_duration_result == expected_total_duration
    assert duration_no_overlap_result == expected_no_overlap_duration

