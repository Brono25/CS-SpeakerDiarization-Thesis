import os
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.dirname(script_dir))

import matplotlib.pyplot as plt
import test_files.utils as u

from pyannote.core import Annotation, Segment
from language_metric import LanguageMetric


URI = "test bench"


#######################################
#  met._filter_language_annotation
######################################
test = LanguageMetric(uri=URI)
language_annotation = Annotation(uri=URI)
language_annotation[Segment(0, 2)] = "ENG"
language_annotation[Segment(3, 5)] = "SPA"
language_annotation[Segment(3.5, 6)] = "ENG"
spanish = test._filter_language_annotation(language_annotation, "SPA")
english = test._filter_language_annotation(language_annotation, "ENG")

eng_answer = Annotation(uri=language_annotation.uri)
eng_answer[Segment(0, 2)] = "ENG"
eng_answer[Segment(3.5, 6)] = "ENG"
spa_answer = Annotation(uri=language_annotation.uri)
spa_answer[Segment(3, 5)] = "SPA"

if (
    isinstance(english, Annotation)
    and english == eng_answer
    and spanish == spa_answer
    and language_annotation.uri == english.uri
):
    print("PASS: _filter_language_annotation")
    sys.exit(0)
else:
    print("FAIL: _filter_language_annotation")
    sys.exit(1)
