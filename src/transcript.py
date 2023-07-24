from pyannote.core import Annotation
from pyannote.core import Segment
import os
import time
from datetime import datetime

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.utilities import (  # noqa: E402
    get_uri_of_file,
    get_primary_language_of_file,
    TRANSCRIPTION_FILES_DIR,
    ROOT_DIR,
)


class Transcript(Annotation):
    """
    Transcript extends the pyannote.metrics.Annotation class by adding support for
    storing the spoken text and language label alongside each annotated segment.
    Uses pyannote.core Segments.
    Usage:
            transcript = Transcript(uri=uri)
            transcript[Segment(start, end)] = (label, text, language)
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
                "Value must be a tuple with length 3: (label, text, language_tag)"
            )

    def __eq__(self, other):
        if not isinstance(other, Transcript):
            return NotImplemented

        if self.uri != other.uri:
            return False

        if len(self) != len(other):
            return False

        for seg, (language, label, text) in self.items():
            if seg not in other or other[seg] != (language, label, text):
                return False
        return True

    def __ne__(self, other):
        return not self.__eq__(other)

    def __getitem__(self, segment):
        return (
            super().__getitem__(segment),
            self.transcript[segment],
            self.language_tags[segment],
        )

    def save_as_rttm(self, output_path: str = None):
        if output_path is None:
            output_path = f"{ROOT_DIR}/{self.uri}.rttm"
        if os.path.isfile(output_path):
            # if exists, add a timestamp to the filename
            filename, file_extension = os.path.splitext(output_path)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_path = f"{filename}_{timestamp}{file_extension}"

        with open(output_path, "w") as f:
            self.write_rttm(f)

        with open(output_path, "w") as f:
            self.write_rttm(f)

    def items(self):
        for segment in self.transcript:
            yield segment, (
                super().__getitem__(segment),
                self.transcript[segment],
                self.language_tags[segment],
            )


def cha_to_transcript(cha_file):
    uri = get_uri_of_file(cha_file)
    prim_lang = get_primary_language_of_file(uri)

    with open(cha_file, "r") as f:
        cha_content = f.readlines()

    speaker_content = _get_speaker_content_from_cha(cha_content)
    filtered_content = _filter_content(speaker_content)
    fixed_timestamp_content = _fix_timestamps(filtered_content)
    transcript_content = _seperate_content_languages(fixed_timestamp_content)
    transcript = _build_transcript(transcript_content, prim_lang, uri)

    return transcript


def save_transcript_to_file(transcript: Transcript, output=None):
    if not output:
        output = f"{TRANSCRIPTION_FILES_DIR}/{transcript.uri}.tr"

    # if file already exists, append a timestamp to the filename
    if os.path.exists(output):
        output = f"{output.rsplit('.', 1)[0]}_{int(time.time())}.tr"

    printable_content = []
    if transcript:
        for seg, (language, label, text) in transcript.items():
            start = seg.start
            end = seg.end
            line = f"{start:.3f}|{end:.3f}|{language}|{label}|{text}"
            printable_content.append(line)

    output_content = "\n".join(printable_content)
    with open(output, "w") as file:
        file.write(output_content)
    return output


def load_transcript_from_file(file):
    if not os.path.exists(file):
        raise FileNotFoundError

    with open(file, "r") as f:
        content = f.readlines()

    uri = get_uri_of_file(file)
    transcript = Transcript(uri=uri)
    for line in content:
        start, end, language, label, text = line.split("|")
        transcript[Segment(float(start), float(end))] = (label, text.rstrip(), language)

    return transcript


def save_transcript_as_rttm(transcript: Transcript, output: str):
    pass


def _build_transcript(content, prim_lang, uri):
    transcript = Transcript(uri=uri)

    for line in content:
        label = re.match(r"^([A-Z]{3}) ", line).group(1)
        match = re.search(r"(\d+)_(\d+)", line)
        text = re.search(r"^[A-Z]{3} (.*) \d+_\d+$", line).group(1)
        if match:
            start = int(match.group(1)) / 1000
            end = int(match.group(2)) / 1000
        else:
            raise ValueError(f"No timestamp found in'{line}'")
        language = None
        if prim_lang == "ENG":
            if re.search(r"_SPA", line) or re.search(r"@s", line):
                language = "SPA"
            else:
                language = "ENG"

        if prim_lang == "SPA":
            if re.search(r"_ENG", line) or re.search(r"@s", line):
                language = "ENG"
            else:
                language = "SPA"

        transcript[Segment(start, end)] = (language, label, text)
    return transcript


def _get_speaker_content_from_cha(cha_content):
    speaker_content = []
    label_flag = False
    tab_flag = False
    capture_flag = False
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
            speaker_content.append(line)
        if capture_flag and tab_flag:
            line = re.sub(r"\x15+", "", line)
            line = re.sub(r"\s+", " ", line).lstrip()
            speaker_content[-1] = speaker_content[-1].rstrip() + " " + line

    return speaker_content


def _seperate_content_languages(speaker_content):
    split_language_content = []
    for line in speaker_content:
        label, test = line.split(" ", 1)
        try:
            timestamp = re.search(r"(\d+_\d+)", line).group(1)
            test = re.sub(r"\d+_\d+", "", test).rstrip("\n ")
        except AttributeError:
            print(f"No timestamp found on line: {line}")
            sys.exit(1)

        words = test.split()
        if "@s" not in line:
            split_language_content.append(line)
        else:
            groups = _group_languages(words)
            new_lines = _split_into_lines(groups, label, timestamp)
            split_language_content.extend(new_lines)

    return split_language_content


def _group_languages(words):
    groups = []
    group = ""
    for word in words:
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
    return groups


def _split_into_lines(groups, label, timestamp):
    """
    Segments are used as keys for Transcript hence they need to be unique.
    This function duplicates segments when it splits lines based on
    language, hence small changes to timestamps are needed to make
    the segments slightly different.
    """
    new_lines = []
    delta = 0
    match = re.search(r"(\d+)_(\d+)", timestamp)
    start, end = int(match.group(1)), int(match.group(2))
    for group in groups:
        new_timestamp = f"{start + delta}_{end - delta}"
        new_lines.append(f"{label} ! {group} {new_timestamp}")
        delta += 1
    return new_lines


def _fix_timestamps(content):
    corrected_content = []
    timestamp = None
    for line in content:
        match = re.search(r"(\d+_\d+)", line)
        if match:
            timestamp = match.group(1)
            corrected_content.append(line)
        else:
            corrected_line = line + " ! " + timestamp
            corrected_content.append(corrected_line)
    return corrected_content


def _filter_content(content):
    filtered_content = []
    for line in content:
        filtered_line = re.sub(r"\[- spa\]", "_SPA", line)
        filtered_line = re.sub(r"\[- eng\]", "_ENG", filtered_line)
        filtered_line = re.sub(r"\*([A-Z]{3}):", r"\g<1>", filtered_line)
        filtered_line = re.sub(r"[!?+<>.\"[\]:&()\~,\'-/]", "", filtered_line)
        filtered_line = re.sub(r"= ?[a-z]+", "", filtered_line)
        filtered_line = re.sub(r"[\s]+", " ", filtered_line).rstrip()
        filtered_content.append(filtered_line)
    return filtered_content
