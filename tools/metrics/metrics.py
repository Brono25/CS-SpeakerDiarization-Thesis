import matplotlib.pyplot as plt
from pyannote.core import Annotation, Segment, Timeline, notebook
from pyannote.metrics.errors.identification import IdentificationErrorAnalysis
import utils
from pyannote.metrics.base import BaseMetric
from typing import Union


class EnglishSpanishErrorRate(BaseMetric):
    def __init__(self, reference=None, hypothesis=None, language_map=None, uri=None):
        super().__init__(uri=uri)
        self.uri = uri
        self.ref = reference
        self.hyp = hypothesis
        self.lang_map = language_map
        self.spanish = "SPA"
        self.english = "ENG"

    @classmethod
    def metric_name(cls):
        return "English and Spanish Error Rate"

    @classmethod
    def metric_components(cls):
        return [
            "english error seconds",
            "spanish error seconds",
            "total english seconds",
            "total spanish seconds",
        ]

    def compute_components(self):
        # 1. Select the language map segments which occur during a confusion error

        # 2. Get the time in seconds of each language which occur during a
        # confusion error

        english_error_seconds = 0

        spanish_error_seconds = 0

        # 3. Get the total english and spanish speaking time

        english_total_seconds = 0

        spanish_total_seconds = 0

        # 4. Return the componants
        components = {
            "english_error": english_error_seconds,
            "english_total": english_total_seconds,
            "spanish_error": spanish_error_seconds,
            "spanish_total": spanish_total_seconds,
        }
        return components

    def compute_metric(self, components):
        english_total = components["english_total"]
        english_error = components["english_error"]
        spanish_error = components["spanish_error"]
        spanish_total = components["spanish_total"]

        error_rates = {
            "english_error_rate": english_error / english_total,
            "spanish_error_rate": spanish_error / spanish_total,
        }
        return error_rates

    def language_confusion_annotation(self):
        """
        Returns an Annotation object where each segment corresponds to a time interval
        where confusion errors occurred. Each segment is labeled with the language/s
        that occurred within that segment.
        """
        # 1. Get the segments where the confusion errors occurred
        confusion_mask = self._timeline_to_annotation(
            self._get_confusion_timeline(), "CONF_MASK"
        )
        # 2. Crop the language map using the confusion annotation as a mask
        language_confusion_errors_annotation = self._keep_annotation_sections(
            self.lang_map, confusion_mask
        )
        return language_confusion_errors_annotation

    def _extrude_overlap(self, annotation: Annotation) -> Annotation:
        """Return the annotation with its overlap segments subtracted"""
        overlap = annotation.get_overlap()
        annotation_extruded_overlap = annotation.extrude(overlap)
        return annotation_extruded_overlap

    def _filter_language_annotation(
        self, annotation: Annotation, language: str
    ) -> Annotation:
        """
        Takes in a language annotation and returns a single language annotation
        """
        filtered_annotation = Annotation(uri=annotation.uri)

        for segment, _, label in annotation.itertracks(yield_label=True):
            if label == language:
                filtered_annotation[segment] = label
        return filtered_annotation

    def _get_confusion_timeline(self) -> Timeline:
        """
        Returns a timeline consisting of all the confusion errors between ref and hyp.
        """
        confusion_tl = Timeline(uri=self.uri)
        uem = self._default_uem()
        analysis = IdentificationErrorAnalysis(collar=0.0, skip_overlap=True)
        errors = analysis.difference(self.ref, self.hyp, uem=uem)

        for segment, _, label in errors.itertracks(yield_label=True):
            status, _, _ = label
            if status == "confusion":
                confusion_tl.add(segment)
        return confusion_tl

    def _timeline_to_annotation(self, timeline: Timeline, label: str) -> Annotation:
        """Convert a timeline to an annotation with a specified label."""
        annotation = Annotation(uri=timeline.uri)
        for segment in timeline:
            annotation[segment] = label
        return annotation

    def _crop_annotation_from_map(
        self, annotation: Annotation, map: Union[Annotation, Timeline]
    ) -> Annotation:
        """
        Crop the parts of the annotation dictated by the map. The map is
        the segments of either a Timeline or Annotation (labels dont matter).

        annotation: |----|  |------|
        mask:          |-------|
        return:        |-|  |--|
        """
        mask = self._create_mask_annotation(map=map)
        cropped_annotation = Annotation(uri=annotation.uri)
        for seg in mask.itersegments():
            tmp = annotation.crop(seg, mode="intersection")
            cropped_annotation.update(tmp)
        return cropped_annotation

    def _extrude_annotation_from_map(
        self, annotation: Annotation, map: Union[Annotation, Timeline]
    ) -> Annotation:
        """
        Extrude (remove) the parts of the annotation dictated by the map. The map is
        the segments of either a Timeline or Annotation (labels dont matter).
        annotation: |----|  |------|
        map:           |-------|
        return:     |--|       |---|
        """
        mask = self._create_mask_annotation(map=map)
        extruded_annotation = annotation.extrude(mask.get_timeline())
        return extruded_annotation

    def _create_mask_annotation(self, map: Union[Annotation, Timeline]) -> Annotation:
        """
        Takes in a map and turns it into a mask annotation. A map is either
        an annotation or timeline consisting of segments you want to use for 
        manipulating annotations or timelines. A mask is these segments turned
        into an annotation with the label "MASK" for every label. Masks are 
        Annotations so they can use Annotation methods like crop and extrude
        """
        mask = Annotation(uri=map.uri)
        label = "MASK"
        if isinstance(map, Annotation):
            for segment in map.itersegments():
                mask[segment] = label
            return mask
        elif isinstance(map, Timeline):
            for segment in map:
                mask[segment] = label
        else:
            raise ValueError("Must be Timeline or Annotation instances")
        return mask

    def _default_uem(self) -> Timeline:
        """
        Creates a uem covering the extent of ref and hyp.
        Not required, it just to suppress the no uem warning.
        """
        ref_tl = self.ref.get_timeline()
        hyp_tl = self.hyp.get_timeline()
        extent_segment = ref_tl.union(hyp_tl).extent()
        uem = Timeline([extent_segment], uri=self.uri)
        return uem
