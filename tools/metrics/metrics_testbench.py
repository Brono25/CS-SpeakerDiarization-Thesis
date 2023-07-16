import matplotlib.pyplot as plt
from pyannote.core import Annotation, Segment, Timeline, notebook
from pyannote.metrics.errors.identification import IdentificationErrorAnalysis
import utils
import metrics as met
import sys

URI = "test bench"
#######################################
#       met.compute_components
######################################
test = met.EnglishSpanishErrorRate(uri=URI)
ref = Annotation(uri=URI)
hyp = Annotation(uri=URI)
lang_map = Annotation(uri=URI)


#######################################
#       met.compute_metric
######################################

#######################################
#       met.compute_metric
######################################


#######################################
#  met.language_confusion_annotation
######################################


#######################################
#       met._extrude_overlap
######################################
test = met.EnglishSpanishErrorRate(uri=URI)
annotation = Annotation(uri=URI)
annotation[Segment(0, 1)] = "A"
annotation[Segment(2, 3)] = "A"
annotation[Segment(4, 7)] = "A"
annotation[Segment(0.5, 2)] = "B"
annotation[Segment(3, 5)] = "B"
annotation[Segment(6, 7)] = "B"

result = test._extrude_overlap(annotation)

answer = Annotation(uri=annotation.uri)
answer[Segment(0, 0.5)] = "A"
answer[Segment(2, 3)] = "A"
answer[Segment(1, 2)] = "A"
answer[Segment(5, 6)] = "A"
answer[Segment(1, 2)] = "B"
answer[Segment(3, 4)] = "B"


if isinstance(result, Annotation) and result == answer and result.uri == annotation.uri:
    print("PASS: _extrude_overlap")
else:
    print("FAIL: _extrude_overlap")


#######################################
#  met._filter_language_annotation
######################################
test = met.EnglishSpanishErrorRate(uri=URI)
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
else:
    print("FAIL: _filter_language_annotation")


#######################################
#  met._get_confusion_timeline
######################################
ref = Annotation(uri=URI)
ref[Segment(0, 10)] = "A"
hyp = Annotation(uri=URI)
hyp[Segment(0, 4)] = "A"
hyp[Segment(3, 7)] = "B"
hyp[Segment(7, 10)] = "A"

test = met.EnglishSpanishErrorRate(uri=URI, reference=ref, hypothesis=hyp)
answer = Timeline(uri=URI)
answer.add(Segment(4, 7))
result = test._get_confusion_timeline()

if ref.uri == result.uri and answer == result:
    print("PASS: _get_confusion_timeline")
else:
    print("FAIL: _get_confusion_timeline")


#######################################
#  met._timeline_to_annotation
######################################


""" 
utils.plot_annotations([(ref, "ref"), (hyp, "hyp")])
utils.plot_timelines([(answer, "answer"), (result, "result")])
plt.show() """
 
#######################################
#   met._crop_annotation_from_map
######################################
test = met.EnglishSpanishErrorRate(uri=URI)
annotation = Annotation(uri=URI)
annotation[Segment(0, 2)] = "A"
annotation[Segment(3, 5)] = "A"
annotation[Segment(3.5, 6)] = "B"
map = Timeline(uri=URI)
map.add(Segment(1, 4))
result = test._crop_annotation_from_map(annotation, map)

answer = Annotation(uri=annotation.uri)
answer[Segment(1, 2)] = "A"
answer[Segment(3, 4)] = "A"
answer[Segment(3.5, 4)] = "B"


if isinstance(result, Annotation) and result == answer and result.uri == annotation.uri:
    print("PASS: _keep_annotation_sections")
else:
    print("FAIL: _keep_annotation_sections")

#######################################
#  met._extrude_annotation_from_map
######################################
test = met.EnglishSpanishErrorRate(uri=URI)
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
else:
    print("FAIL: _extrude_annotation_from_map")


#######################################
#   met._create_mask_annotation
######################################
test = met.EnglishSpanishErrorRate(uri=URI)
annotation = Annotation(uri=URI)
annotation[Segment(0, 2)] = "A"
annotation[Segment(3, 5)] = "A"
timeline = annotation.get_timeline()
result1 = test._create_mask_annotation(annotation)
result2 = test._create_mask_annotation(timeline)

if annotation.get_timeline() == result1.get_timeline() == result2.get_timeline():
    if result1 == result2 and result1.uri == annotation.uri:
        print("PASS: _create_mask_annotation")
else:
    print("FAIL: _create_mask_annotation")


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
test = met.EnglishSpanishErrorRate(uri=URI, reference=ref, hypothesis=hyp)
uem = test._default_uem()

if uem.uri == ref.uri and answer == uem:
    if result1 == result2 and result1.uri == annotation.uri:
        print("PASS: _default_uem")
else:
    print("FAIL: _default_uem")
