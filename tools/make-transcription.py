import sys
import re
import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("file", help="Input file")
parser.add_argument("-o", "--output", help="Output directory")
args = parser.parse_args()

file = args.file

filename = re.search(r".*/(.*)\.cha$", file).group(1)

if args.output:
    if not os.path.exists(args.output):
        os.makedirs(args.output)
    output = os.path.join(args.output, f"o_{filename}.txt")
else:
    output = f"../transcriptions/o_{filename}.txt"

with open(file, 'r') as f:
    content = f.readlines()

speaker_lines = []
label_flag = False
tab_flag = False
capture_flag = False
for line in content:

    label_flag = bool(re.match(r"^\*[A-Z]{3}:", line))
    tab_flag = bool(re.match(r'\t', line))

    if label_flag:
        capture_flag = True
    
    if not label_flag and not tab_flag:
        capture_flag = False

    if capture_flag and label_flag:
        line = re.sub(r'\t', '', line)
        line = re.sub(r'\x15', '', line)
        speaker_lines.append(line)
    if capture_flag and tab_flag:
        line = re.sub(r'\x15', '', line)
        line = re.sub(r'\t', '', line)
        speaker_lines[-1] = speaker_lines[-1].rstrip() + ' ' + line

with open(output, 'w') as f:
    for line in speaker_lines:
        f.write(line)
