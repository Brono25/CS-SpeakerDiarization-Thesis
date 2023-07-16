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
ref = Annotation(uri=URI)
hyp = Annotation(uri=URI)
lang_map = Annotation(uri=URI)


# Confusion speaker A
ref[Segment(0, 5)] = "A"
ref[Segment(0, 1)] = "B"
hyp[Segment(0, 2)] = "A"
hyp[Segment(2, 4)] = "B"
hyp[Segment(4, 5)] = "A"
lang_map[Segment(0, 2.5)] = "ENG"
lang_map[Segment(0.5, 1)] = "ENG"
lang_map[Segment(1, 2)] = "SPA"
lang_map[Segment(2.5, 4.5)] = "SPA"
lang_map[Segment(4.5, 5)] = "ENG"

# Confusion speaker B
ref[Segment(5, 10)] = "B"
hyp[Segment(5, 8)] = "B"
hyp[Segment(8, 10)] = "A"
lang_map[Segment(5, 8)] = "SPA"
lang_map[Segment(8, 10)] = "ENG"

answer = {
    "english_error": 2.5,
    "english_total": 3.5,
    "spanish_error": 1.5,
    "spanish_total": 5,
}

test = met.EnglishSpanishErrorRate(
    uri=URI, reference=ref, hypothesis=hyp, language_map=lang_map
)
result = test.compute_components()
for k in result.keys():
    if result[k] != answer[k]:
        print("FAIL: compute_components")
        break
else:
    print("PASS: compute_components")

#######################################
#       met.compute_metric
######################################


#######################################
#  met.language_confusion_annotation
######################################

ref = Annotation(uri=URI)
ref[Segment(0, 10)] = "A"
ref[Segment(9, 11)] = "B"
hyp = Annotation(uri=URI)
hyp[Segment(0, 4)] = "A"
hyp[Segment(3, 8)] = "B"
hyp[Segment(8, 11)] = "A"
language_annotation = Annotation(uri=URI)
language_annotation[Segment(0, 4)] = "ENG"
language_annotation[Segment(4, 7.5)] = "SPA"
language_annotation[Segment(7.5, 11)] = "ENG"
test = met.EnglishSpanishErrorRate(
    uri=URI, reference=ref, hypothesis=hyp, language_map=language_annotation
)
result = test.language_confusion_annotation()

answer = Annotation(uri=URI)
answer[Segment(4, 7.5)] = "SPA"
answer[Segment(7.5, 8)] = "ENG"
answer[Segment(10, 11)] = "ENG"


if isinstance(result, Annotation) and result == answer and result.uri == ref.uri:
    print("PASS: language_confusion_annotation")
else:
    print("FAIL: language_confusion_annotation")

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
ref[Segment(9, 11)] = "B"
hyp = Annotation(uri=URI)
hyp[Segment(0, 4)] = "A"
hyp[Segment(3, 7)] = "C"
hyp[Segment(7, 11)] = "A"

test = met.EnglishSpanishErrorRate(uri=URI, reference=ref, hypothesis=hyp)
answer = Timeline(uri=URI)
answer.add(Segment(4, 7))
answer.add(Segment(10, 11))
result = test._get_confusion_timeline()


if ref.uri == result.uri and answer == result:
    print("PASS: _get_confusion_timeline")
else:
    print("FAIL: _get_confusion_timeline")


#######################################
#  met._timeline_to_annotation
######################################
timeline = Timeline(uri=URI)
timeline.add(Segment(0, 3))
timeline.add(Segment(2, 5))
test = met.EnglishSpanishErrorRate(uri=URI)
result = test._timeline_to_annotation(timeline, "LABEL")

answer = Annotation(uri=URI)
answer[Segment(0, 3)] = "LABEL"
answer[Segment(2, 5)] = "LABEL"

if timeline.uri == result.uri and answer == result:
    print("PASS: _timeline_to_annotation")
else:
    print("FAIL: _timeline_to_annotation")


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
