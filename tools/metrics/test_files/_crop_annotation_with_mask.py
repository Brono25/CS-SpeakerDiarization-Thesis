import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(script_dir))

import matplotlib.pyplot as plt
import test_files.utils as u

from pyannote.core import Annotation, Segment, Timeline
from language_metric import LanguageMetric, Mask


URI = "test bench"


#######################################
#   met._crop_annotation_with_mask
######################################
test = LanguageMetric(uri=URI)
annotation = Annotation(uri=URI)
annotation[Segment(0, 2)] = "A"
annotation[Segment(3, 5)] = "A"
annotation[Segment(3.5, 6)] = "B"
tmp = Timeline(uri=URI)
tmp.add(Segment(1, 4))
mask = Mask(tmp)
result = test._crop_annotation_with_mask(annotation, mask)

answer = Annotation(uri=annotation.uri)
answer[Segment(1, 2)] = "A"
answer[Segment(3, 4)] = "A"
answer[Segment(3.5, 4)] = "B"


if isinstance(result, Annotation) and result == answer and result.uri == annotation.uri:
    print("PASS: _keep_annotation_sections")
    sys.exit(0)
else:
    print("FAIL: _keep_annotation_sections")
    sys.exit(1)
