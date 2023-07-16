
from pyannote.core import Segment, Annotation
import sys
import os
import re


def get_file_path(default_file):
    if len(sys.argv) > 1:
        file_path = sys.argv[1] 
        if os.path.isfile(file_path):
            return file_path
        else:
            raise ValueError(f"The provided argument {file_path} is not a valid file.")
    else:
        if os.path.isfile(default_file):
            return default_file
        else:
            raise ValueError(f"The default file {default_file} does not exist.")
        

def change_root_dir():
    katana_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(katana_dir)
    os.chdir(root_dir)



if __name__ == "__main__":

    change_root_dir()
    file = get_file_path("./transcriptions/sastre09_1.txt")
    output_rttm = re.search(r"^.*/(.*)\.txt$", file).group(1)
    label_pattern = re.compile(r"^\*([A-Z]{3}):")
    skip_pattern = re.compile(r"\[DEL\]")
    timestamp_pattern = re.compile(r"(\d+)_(\d+)")


    ref_rttm = Annotation(uri=output_rttm)


    with open(get_file_path(file), 'r') as f:
        transcript = f.readlines()

    for line in transcript:

        if skip_pattern.match(line):
            print("skipping line <",line.rstrip(),'>')
        
        elif label := label_pattern.match(line).group(1):
            if match := timestamp_pattern.search(line):
                start_sec = float(int(match.group(1)) / 1000)
                end_sec = float(int(match.group(2)) / 1000)
                
                # Create annotation segment
                ref_rttm[Segment(start_sec, end_sec)] = label

            else:
                print("Line without timestampe <", line, '>', end='')
        else:
            print("Line without label <", line, '>', end='')

    #merge annotations which are within 0.5s
    supp_ref_rttm =  ref_rttm.support(collar=0.5) 

with open(f"./ref_rttm/ref_{output_rttm}.rttm", 'w') as f:
    supp_ref_rttm.write_rttm(f)
