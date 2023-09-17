from pyannote.core import Annotation
from pyannote.core import Segment, Timeline
import os
import time
from datetime import datetime

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re
import copy

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.functions.utilities import (  # noqa: E402
    get_primary_language_of_file,
)

LOG_FILES = "/Users/brono/GitHub/cs-dataset/code-switched/sastre01/"
LABEL_REMOVAL_PATTERN = re.compile(r"^\*([A-Z]{3}): ")
LABEL_REPLACE_PATTERN = re.compile(r"\*([A-Z]{3}):")
SPA_PATTERN = re.compile(r"\[- spa\]")
ENG_PATTERN = re.compile(r"\[- eng\]")
PUNCTUATION_PATTERN = re.compile(r"[!?+<>.\"[\]:&()\~,\'-/]")
NON_SPEECH_PATTERN = re.compile(r"= ?[a-z]+")
TIMESTAMP_PATTERN = re.compile(r"\d+_\d+")
SPACE_PATTERN = re.compile(r"[\s]+")


class Transcript(Annotation):
    """
    Transcript extends the pyannote.metrics.Annotation class by adding support for
    storing the spoken text and language label alongside each annotated segment.
    Uses pyannote.core Segments.
    Usage:
            transcript = Transcript(uri=uri)
            transcript[Segment(start, end)] = (label, language, text)
    """

    def __init__(self, uri=None, modality=None):
        super().__init__(uri=uri, modality=modality)
        self.transcript = dict()
        self.language_tags = dict()

    def __setitem__(self, segment, value):
        if isinstance(value, tuple) and len(value) == 3:
            super().__setitem__(segment, value[0])
            self.transcript[segment] = value[1]
            self.language_tags[segment] = value[2]
        else:
            raise ValueError(
                "Value must be a tuple with length 3: (label, language_tag, text)"
            )

    def __eq__(self, other):
        if not isinstance(other, Transcript):
            return NotImplemented

        if self.uri != other.uri:
            return False

        if len(self) != len(other):
            return False

        for seg, (label, language, text) in self.items():
            if seg not in other or other[seg] != (label, language, text):
                return False
        return True

    def __ne__(self, other):
        if isinstance(other, Annotation):
            return True
        return not self.__eq__(other)

    def __getitem__(self, segment):
        return (
            super().__getitem__(segment),
            self.transcript[segment],
            self.language_tags[segment],
        )

    def __str__(self):
        lines = []
        for segment, (label, language, text) in self.items():
            start, end = segment.start, segment.end
            line = f"{start:.3f}|{end:.3f}|{label}|{language}|{text}"
            lines.append(line)
        return "\n".join(lines)

    def itertr(self):
        for segment in self.transcript:
            yield (
                segment.start, 
                segment.end,
                super().__getitem__(segment),
                self.transcript[segment],
                self.language_tags[segment]
            )


    def export_ref_rttm(self, output_path: str, support=False) -> str:
        ref_rttm = Annotation(uri=self.uri)
        for seg, (label, _, _) in self.items():
            ref_rttm[seg] = label

        if support:
            ref_rttm = ref_rttm.support(collar=0.0)

        if os.path.isfile(output_path):
            # if exists, add a timestamp to the filename
            filename, file_extension = os.path.splitext(output_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{filename}_{timestamp}{file_extension}"

        with open(output_path, "w") as f:
            ref_rttm.write_rttm(f)
        return output_path

    def export_lang_rttm(self, output_path, support=False) -> str:
        lang_rttm = Annotation(uri=self.uri)
        for seg, (_, language, _) in self.items():
            lang_rttm[seg] = language

        if support:
            lang_rttm = lang_rttm.support(collar=0.0)

        if os.path.isfile(output_path):
            # if exists, add a timestamp to the filename
            filename, file_extension = os.path.splitext(output_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{filename}_{timestamp}{file_extension}"

        with open(output_path, "w") as f:
            lang_rttm.write_rttm(f)
        return output_path

    def get_ref_annotation(self, support=False) -> Annotation:
        annotation = Annotation(uri=self.uri)
        for seg, (label, _, _) in self.items():
            annotation[seg] = label
        if support:
            annotation = annotation.support(collar=0.0)
        return annotation

    def get_language_annotation(self, support=False) -> Annotation:
        annotation = Annotation(uri=self.uri)
        for seg, (_, language, _) in self.items():
            annotation[seg] = language
        if support:
            annotation = annotation.support(collar=0.0)
        return annotation
    
    def get_text_annotation(self, support=False) -> Annotation:
        annotation = Annotation(uri=self.uri)
        for seg, (_, _, text) in self.items():
            annotation[seg] = text
        if support:
            annotation = annotation.support(collar=0.0)
        return annotation

    def items(self):
        for segment in self.transcript:
            yield segment, (
                super().__getitem__(segment),
                self.transcript[segment],
                self.language_tags[segment],
            )

    def save_transcript_to_file(self, output):

        # if file already exists, append a timestamp to the filename
        if os.path.exists(output):
            output = f"{output.rsplit('.', 1)[0]}_{int(time.time())}.tr"

        printable_content = []
        if self.transcript:
            for seg, (label, language, text) in self.items():
                start = seg.start
                end = seg.end
                line = f"{start:.3f}|{end:.3f}|{label}|{language}|{text}"
                printable_content.append(line)

        output_content = "\n".join(printable_content)
        with open(output, "w") as file:
            file.write(output_content)
        return output


    def crop_transcript_from_uem(self, uem: Timeline) -> 'Transcript':
        # Create a pyannote annotation for label, language and text so
        # pyannote extrude method can be used to do the cropping. 
        # after each seperate annotation is processed they are pieced
        # back together into a Transcript.

        language_annotation = self.get_language_annotation()
        label_annotation = self.get_ref_annotation()
        text_annotation = self.get_text_annotation()
        extruded_label_annotation = label_annotation.extrude(uem)
        extruded_language_annotation = language_annotation.extrude(uem)
        extruded_text_annotation = text_annotation.extrude(uem)

        new_transcript = Transcript(uri=self.uri, modality=self.modality)
        
        for segment in extruded_label_annotation.itersegments():
            label = extruded_label_annotation[segment]
            language = extruded_language_annotation[segment]
            text = extruded_text_annotation[segment]
            new_transcript[segment] = (label, language, text)
        return new_transcript


    def get_transcript_speaker_overlap_timeline(self):
        ref_ann = self.get_ref_annotation()
        return ref_ann.get_overlap()


    def duration(self):
        total_duration = self._total_duration()
        ol_duration = self.get_transcript_speaker_overlap_timeline().duration()
        duration_exclude_overlap = total_duration - ol_duration
        return total_duration, duration_exclude_overlap

    def _total_duration(self):
            all_segments = [segment for segment in self.get_ref_annotation().itersegments()]
            if not all_segments:
                return 0
            end_time = max(segment.end for segment in all_segments)
            return end_time  


def load_transcript_from_file(file, uri):
    if not os.path.exists(file):
        raise FileNotFoundError

    with open(file, "r") as f:
        content = f.readlines()

    transcript = Transcript(uri=uri)
    for line in content:
        start, end, label, language, text = line.split("|")
        transcript[Segment(float(start), float(end))] = (label, language, text.rstrip())
    return transcript

