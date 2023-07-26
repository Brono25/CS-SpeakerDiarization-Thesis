from pyannote.core import Annotation, Segment
import os

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

from src.transcript import Transcript
from src.utilities import get_uri_of_file, get_primary_language_of_file, LOG_FILES


import timeit


LABEL_REMOVAL_PATTERN = re.compile(r"^\*([A-Z]{3}): ")
LABEL_REPLACE_PATTERN = re.compile(r"\*([A-Z]{3}):")
SPA_PATTERN = re.compile(r"\[- spa\]")
ENG_PATTERN = re.compile(r"\[- eng\]")
PUNCTUATION_PATTERN = re.compile(r"[!?+<>.\"[\]:&()\~,\'-/]")
NON_SPEECH_PATTERN = re.compile(r"= ?[a-z]+")
TIMESTAMP_PATTERN = re.compile(r"\d+_\d+")
SPACE_PATTERN = re.compile(r"[\s]+")



def convert_cha_to_transcript(cha_file):

    #iterator over labeled cha lines only
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
        for word in line.split(' '):
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
        groups = [x for x in groups if x != '']
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
        log_file =f"{LOG_FILES}/{uri}_changes.log"
        with open(log_file, 'a') as f:
            f.write(line + '\n')

    
    uri = get_uri_of_file(cha_file)
    with open(f"{LOG_FILES}/{uri}_debug.log", 'w') as f:
        pass
    prim_lang = get_primary_language_of_file(uri)
    transcript = Transcript(uri=uri)
    timestamp_pattern = re.compile(r"(\d+)_(\d+)")
    label_pattern = re.compile(r"^\*([A-Z]{3}):")
    start, end = 0, 0
    for i, line in enumerate(_get_labeled_lines(cha_file)):
        
        label = label_pattern.search(line).group(1)
        match = timestamp_pattern.search(line)
        if match:
            start, end = [int(x) for x in match.groups()]
        else:
            start += 1
            end -= 1
        _output_debug_log(uri, f"--------------SECTION {i}--------------")
        _output_debug_log(uri, "ORIGINAL:\n" + '\t\t' + line + "\nEDITED:")
        filtered_line = _filter_line(line)
        monolingual_lines = _group_languages(filtered_line)
        delta = 0
        for mono_line in monolingual_lines:
            language = _detect_language(mono_line, prim_lang)
            text = re.sub(r"_SPA|_ENG", "", mono_line).lstrip().rstrip()
            start_sec, end_sec  = (start + delta) / 1000, (end - delta)  / 1000
            transcript[Segment(start_sec, end_sec )] = (label, language, text)
            delta += 1

            _output_debug_log(uri, f"\t\t{label} {language} {text} {start_sec} {end_sec}")
        _output_debug_log(uri, '\n')
    
    return transcript
    

start = timeit.default_timer()

cha_file = "/Users/brono/GitHub/CS-SpeakerDiarization-Thesis/cha_files/sastre09.cha"
convert_cha_to_transcript(cha_file)



end = timeit.default_timer()
print(f"Execution time: {end - start} seconds")






    expected_output = Transcript(uri=uri)
    expected_output[Segment(0.47, 2.107)] = ("KAY", "ENG", "! so")
    expected_output[Segment(0.471, 2.106)] = ("KAY", "SPA", "! sí@s hay@s un@s")
    expected_output[Segment(0.472, 2.105)] = ("KAY", "ENG", "! range")
    expected_output[Segment(0.473, 2.104)] = ("KAY", "SPA", "! ahí@s")
    expected_output[Segment(2.180, 2.490)] = ("VAL", "ENG", "mhm")
    expected_output[Segment(2.181, 4.321)] = ("KAY", "SPA", "_SPA donde los policías e practican")
    expected_output[Segment(4.293, 7.486)] = ("KAY", "SPA", "! y@s y@s la@s gente@s que@s están@s los@s")
    expected_output[Segment(4.294, 7.485)] = ("KAY", "ENG", "! trainees the police trainees")
    expected_output[Segment(7.387, 8.618)] = ("KAY", "ENG", "they do it every day")
    expected_output[Segment(8.575, 10.783)] = ("KAY", "ENG", "so when you come here dont be afraid if you hear it")
    expected_output[Segment(11.095, 12.193)] = ("KAY", "ENG", "because you know theyre practicing")
    expected_output[Segment(12.064, 14.786)] = ("VAL", "ENG", "yeah yeah they have to put these earphones")
    expected_output[Segment(14.900, 16.643)] = ("VAL", "SPA", "_SPA porque si no se puede quedar uno sordo")
    expected_output[Segment(16.433, 16.794)] = ("KAY", "ENG", "really")