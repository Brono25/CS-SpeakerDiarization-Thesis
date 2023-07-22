import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(script_dir))

import matplotlib.pyplot as plt
import test_files.utils as u

from pyannote.core import Annotation, Segment
from language_metric import LanguageMetric, Mask 


URI = "test bench"


#######################################
#  met._extrude_annotation_from_map
######################################
test = LanguageMetric(uri=URI)
annotation = Annotation(uri=URI)
annotation[Segment(0, 2)] = "A"
annotation[Segment(3, 5)] = "A"
annotation[Segment(3.5, 6)] = "B"
tmp = Annotation(uri=URI)
tmp[Segment(1, 4)] = "X"
mask = Mask(tmp)
result = test._extrude_annotation_with_mask(annotation, mask)

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
