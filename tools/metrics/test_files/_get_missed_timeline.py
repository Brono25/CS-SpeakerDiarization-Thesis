import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(script_dir))

import matplotlib.pyplot as plt
import test_files.utils as u

from pyannote.core import Annotation, Segment, Timeline
from language_metric import LanguageMetric


URI = "test bench"


#######################################
#  met._get_missed_timeline
######################################

ref = Annotation(uri=URI)
ref[Segment(0, 3)] = "A"
ref[Segment(3, 6)] = "B"
ref[Segment(6, 10)] = "A"

hyp = Annotation(uri=URI)
hyp[Segment(0, 4)] = "A"
hyp[Segment(7, 11)] = "A"

test = LanguageMetric(uri=URI, reference=ref, hypothesis=hyp)
answer = Timeline(uri=URI)
answer.add(Segment(4, 7))
result = test._get_missed_timeline()

if ref.uri == result.uri and answer == result:
    print("PASS: _get_missed_timeline")
    sys.exit(0)
else:
    print("FAIL: _get_missed_timeline")
    sys.exit(1)
