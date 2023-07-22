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
#     met.compute_confusion_components
######################################
ref = Annotation(uri=URI)
hyp = Annotation(uri=URI)
lang_map = Annotation(uri=URI)

# Confusion Errors
ref[Segment(0, 5)] = "A"
ref[Segment(0, 2)] = "B"
hyp[Segment(0, 2)] = "A"
hyp[Segment(2, 4)] = "B"
hyp[Segment(4, 5)] = "A"
lang_map[Segment(0, 2.5)] = "ENG"
lang_map[Segment(0, 1)] = "ENG"
lang_map[Segment(1, 2)] = "SPA"
lang_map[Segment(2.5, 4.5)] = "SPA"
lang_map[Segment(4.5, 5)] = "ENG"
ref[Segment(5, 10)] = "B"
hyp[Segment(5, 8)] = "B"
hyp[Segment(8, 10)] = "A"
lang_map[Segment(5, 8)] = "SPA"
lang_map[Segment(8, 10)] = "ENG"

answer = {
    "english_conf_error": 2.5,
    "english_total": 3,
    "spanish_conf_error": 1.5,
    "spanish_total": 5,
}

test = LanguageMetric(
    uri=URI, reference=ref, hypothesis=hyp, language_annotation=lang_map
)
result = test.compute_confusion_components()


# u.plot_annotations([(ref, "ref"), (hyp, "hyp"), (lang_map, "lang_map")])
plt.show()


for k in result.keys():
    if result[k] != answer[k]:
        print("FAIL: compute_confusion_components")
        print(f"{k}: {result[k]} =/= {answer[k]}")
        sys.exit(1)
        break
else:
    print("PASS: compute_confusion_components")
    sys.exit(0)
