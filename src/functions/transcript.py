from pyannote.core import Annotation
from pyannote.core import Segment
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


def convert_cha_to_transcript(cha_file: str, uri: str, prim_lang: str) -> Transcript:
    """
    Converts CHAT (.cha) formatted file into a Transcript.

    Args:
        cha_file (str): The path to the CHAT (.cha) file to be converted.

    Returns:
        Transcript: The generated Transcript object containing labels, text and language.

    Note:
        A log indicating the steps involved in conversion is created for debugging purposes.
    """

    # iterator over labeled cha lines only
    def _get_labeled_lines(cha_file):
        with open(cha_file, "r") as f:
            cha_content = f.readlines()
        label_flag = False
        tab_flag = False
        capture_flag = False
        speaker_line = None
        for line in cha_content:
            label_flag = bool(re.match(r"^\*[A-Z]{3}:", line))
            tab_flag = bool(re.match(r"^[\s]", line))
            if label_flag:
                capture_flag = True
            if not label_flag and not tab_flag:
                capture_flag = False
            if capture_flag and label_flag:
                line = re.sub(r"\s+", " ", line)
                line = re.sub(r"\x15+", "", line)
                if speaker_line:
                    yield speaker_line
                speaker_line = line
            if capture_flag and tab_flag:
                line = re.sub(r"\x15+", "", line)
                line = re.sub(r"\s+", " ", line).lstrip()
                speaker_line = speaker_line.rstrip() + " " + line
        if speaker_line:
            yield speaker_line

    def _group_languages(line):
        groups = []
        group = ""
        for word in line.split(" "):
            if re.search(r"@s", word):
                if group and "@s" not in group:
                    groups.append(group.strip())
                    group = ""
                group += word + " "
            else:
                if group and "@s" in group:
                    groups.append(group.strip())
                    group = ""
                group += word + " "
        if group:
            groups.append(group.strip())
        groups = [x for x in groups if x != ""]
        return groups

    def _detect_language(line, prim_lang):
        if "_SPA" in line:
            language = "SPA"
        elif "_ENG" in line:
            language = "ENG"
        elif "@s" in line and prim_lang == "ENG":
            language = "SPA"
        elif "@s" in line and prim_lang == "SPA":
            language = "ENG"
        else:
            language = prim_lang
        return language

    def _filter_line(line):
        filtered_line = LABEL_REMOVAL_PATTERN.sub("", line)
        filtered_line = SPA_PATTERN.sub("_SPA", filtered_line)
        filtered_line = ENG_PATTERN.sub("_ENG", filtered_line)
        filtered_line = LABEL_REPLACE_PATTERN.sub(r"\g<1>", filtered_line)
        filtered_line = PUNCTUATION_PATTERN.sub("", filtered_line)
        filtered_line = NON_SPEECH_PATTERN.sub("", filtered_line)
        filtered_line = TIMESTAMP_PATTERN.sub("", filtered_line)
        filtered_line = SPACE_PATTERN.sub(" ", filtered_line).rstrip()
        return filtered_line

    def _output_debug_log(uri, line):
        log_file = f"{LOG_FILES}/{uri}_debug.log"
        with open(log_file, "a") as f:
            f.write(line + "\n")

    with open(f"{LOG_FILES}/{uri}_debug.log", "w") as f:
        pass
    #prim_lang = get_primary_language_of_file(uri)
    transcript = Transcript(uri=uri)
    timestamp_pattern = re.compile(r"(\d+)_(\d+)")
    label_pattern = re.compile(r"^\*([A-Z]{3}):")
    missing_timestamp_flag = False
    start, end = 0, 0
    for i, line in enumerate(_get_labeled_lines(cha_file)):
        label = label_pattern.search(line).group(1)
        match = timestamp_pattern.search(line)
        if match:
            start, end = [float(x) for x in match.groups()]
        else:
            start += 10
            end += 10
            missing_timestamp_flag = True

        _output_debug_log(uri, f"URI:{uri}---------------SECTION:{i}---------------")
        _output_debug_log(uri, "ORIGINAL:\n" + "\t\t\t" + line + "\nEDITED:")
        filtered_line = _filter_line(line)
        monolingual_lines = _group_languages(filtered_line)
        delta = 0
        for mono_line in monolingual_lines:
            language = _detect_language(mono_line, prim_lang)
            text = re.sub(r"_SPA|_ENG", "", mono_line).lstrip().rstrip()
            start_sec, end_sec = (start + delta) / 1000.0, (end - delta) / 1000.0

            # tag lines which have been split or timestamps added with a '!'
            if len(monolingual_lines) > 1 or missing_timestamp_flag:
                text = f"!{text}"
                missing_timestamp_flag = False
            delta += 1

            transcript[Segment(start_sec, end_sec)] = (label, language, text)
            _output_debug_log(
                uri,
                f"\t\t\t({start_sec:.3f}, {end_sec:.3f})\t{label} {language} {text} ",
            )

        _output_debug_log(uri, "\n")

    return transcript


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


def reduce_transcript(transcript_file: str, support=0.25) -> Transcript:
    """
    Reduces a transcript by combining adjacent segments with the same label and language.
    Segments are combined if the time gap between them is less than or equal to the specified support value.

    Parameters:
        transcript (Transcript): The original transcript to be reduced.
        support (float, optional): The maximum time gap allowed for combining segments. Defaults to 0.25 seconds.

    Returns:
        Transcript: The reduced transcript with combined segments.
    """
    if not transcript:
        return transcript

    tr = []
    for seg, (label, language, text) in transcript.items():
        tr.append([seg.start, seg.end, label, language, text])

    result = [tr.pop(0)]

    while tr:
        t_start, t_end, t_label, t_language, t_text = tr[0]

        combined = False
        for i in range(len(result) - 1, -1, -1):
            seg = result[i]
            r_start, r_end, r_label, r_language, r_text = seg


            if t_label == r_label and t_language != r_language:
                result.append(tr.pop(0))
                break

            if (r_label == t_label and r_language == t_language and t_start - r_end <= support):
                combined_seg = _combine_segments(seg, tr[0])
                result[i] = combined_seg
                tr.pop(0)
                combined = True
                break

        if not combined:
            result.append(tr.pop(0))

    result_transcript = Transcript(uri=transcript.uri)
    for segment_data in result:
        start, end, label, language, text = segment_data
        result_transcript[Segment(start, end)] = (label, language, text)

    return result_transcript


def _combine_segments(seg1, seg2):
    start1, end1, label1, language1, text1 = seg1
    start2, end2, label2, language2, text2 = seg2

    if language1 != language2 or label1 != label2:
        return

    start = min(start1, start2)
    end = max(end1, end2)
    text = text1 + " " + text2 if start1 <= start2 else text2 + " " + text1
    seg = [start, end, label1, language1, text]
    return seg


