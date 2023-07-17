import sys
import os

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(script_dir))

import utils as u
import matplotlib.pyplot as plt
import test_bench.utils as u
from pyannote.core import Annotation, Segment, Timeline
from metrics import EnglishSpanishErrorRate


URI = "test bench"

#######################################
#         met._default_uem
######################################
ref = Annotation(uri=URI)
ref[Segment(1, 11)] = "A"
hyp = Annotation(uri=URI)
hyp[Segment(0, 4)] = "A"
hyp[Segment(3, 7)] = "B"
hyp[Segment(7, 10)] = "A"

answer = Timeline(uri=URI)
answer.add(Segment(0, 11))
test = EnglishSpanishErrorRate(uri=URI, reference=ref, hypothesis=hyp)
uem = test._default_uem()


if uem.uri == ref.uri and answer == uem:
    print("PASS: _default_uem")
    sys.exit(0)
else:
    print("FAIL: _default_uem")
    sys.exit(1)
