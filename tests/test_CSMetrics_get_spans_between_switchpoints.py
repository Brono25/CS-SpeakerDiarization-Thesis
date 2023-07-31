import pytest
from pyannote.core import Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.transcript import Transcript  # local import
from src.cs_metrics import CSMetrics  # local import



@pytest.mark.parametrize("segments, expected_spans", [
    # No code-switching one segment
    ([
        (Segment(0, 10), ("A", "SPA", "1 2 3 4"))
     ], 
     [4]),
      # No code-switching multiple  segment
    ([
        (Segment(0, 10), ("A", "ENG", "1 2 3 4")),
        (Segment(10, 20), ("A", "ENG", "5 6 7 8 9")),
        (Segment(20, 30), ("A", "ENG", "10 11 12 13 14 15"))
     ], 
     [15]),
     # ENG ENG SPA SPA
    ([
        (Segment(0, 10), ("A", "ENG", "1 2 3 4")),
        (Segment(10, 20), ("A", "ENG", "5 6 7")),
        (Segment(20, 30), ("A", "SPA", "1 2 3 4 5")),
        (Segment(30, 40), ("A", "SPA", "6 7 8 9 10"))
    ], 
    [7, 10]),
     
    # ENG SPA ENG
    ([
        (Segment(0, 10), ("A", "ENG", "1 2 3 4")),
        (Segment(10, 20), ("A", "SPA", "1 2 3")),
        (Segment(20, 30), ("A", "ENG", "1 2 3 4 5"))
     ], 
     [4, 3, 5]),
     
    # SPA ENG SPA
    ([
        (Segment(0, 10), ("A", "SPA", "1 2 3 4")),
        (Segment(10, 20), ("A", "ENG", "1 2 3")),
        (Segment(20, 30), ("A", "SPA", "1 2 3 4 5"))
     ], 
     [4, 3, 5]), 
     
    # SPA SPA ENG
    ([
        (Segment(0, 10), ("A", "SPA", "1 2 3 4")),
        (Segment(10, 20), ("A", "SPA", "5 6 7")),
        (Segment(20, 30), ("A", "ENG", "1 2 3 4 5"))
     ], 
     [7, 5]), 
    # ENG ENG SPA
    ([
        (Segment(0, 10), ("A", "ENG", "1 2 3 4")),
        (Segment(10, 20), ("A", "ENG", "5 6 7")),
        (Segment(20, 30), ("A", "SPA", "1 2 3 4 5"))
     ], 
     [7, 5]), 

])
def test_get_spans_between_switchpoints(segments, expected_spans):
    ts = Transcript(uri="test_corpus")
    for seg, (speaker, lang, text) in segments:
        ts[seg] = (speaker, lang, text)

    cs = CSMetrics(ts)

    spans = cs.get_spans_between_switchpoints()
    assert spans == expected_spans
