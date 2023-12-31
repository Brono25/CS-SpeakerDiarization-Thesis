import os
import copy
import re
import sys

LABEL_REMOVAL_PATTERN = re.compile(r"^\*([A-Z]{3}): ")
LABEL_REPLACE_PATTERN = re.compile(r"\*([A-Z]{3}):")
SPA_PATTERN = re.compile(r"\[- spa\]")
ENG_PATTERN = re.compile(r"\[- eng\]")
PUNCTUATION_PATTERN = re.compile(r"[!?+<>.\"[\]:&()\~,\'-/]")
NON_SPEECH_PATTERN = re.compile(r"= ?[a-z]+")
TIMESTAMP_PATTERN = re.compile(r"\d+_\d+")
SPACE_PATTERN = re.compile(r"[\s]+")



def reduce_transcript(transcript: [], support=0.25) -> []:
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
    

    tr = copy.deepcopy(transcript)
    result = [tr.pop(0)]
    while tr:
        t_start, t_end, t_label, t_language, t_text = tr[0]

        combined = False
        for i in range(len(result) - 1, -1, -1):
            seg = result[i]
            r_start, r_end, r_label, r_language, r_text = seg


            if t_label == r_label and t_language != r_language:
                result.append(tr.pop(0))
                combined = True
                break

            if (r_label == t_label and r_language == t_language and t_start - r_end <= support):
                combined_seg = _combine_segments(seg, tr[0])
                result[i] = combined_seg
                tr.pop(0)
                combined = True
                break

        if not combined:
            result.append(tr.pop(0))

    return result



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




def convert_cha_to_transcript_str_format(cha_file: str, uri: str, prim_lang: str) -> []:
    """
    Converts CHAT (.cha) formatted file into a Transcript.

    Args:
        cha_file (str): The path to the CHAT (.cha) file to be converted.

    Returns:
        Transcript: The generated Transcript object containing labels, text and language.

    Note:
        A log indicating the steps involved in conversion is created for debugging purposes.
    """
    log_output = os.path.dirname(cha_file)
    
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

    def _detect_language(line, prim_lang, unfiltered_line=None):
        if "_SPA" in line:
            return "SPA"
        if "_ENG" in line:
            return "ENG"
        if "@s" in line and "[- spa]" in unfiltered_line:
            return "ENG"
        if "@s" in line and "[- eng]" in unfiltered_line:
            return "SPA"

        if "@s" in line and prim_lang == "ENG":
            return "SPA"
        if "@s" in line and prim_lang == "SPA":
            return "ENG"
        if "[- spa]" in unfiltered_line:
            return "SPA"
        if "[- eng]" in unfiltered_line:
            return "ENG"
        return prim_lang



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
        log_file = f"{log_output}/{uri}_debug.log"
        with open(log_file, "a") as f:
            f.write(line + "\n")

    with open(f"{log_output}/{uri}_debug.log", "w") as f:
        pass

    transcript = []
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
        
            language = _detect_language(mono_line, prim_lang, unfiltered_line=line)
            text = re.sub(r"_SPA|_ENG", "", mono_line).lstrip().rstrip()
            start_sec, end_sec = (start + delta) / 1000.0, (end + delta) / 1000.0

            # tag lines which have been split or timestamps added with a '!'
            if len(monolingual_lines) > 1 or missing_timestamp_flag:
                text = f"!{text}"
                missing_timestamp_flag = False
            delta += 10


            transcript.append([start_sec,end_sec,label,language, text])
       
            _output_debug_log(
                uri,
                f"\t\t\t({start_sec:.3f}, {end_sec:.3f})\t{label} {language} {text} ",
            )

        _output_debug_log(uri, "\n")

    return transcript


def write_transcript_format_to_file(trancript, output):
    with open(output, 'w') as f:
        for start, end, label, lang, text in trancript:
            line = f"{start:.3f}|{end:.3f}|{label}|{lang}|{text}" 
            f.write(line + '\n')