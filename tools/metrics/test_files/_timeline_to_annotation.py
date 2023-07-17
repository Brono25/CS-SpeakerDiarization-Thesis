import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(script_dir))

import matplotlib.pyplot as plt
import test_files.utils as u

from pyannote.core import Annotation, Segment, Timeline
from language_metrics import EnglishSpanishErrorRate


URI = "test bench"


#######################################
#  met._timeline_to_annotation
######################################
timeline = Timeline(uri=URI)
timeline.add(Segment(0, 3))
timeline.add(Segment(2, 5))
test = EnglishSpanishErrorRate(uri=URI)
result = test._timeline_to_annotation(timeline, "LABEL")

answer = Annotation(uri=URI)
answer[Segment(0, 3)] = "LABEL"
answer[Segment(2, 5)] = "LABEL"

if timeline.uri == result.uri and answer == result:
    print("PASS: _timeline_to_annotation")
    sys.exit(0)
else:
    print("FAIL: _timeline_to_annotation")
    sys.exit(1)
