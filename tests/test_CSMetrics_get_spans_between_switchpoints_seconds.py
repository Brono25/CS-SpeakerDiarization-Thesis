import pytest
from pyannote.core import Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.functions.transcript import Transcript  # local import
from src.functions.cs_dataset_metrics import DatasetMetrics  # local import



@pytest.mark.parametrize("segments, expected_spans", [
    # No code-switching one segment
    ([
        (Segment(0, 10), ("A", "SPA", "1 2 3 4"))
     ], 
     {"language": ["SPA"], "time": [10]}),

    
    ([
    (Segment(0, 10), ("A", "ENG", "1 2 3 4")),
    (Segment(15, 20), ("A", "ENG", "5 6 7 8 9")),
    (Segment(20, 30), ("A", "ENG", "10 11 12 13 14 15"))
    ], 
    {"language": ["ENG"], "time": [25]}),

    # ENG ENG SPA SPA
    ([
        (Segment(0, 10), ("A", "ENG", "1 2 3 4")),
        (Segment(10, 20), ("A", "ENG", "5 6 7")),
        (Segment(25, 30), ("A", "SPA", "1 2 3 4 5")),
        (Segment(30, 40), ("A", "SPA", "6 7 8 9 10"))
    ], 
    {"language": ["ENG", "SPA"], "time": [20, 15]}),

    # ENG SPA ENG
    ([
        (Segment(0, 10), ("A", "ENG", "1 2 3 4")),
        (Segment(10, 20), ("A", "SPA", "1 2 3")),
        (Segment(20, 30), ("A", "ENG", "1 2 3 4 5"))
    ], 
    {"language": ["ENG", "SPA", "ENG"], "time": [10, 10, 10]}),

    # SPA ENG SPA
    ([
        (Segment(0, 10), ("A", "SPA", "1 2 3 4")),
        (Segment(10, 20), ("A", "ENG", "1 2 3")),
        (Segment(20, 30), ("A", "SPA", "1 2 3 4 5"))
    ], 
    {"language": ["SPA", "ENG", "SPA"], "time": [10, 10, 10]}),

    # SPA SPA ENG
    ([
        (Segment(0, 10), ("A", "SPA", "1 2 3 4")),
        (Segment(10, 20), ("A", "SPA", "5 6 7")),
        (Segment(20, 30), ("A", "ENG", "1 2 3 4 5"))
    ], 
    {"language": ["SPA", "ENG"], "time": [20, 10]}),

    # ENG ENG SPA
    ([
        (Segment(0, 10), ("A", "ENG", "1 2 3 4")),
        (Segment(10, 20), ("A", "ENG", "5 6 7")),
        (Segment(20, 30), ("A", "SPA", "1 2 3 4 5"))
    ], 
    {"language": ["ENG", "SPA"], "time": [20, 10]}),

])
def test_get_spans_between_switchpoints_seconds(segments, expected_spans):
    ts = Transcript(uri="test_corpus")
    for seg, (speaker, lang, text) in segments:
        ts[seg] = (speaker, lang, text)

    cs = DatasetMetrics(ts)

    spans = cs.get_spans_between_switchpoints_seconds()
    assert spans == expected_spans
