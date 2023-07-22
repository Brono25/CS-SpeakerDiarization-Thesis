
from pyannote.core import Segment, Annotation
import sys
import os
import re


input_transcipt = "/Users/brono/GitHub/katana/transcriptions/sastre09_1.txt"
uri = "sastre09_1"
prim_lang = "ENG"

label_pattern = re.compile(r"^([A-Z]{3}) ")
skip_pattern = re.compile(r"\[DEL\]")
timestamp_pattern = re.compile(r"(\d+)_(\d+)")
ref_rttm = Annotation(uri=uri)
lang_rttm = Annotation(uri=uri)

with open(input_transcipt, 'r') as f:
    transcript = f.readlines()



def get_lang_segment(line, start, end, prim_lang, annotation):
    if prim_lang == "ENG":
        if re.search(r"_SPA", line) or re.search(r"@s", line):
            annotation[Segment(start, end)] = "SPA"
        else:
            annotation[Segment(start, end)] = "ENG"
    elif prim_lang == "SPA":
        if re.search(r"_ENG", line) or re.search(r"@s", line):
            annotation[Segment(start, end)] = "ENG"
        else:
            annotation[Segment(start, end)] = "SPA"
    else:
        print("error")


for line in transcript:

    if skip_pattern.match(line):
        print("skipping line <",line.rstrip(),'>')
    
    elif label := label_pattern.match(line).group(1):
        if match := timestamp_pattern.search(line):
            start_sec = float(int(match.group(1)) / 1000)
            end_sec = float(int(match.group(2)) / 1000)
            ref_rttm[Segment(start_sec, end_sec)] = label

            get_lang_segment(line, start_sec, end_sec, prim_lang, lang_rttm)

        else:
            print("Line without timestampe <", line, '>', end='')
    else:
        print("Line without label <", line, '>', end='')



#merge annotations which are within 0.5s
supp_ref_rttm =  ref_rttm.support(collar=0.0) 
supp_lang_rttm = lang_rttm.support(collar=0.0)



with open(f"./ref_rttm/ref_{uri}.rttm", 'w') as f:
    supp_ref_rttm.write_rttm(f)

with open(f"./lang_rttm/lang_{uri}.rttm", 'w') as f:
    supp_lang_rttm.write_rttm(f)