from collections import defaultdict, OrderedDict
from prettytable import PrettyTable
import json
from pyannote.core import Timeline, Annotation, Segment


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


class Window:
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

    def _format_time(self, seconds):
        hours, remainder = divmod(int(seconds), 3600)
        minutes, seconds = divmod(remainder, 60)
        milliseconds = (seconds - int(seconds)) * 1000
        return f"{hours:02d}:{minutes:02d}:{int(seconds):02d}.{int(milliseconds):03d}"



class ConfusionTimelineAnalyser:
    def __init__(
        self,
        ref: Annotation,
        lang: Annotation,
        hyp: Annotation,
        confusion_timeline: Timeline,
        window_len=5,
        min_dur=0.0,
    ):
        self.ref = ref
        self.lang = lang
        self.hyp = hyp
        self.conf_tl = confusion_timeline
        self.window_len = window_len
        self.min_dur = min_dur
        self.current_idx = 0
        self.segments = list(self.conf_tl)
        self.extent = self.ref.get_timeline().extent()

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_idx >= len(self.segments):
            raise StopIteration
        
        segment = self.segments[self.current_idx]
        window = Window(segment=segment, max_duration=self.extent)

        



if __name__ == "__main__":
    # Create an instance
    cm = ConfusionMatrix()
    x = ConfusionMatrix().from_json("/Users/brono/Desktop/cm.json")

    non, sssl, ssdl, dssl, dsdl = cm.keys




