from collections import defaultdict, OrderedDict
from prettytable import PrettyTable
import json
from pyannote.core import Timeline, Annotation, Segment
import re
import sys
import os
from pyannote.database.util import load_rttm
import matplotlib.pyplot as plt
from typing import Union, List, Dict

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

from src.functions.helper import plot_annotations
from src.functions.cs_diarization_metrics import CSDiarizationMetrics
from src.functions.transcript import (
    Transcript,
    Timeline,
    load_transcript_from_file,
)

MIN_SEG = 0.1

class ConfusionAnalysisData:
    def __init__(self, tr_file, hyp_file):
        # Fie paths and IO
        self.tr_file = tr_file
        self.uri = self.get_uri()
        self.hyp_file = self.validate_hypothesis(hyp_file)
        self.root_dir = self.get_root()
        self.pyannote_dir = f"{self.root_dir}/pyannote"
        self.output_file = f"{self.root_dir}/pyannote/{self.uri}"

        # Transcripts and Annotations
        self.tr: Transcript = load_transcript_from_file(self.tr_file, self.uri)
        self.ref_overlap = self.tr.get_ref_annotation().get_overlap()
        self.ref: Annotation = self.tr.get_ref_annotation().extrude(self.ref_overlap)
        self.lang: Annotation = self.tr.get_language_annotation().extrude(self.ref_overlap)
        self.hyp: Annotation = load_rttm(self.hyp_file)[self.uri]
        self.conf_lang: Annotation = self.get_language_confusion_annotation()
        self.conf_label: Annotation = self.hyp.crop(self.get_confusion_timeline())
        self.conf_tl: Timeline = self.conf_label.get_timeline()

        if len(self.ref.get_timeline()) != len(self.lang.get_timeline()):
            print(f"len(ref) = {len(self.ref.get_timeline())} & len(lan) = {len(self.lang.get_timeline())}")
            sys.exit(1)

        self.align_conf_lang_annotation()


    def align_conf_lang_annotation(self):
        align_conf_lang = Annotation(uri=self.uri)
        
        for (seg1, _), (seg2, _) in self.conf_label.co_iter(self.conf_lang):
            align_conf_lang[seg1] = self.conf_lang[seg2]
            
            threshold = 10
            if abs(seg1.start -  seg2.start) > threshold or abs(seg1.end -  seg2.end) > threshold:
                print(
                    "Confusion label timeline and language timeline has differing segments",
                    file=sys.stderr,
                )
                print(abs(seg1.start -  seg2.start))
                print(abs(seg1.end -  seg2.end))
                sys.exit(1)
            
        self.conf_lang = align_conf_lang

            

    def get_uri(self):
        file_name = os.path.basename(self.tr_file)
        uri = os.path.splitext(file_name)[0]
        return uri

    def get_root(self):
        root = os.path.dirname(self.tr_file)
        return root

    def get_confusion_timeline(self) -> Timeline:
        analysis = CSDiarizationMetrics(
            uri=self.uri, reference=self.ref, hypothesis=self.hyp
        )
        conf_tl = analysis._get_confusion_timeline()
        return conf_tl

    def get_language_confusion_annotation(self) -> Annotation:
        analysis = CSDiarizationMetrics(
            uri=self.uri,
            reference=self.ref,
            hypothesis=self.hyp,
            language_annotation=self.lang,
        )
        return analysis.language_confusion_annotation()

    def validate_hypothesis(self, hyp):
        hyp_name = os.path.basename(hyp)
        expected_filename = None
        if "_pyannote.rttm" in hyp_name:
            expected_filename = f"{self.uri}_pyannote.rttm"

        if hyp_name != expected_filename:
            print(f"{hyp_name} is not a hypothesis rttm file", file=sys.stderr)
            sys.exit(1)

        return hyp

    def __str__(self):
        info_str = (
            f"     URI : {self.uri}\n"
            f"      TR : {os.path.basename(self.tr_file)}\n"
            f"     HYP : {os.path.basename(self.hyp_file)}\n"
            f"    ROOT : {self.root_dir}\n"
            f"OUT_FILE : {self.output_file}\n"
        )
        return info_str

    def plot_confusions(self):
        to_plot = [
            (self.ref, "Reference"),
            (self.hyp, "Hypothesis"),
            (self.lang, "Reference Language"),
            (self.conf_label, "Labeled Confusions"),
            (self.conf_lang, "Language Confusions"),
        ]
        plot_annotations(to_plot)
        plt.show()


class ConfusionMatrix:
    """
    A class for managing a confusion matrix.

    None  = No Speech
    SS:SL = Same Speaker : Same Language
    SS:DL = Same Speaker : Different Language
    DS:SL = Different Speaker : Same Language
    DS:DL = Different Speaker : Different Language

    Key order: ["None", "SS:SL", "SS:DL", "DS:SL", "DS:DL"]
    """

    def __init__(self):
        self.matrix = defaultdict(self._nested_dict)
        self._keys = ["None", "SS:SL", "SS:DL", "DS:SL", "DS:DL"]
        for row in self.keys:
            for col in self.keys:
                self.matrix[row][col] = 0

    def _nested_dict(self):
        return OrderedDict()

    def increment_count(self, row, col):
        self.matrix[row][col] += 1

    def decrement_count(self, row, col):
        self.matrix[row][col] -= 1

    def get_count(self, row, col):
        return self.matrix[row][col]

    def sum_matrix(self):
        return sum(count for cols in self.matrix.values() for count in cols.values())

    def get_keys(self):
        return self.keys

    def __str__(self):
        table = PrettyTable()
        table.field_names = [""] + self.keys
        for row in self.keys:
            table_row = [row]
            for col in self.keys:
                table_row.append(self.matrix[row].get(col, 0))
            table.add_row(table_row)
        return str(table)

    def __eq__(self, other):
        if not isinstance(other, ConfusionMatrix):
            return False
        return self.matrix == other.matrix

    def __add__(self, other):
        if not isinstance(other, ConfusionMatrix):
            raise ValueError("Can only add ConfusionMatrix to another ConfusionMatrix")
        if sorted(self.matrix.keys()) != sorted(other.matrix.keys()):
            raise ValueError("Both matrices must have the same keys")

        new_matrix = ConfusionMatrix()
        for row_key, cols in self.matrix.items():
            for col_key, count in cols.items():
                new_matrix.matrix[row_key][col_key] = count
        for row_key, cols in other.matrix.items():
            for col_key, count in cols.items():
                new_matrix.matrix[row_key][col_key] += count
        return new_matrix

    def to_json(self, file_path):
        with open(file_path, "w") as f:
            json.dump(self.matrix, f, indent=4)

    def print_json(self):
        print(json.dumps(self.matrix, indent=4))

    @staticmethod
    def from_json(file_path):
        with open(file_path, "r") as f:
            json_data = json.load(f)
        cm = ConfusionMatrix()
        cm.matrix = defaultdict(cm._nested_dict, json_data)
        return cm

    @property
    def keys(self):
        return self._keys


class WindowFrame:
    """
    A WindowFrame is defined as three Segments. Two five second Segments
    either side of a confusion segment

                  5 sec   Confusion Segment   5 sec
                |-------|-------------------|-------|
                               WindowFrame
    """

    def __init__(self, segment: Segment, extent: float, window_dur: float = 5.0):
        self.max_duration = extent
        self.window_dur = window_dur
        self.conf_segment = segment
        self.leading_segment = None
        self.lagging_segment = None
        self.clamp_window()

    def clamp_window(self):
        leading_segment_end = min(
            self.conf_segment.end + self.window_dur, self.max_duration
        )
        lagging_segment_start = max(self.conf_segment.start - self.window_dur, 0.0)
        self.leading_segment = Segment(self.conf_segment.end, leading_segment_end)
        self.lagging_segment = Segment(lagging_segment_start, self.conf_segment.start)
        

    def __str__(self):
        lagging_str = f"[{self._format_time(self.lagging_segment.start)} --> {self._format_time(self.lagging_segment.end)}]"
        conf_str = f"[{self._format_time(self.conf_segment.start)} --> {self._format_time(self.conf_segment.end)}]"
        leading_str = f"[{self._format_time(self.leading_segment.start)} --> {self._format_time(self.leading_segment.end)}]"
        return f"{lagging_str} {conf_str} {leading_str}"

    def _format_time(self, time_in_seconds, sec=False):
        if sec:
            return time_in_seconds
        hours, remainder = divmod(int(time_in_seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{int(seconds):02d}.{milliseconds:03d}"
    
    @property
    def frame_mask(self):
        frame_mask = Timeline(uri='FrameMask')
        frame_mask.add(self.lagging_segment)
        frame_mask.add(self.conf_segment)
        frame_mask.add(self.leading_segment)
        return frame_mask

    @property
    def lead_lag_mask(self):
        lead_lag_mask = Timeline(uri='LeadLagMask')
        lead_lag_mask.add(self.leading_segment)
        lead_lag_mask.add(self.lagging_segment)
        return lead_lag_mask


    @property
    def leading_mask(self):
        leading_mask = Timeline(uri='LeadingMask')
        leading_mask.add(self.leading_segment)
        return leading_mask
    
    @property
    def lagging_mask(self):
        lagging_mask = Timeline(uri='LaggingMask')
        lagging_mask.add(self.lagging_segment)
        return lagging_mask
    @property
    def start(self):
        return self.lagging_segment.start

    @property
    def end(self):
        return self.leading_segment.end


class ConfusionTimelineAnalyser:
    def __init__(
        self,
        data: ConfusionAnalysisData,
        window_len=5,
        min_dur=0.0,
    ):
        self.uri = data.uri
        self.ref = data.ref
        self.lang = data.lang
        self.hyp = data.hyp
        self.conf_tl = data.conf_tl
        self.window_len = window_len
        self.min_dur = min_dur
        self.current_idx = 0
        self.segments = list(self.conf_tl)
        self.extent = self.ref.get_timeline().extent().duration
        self.window = None
        self.conf_label = data.conf_label
        self.conf_lang = data.conf_lang
        self.step_results: Dict[str, Union[Annotation, None, str]] = {
            "conf_label": None,
            "conf_lang": None,
            "ref_label": None,
            "ref_lang": None,
            "lag_label": None,
            "lag_lang": None,
            "lead_label": None,
            "lead_lang": None
        }
        

    def reset(self):
            self.step_results["lag_label"] = None
            self.step_results["lag_lang"] = None
            self.step_results["lead_label"] = None
            self.step_results["lead_lang"] = None
            self.step_results["conf_label"] = None
            self.step_results["conf_lang"] = None
            self.step_results["ref_label"] = None
            self.step_results["ref_lang"] =  None

    def __iter__(self):
        return self

    def __next__(self):
        while self.current_idx < len(self.segments):
            segment = self.segments[self.current_idx]
            self.current_idx += 1
            
            if segment.end - segment.start <= self.min_dur:
                continue
            
            self.window_frame = WindowFrame(segment=segment, extent=self.extent)
            frame_mask  = self.window_frame.frame_mask
            lead_mask = self.window_frame.leading_mask
            lag_mask = self.window_frame.lagging_mask
            lead_lag_mask = self.window_frame.lead_lag_mask

            
            self.ref_label_window = self.ref.crop(lead_lag_mask)
            self.ref_lang_window = self.lang.crop(lead_lag_mask)
            self.conf_label_window = self.conf_label.crop(segment)
            self.conf_lang_window = self.conf_lang.crop(segment)

        
            assert self.ref_lang_window.get_timeline() == self.ref_label_window.get_timeline()

            lag_seg = self.get_least_lagging_segment(self.ref_label_window.crop(lag_mask))
            lead_seg = self.get_least_leading_segment(self.ref_label_window.crop(lead_mask))

            self.reset()
            self.step_results["lag_label"] = self.ref_label_window[lag_seg] if lag_seg else None
            self.step_results["lag_lang"] = self.ref_lang_window[lag_seg] if lag_seg else None
            self.step_results["lead_label"] = self.ref_label_window[lead_seg] if lead_seg else None
            self.step_results["lead_lang"] = self.ref_lang_window[lead_seg] if lead_seg else None
            self.step_results["conf_label"] = list(self.conf_label_window.get_labels(segment))[0]
            self.step_results["conf_lang"] = list(self.conf_lang_window.get_labels(segment))[0]
            self.step_results["ref_label"] = self.get_label_under_mask(self.ref, segment)
            self.step_results["ref_lang"] =  self.get_label_under_mask(self.lang, segment)

            
            
            
            if not self.step_results["lag_label"] or not self.step_results["lead_label"]:
                #print(self.current_idx)
                #print(self.step_results)
                #self.inspect_window()
                pass

                
            return self.step_results
    
        raise StopIteration

    def get_least_lagging_segment(self, lagging_window: Annotation, min_seg=MIN_SEG ) -> Segment:

        seg_list = list(lagging_window.itersegments())
        for seg in reversed(seg_list):
            if seg.end - seg.start < min_seg:
                continue
            return seg   
        return None

    def get_least_leading_segment(self, leading_window: Annotation, min_seg=MIN_SEG ) -> Segment:
        for seg in leading_window.itersegments():
            if seg.end - seg.start < min_seg:
                continue
            return seg
        return None

    def get_label_under_mask(self, base_ann: Annotation,  mask: Segment):
        reduced_ann = base_ann.crop(mask)
        _, _, label = next(reduced_ann.itertracks(yield_label=True))
        return label

    def inspect_window(self):
        annotations = [
            (self.convert_to_annotation(self.window_frame.frame_mask), "Frame Mask"),
            (self.conf_label_window, "Confusion Label"),
            (self.conf_lang_window, "Confusion Language"),
            (self.ref_lang_window, "Reference Language"),
            (self.ref_label_window, "Reference Labels"),
        ]
        plot_annotations(annotations, self.window_frame.start, self.window_frame.end)
        
    
    def convert_to_annotation(self, segments: Union[Timeline, List[Segment]]):
        annotation = Annotation(uri=self.uri)
        if isinstance(segments, Timeline):
            for segment in segments:
                annotation[segment] = "Mask"
        elif isinstance(segments, list):
            for segment in segments:
                annotation[segment] = "Mask"
        else:
            raise ValueError(
                "Invalid argument type. Must be either a Timeline or a List of Segments."
            )
        return annotation






if __name__ == "__main__":
    # Create an instance
    pass
