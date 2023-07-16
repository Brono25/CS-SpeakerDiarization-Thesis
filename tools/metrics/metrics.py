from typing import Union
import utils as u
import matplotlib.pyplot as plt
from pyannote.core import Annotation, Timeline
from pyannote.metrics.base import BaseMetric
from pyannote.metrics.errors.identification import IdentificationErrorAnalysis


class EnglishSpanishErrorRate(BaseMetric):
    def __init__(self, reference=None, hypothesis=None, language_map=None, uri=None):
        super().__init__(uri=uri)
        self.uri = uri
        self.ref = reference
        self.hyp = hypothesis
        self.lang_map = self._lang_map_extrude_overlap(language_map)

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
    
    def compute_components(self):
        conf_components = self.compute_conf_components()
        miss_components = self.compute_miss_components()

        components = {**conf_components, **miss_components}
        return components

    def compute_conf_components(self):
        # 1. Crop the language annotation to the sections where confusion happens
        lang_conf_annotation = self.language_confusion_annotation()

        # 2. Isolate the spanish and english total speaking time and time in confusion
        english_error = self._filter_language_annotation(lang_conf_annotation, "ENG")
        spanish_error = self._filter_language_annotation(lang_conf_annotation, "SPA")
        english_tot = self._filter_language_annotation(self.lang_map, "ENG")
        spanish_tot = self._filter_language_annotation(self.lang_map, "SPA")

        # 3. Return the durations in the componants
        components = {
            "english_conf_error": english_error.get_timeline().duration(),
            "english_total": english_tot.get_timeline().duration(),
            "spanish_conf_error": spanish_error.get_timeline().duration(),
            "spanish_total": spanish_tot.get_timeline().duration(),
        }
        return components

    def compute_miss_components(self):
        # 1. Crop the language annotation to the sections where missed detection happens
        lang_miss_annotation = self.language_missed_annotation()

        # 2. Isolate the spanish and english total speaking time and time in missed detection
        english_miss = self._filter_language_annotation(lang_miss_annotation, "ENG")
        spanish_miss = self._filter_language_annotation(lang_miss_annotation, "SPA")
        english_tot = self._filter_language_annotation(self.lang_map, "ENG")
        spanish_tot = self._filter_language_annotation(self.lang_map, "SPA")

        # 3. Return the durations in the components
        components = {
            "english_miss_error": english_miss.get_timeline().duration(),
            "english_total": english_tot.get_timeline().duration(),
            "spanish_miss_error": spanish_miss.get_timeline().duration(),
            "spanish_total": spanish_tot.get_timeline().duration(),
        }
        return components

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
        language_confusion_errors_annotation = self._crop_annotation_from_map(
            self.lang_map, confusion_mask
        )
        return language_confusion_errors_annotation

    def language_missed_annotation(self):
        """
        Returns an Annotation object where each segment corresponds to a time interval
        where missed detection errors occurred. Each segment is labeled with the language/s
        that occurred within that segment.
        """
        # 1. Get the segments where the missed detection errors occurred
        missed_mask = self._timeline_to_annotation(
            self._get_missed_timeline(), "MISS_MASK"
        )

        # 2. Crop the language map using the missed detection annotation as a mask
        language_missed_detection_errors_annotation = self._crop_annotation_from_map(
            self.lang_map, missed_mask
        )
        return language_missed_detection_errors_annotation

    def _extrude_overlap(self, annotation) -> Annotation:
        """Return the annotation with its overlap segments subtracted"""
        annotation_extruded_overlap = None
        if annotation is not None:
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
        # skip_overlap only skips on reference
        analysis = IdentificationErrorAnalysis(collar=0.0, skip_overlap=True)
        errors = analysis.difference(self.ref, self.hyp, uem=uem)
        for segment, _, label in errors.itertracks(yield_label=True):
            status, _, _ = label
            if status == "confusion":
                confusion_tl.add(segment)
        return confusion_tl.support()

    def _get_missed_timeline(self) -> Timeline:
        """
        Returns a timeline consisting of all the missed detection errors between ref and hyp.
        """
        missed_tl = Timeline(uri=self.uri)
        uem = self._default_uem()
        # skip_overlap only skips on reference
        analysis = IdentificationErrorAnalysis(collar=0.0, skip_overlap=True)
        errors = analysis.difference(self.ref, self.hyp, uem=uem)
        for segment, _, label in errors.itertracks(yield_label=True):
            status, _, _ = label
            if status == "missed detection":
                missed_tl.add(segment)
        return missed_tl.support()

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

    def _lang_map_extrude_overlap(self, language_map):
        """
        Remove overlaps from language map to align with ref and hyp
        """
        if language_map is not None:
            overlap_extruded = self._extrude_overlap(language_map)
            overlap_same_label_map = overlap_extruded.get_timeline().get_overlap()
            overlap_extruded = self._extrude_annotation_from_map(
                overlap_extruded, overlap_same_label_map
            )
            return overlap_extruded
        else:
            return None
