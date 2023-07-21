from typing import Union
import test_files.utils as u
import matplotlib.pyplot as plt
from pyannote.core import Annotation, Timeline, Segment
from pyannote.metrics.base import BaseMetric
from pyannote.metrics.errors.identification import IdentificationErrorAnalysis
import copy


class Mask(Annotation):
    """
    A subclass of Annotation for manipulating other Annotation instances,
    acting as a tool to guide cropping and extruding of annotations.
    The segments of either a Timeline or Annotation can be turned into a Mask.
    """

    def __init__(self, obj=None):
        if obj is None:
            return
        super().__init__(uri=obj.uri)
        if isinstance(obj, Annotation):
            for segment in obj.itertracks():
                self[segment] = "MASK"
        elif isinstance(obj, Timeline):
            for segment in obj:
                self[segment] = "MASK"
        else:
            raise TypeError(
                f"Expected an object of type 'Annotation' or 'Timeline', got {type(obj).__name__}"
            )


class LanguageMetric(BaseMetric):
    def __init__(
        self, reference=None, hypothesis=None, language_annotation=None, uri=None
    ):
        super().__init__(uri=uri)
        self.uri = uri
        self.ref = copy.deepcopy(reference)
        self.hyp = copy.deepcopy(hypothesis)
        self.lang_ann = None
        self.overlap_mask = None
        if self.ref:
            self.overlap_mask = Mask(self.ref.get_overlap())
        if language_annotation:
            self.lang_ann = self._extrude_annotation_with_mask(
                copy.deepcopy(language_annotation), self.overlap_mask
            )
        self.spanish = "SPA"
        self.english = "ENG"

    @classmethod
    def metric_name(cls):
        return "English and Spanish Error Rate"

    @classmethod
    def metric_components(cls):
        return [
            "english_total",
            "english_conf_error",
            "english_miss_error",
            "spanish_conf_error",
            "spanish_miss_error",
            "spanish_total",
        ]

    def compute_metric(self, components: object):
        eng_total = components["english_total"]
        eng_conf_error = components["english_conf_error"]
        eng_miss_error = components["english_miss_error"]
        spa_conf_error = components["spanish_conf_error"]
        spa_miss_error = components["spanish_miss_error"]
        spa_total = components["spanish_total"]

        error_rates = {
            "english_conf_error_rate": eng_conf_error / eng_total,
            "spanish_conf_error_rate": spa_conf_error / spa_total,
            "english_miss_error_rate": eng_miss_error / eng_total,
            "spanish_miss_error_rate": spa_miss_error / spa_total,
            "english_error_rate": (eng_conf_error + eng_miss_error) / eng_total,
            "spanish_error_rate": (spa_conf_error + spa_miss_error) / spa_total,
        }
        return error_rates

    def compute_components(self):
        confusion_components = self.compute_confusion_components()
        miss_comp = self.compute_miss_components()
        assert miss_comp["english_total"] == confusion_components["english_total"], "Error"
        assert miss_comp["spanish_total"] == confusion_components["spanish_total"], "Error"
        components = {**confusion_components, **miss_comp}
        return components

    def compute_confusion_components(self):
        lang_conf_annotation = self.language_confusion_annotation()

        english_error = self._filter_language_annotation(lang_conf_annotation, "ENG")
        spanish_error = self._filter_language_annotation(lang_conf_annotation, "SPA")
        english_tot = self._filter_language_annotation(self.lang_ann, "ENG")
        spanish_tot = self._filter_language_annotation(self.lang_ann, "SPA")

        components = {
            "english_conf_error": english_error.get_timeline().duration(),
            "english_total": english_tot.get_timeline().duration(),
            "spanish_conf_error": spanish_error.get_timeline().duration(),
            "spanish_total": spanish_tot.get_timeline().duration(),
        }
        return components

    def compute_miss_components(self):

        lang_miss_annotation = self.language_missed_annotation()

        english_miss = self._filter_language_annotation(lang_miss_annotation, "ENG")
        spanish_miss = self._filter_language_annotation(lang_miss_annotation, "SPA")
        english_tot = self._filter_language_annotation(self.lang_ann, "ENG")
        spanish_tot = self._filter_language_annotation(self.lang_ann, "SPA")

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
        confusion_mask = Mask(self._get_confusion_timeline())
        language_confusion_errors_annotation = self._crop_annotation_with_mask(
            self.lang_ann, confusion_mask
        )
        return language_confusion_errors_annotation

    def language_missed_annotation(self):
        """
        Returns an Annotation object where each segment corresponds to a time interval
        where missed detection errors occurred. Each segment is labeled with the language/s
        that occurred within that segment.
        """
        missed_mask = Mask(self._get_missed_timeline())
        language_missed_detection_errors_annotation = self._crop_annotation_with_mask(
            self.lang_ann, missed_mask
        )
        return language_missed_detection_errors_annotation

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
        analysis = IdentificationErrorAnalysis(collar=0.0, skip_overlap=True)
        errors = analysis.difference(self.ref, self.hyp, uem=uem)
        for segment, _, label in errors.itertracks(yield_label=True):
            status, _, _ = label
            if status == "missed detection":
                missed_tl.add(segment)
        return missed_tl.support()

    def _crop_annotation_with_mask(
        self, annotation: Annotation, mask: Mask
    ) -> Annotation:
        """
        Crop the parts of the annotation dictated by the mask. The mask is
        the segments of either a Timeline or Annotation (labels dont matter).

        annotation: |----|  |------|
        mask:          |-------|
        return:        |-|  |--|
        """
        cropped_annotation = Annotation(uri=annotation.uri)
        for seg in mask.itersegments():
            tmp = annotation.crop(seg, mode="intersection")
            cropped_annotation.update(tmp)
        return cropped_annotation

    def _extrude_annotation_with_mask(
        self, annotation: Annotation, mask: Mask
    ) -> Annotation:
        """
        Extrude (remove) the parts of the annotation dictated by the mask. The mask is
        the segments of either a Timeline or Annotation (labels dont matter).
        annotation: |----|  |------|
        mask:           |-------|
        return:     |--|       |---|
        """
        extruded_annotation = annotation.extrude(mask.get_timeline())
        return extruded_annotation

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
