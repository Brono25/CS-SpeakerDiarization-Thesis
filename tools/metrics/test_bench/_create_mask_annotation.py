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
#      _create_mask_annotation
######################################
test = EnglishSpanishErrorRate(uri=URI)
annotation = Annotation(uri=URI)
annotation[Segment(0, 2)] = "A"
annotation[Segment(3, 5)] = "A"
timeline = annotation.get_timeline()
result1 = test._create_mask_annotation(annotation)
result2 = test._create_mask_annotation(timeline)

if annotation.get_timeline() == result1.get_timeline() == result2.get_timeline():
    if result1 == result2 and result1.uri == annotation.uri:
        print("PASS: _create_mask_annotation")
        sys.exit(0)
else:
    print("FAIL: _create_mask_annotation")
    sys.exit(1)
