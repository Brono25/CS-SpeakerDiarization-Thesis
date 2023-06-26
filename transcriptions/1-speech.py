
import sys
import re
import os

file = sys.argv[1]
#file =  "/Users/brono/GitHub/katana/cha/herring06.cha"
output_dir = "/Users/brono/GitHub/katana/transcriptions/1-speech"
file_name = re.search(r".*/(.*)\.cha", file).group(1)
output_file = f"/Users/brono/GitHub/katana/transcriptions/1-speech/1-{file_name}.txt"


with open(file, 'r') as f:
    content = f.readlines()

speech_content = []
speech_flag = False
for i, line in enumerate(content):

    if re.search(r'\|', line):
        continue    
    if re.search(r"^\*[A-Z]{3}:", line):
        speech_flag = True
        speech_content.append(line)

    elif speech_flag:
        speech_content[-1] += line

    time_stamps = re.search(r"\x15(\d+_\d+)\x15", line)
    if time_stamps:
        time_stamps = time_stamps.group(1)
        speech_flag = False



corrupted = False
with open(output_file, 'w') as f:
    for line in speech_content:
        f.write(line)
        if not re.search(r"\x15(\d+_\d+)\x15", line):
            f.write("\n\n--------------------------------Error Missing Timestamp--------------------------------\n\n")
            corrupted = True

if corrupted:
    os.rename(output_file, f"{output_file}.err")
