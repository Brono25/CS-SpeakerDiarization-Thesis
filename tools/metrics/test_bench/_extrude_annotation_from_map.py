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
#  met._extrude_annotation_from_map
######################################
test = EnglishSpanishErrorRate(uri=URI)
annotation = Annotation(uri=URI)
annotation[Segment(0, 2)] = "A"
annotation[Segment(3, 5)] = "A"
annotation[Segment(3.5, 6)] = "B"
map = Annotation(uri=URI)
map[Segment(1, 4)] = "X"
result = test._extrude_annotation_from_map(annotation, map)

answer = Annotation(uri=annotation.uri)
answer[Segment(0, 1)] = "A"
answer[Segment(4, 5)] = "A"
answer[Segment(4, 6)] = "B"

if isinstance(result, Annotation) and result == answer and result.uri == annotation.uri:
    print("PASS: _extrude_annotation_from_map")
    sys.exit(0)
else:
    print("FAIL: _extrude_annotation_from_map")
    sys.exit(1)
