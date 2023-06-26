

import sys
import re
from collections import defaultdict


CHA_PATH = "/Users/brono/Desktop/thesis-dataset.tmp/cha"

file = sys.argv[1]
file = "/Users/brono/GitHub/katana/cha/herring06.cha"

# Ensure a command line argument has been provided
if len(sys.argv) < 2:
    print("Please provide a CHAT file")
    sys.exit(1)

try:
    with open(file, 'r') as f:
        content = f.readlines()

except FileNotFoundError:
    print(f"No such file or directory: '{file}'")
    sys.exit(1)




# Filter CHA file to the relevent details
filter_content = []
start_capture = False
prim_lang = None
sec_lang = None
remove_chars = "[\x15\n<>&+/\'(.)?\",]"

# Filter the content
for line in content:

    match = re.search(r"1287681_1290003", line)
    if match:
        match = 0
        pass

    match = re.match(r"@Languages:	([a-z]{3}), ([a-z]{3})", line)
    if match:
        prim_lang = match.group(1)
        sec_lang = match.group(2)

    filter_line = re.sub(remove_chars, "", line).replace('\t', ' ')

    if line[0] == '*':
        start_capture = True
        filter_content.append(filter_line)
        continue
    if line[0] == '%':
        start_capture = False
    
    if start_capture is True:
        filter_content[-1] += filter_line



if not prim_lang and sec_lang:
    print("Invalid cha file")
    sys.exit(1)




# count code-switching percent
speaker_dict = defaultdict(lambda: defaultdict(int))

for i, line in enumerate(filter_content):
    speaker = re.match(r"\*([A-Z]+):", line).group(1)

    bare_line = re.sub("\[- spa\]", "", line)
    bare_line = re.sub("=[a-z]+", "", bare_line)
    bare_line = re.sub("\*[A-Z]+:", "", bare_line)
    bare_line = re.sub("~[a-z]+", "", bare_line)
    bare_line = re.sub("[0-9]+_[0-9]+", "", bare_line)
    bare_line = re.sub("[?\".\[\]()'!=]", "", bare_line)


    if re.search(r"\[- spa\]", line):
        speaker_dict[speaker]['spa'] += len(line.split())
    
    elif re.search(r"\[- eng\]", line):
        speaker_dict[speaker]['eng'] += len(line.split())

    elif prim_lang == 'eng':
        spa = re.findall(r'[a-zA-Z]+@s', bare_line)
        eng = re.sub('[a-zA-Z]+@s', '', bare_line).split(' ')
        eng = [x for x in eng if x != '']
        speaker_dict[speaker]['eng'] += len(eng)
        speaker_dict[speaker]['spa'] += len(spa)

    else:
        eng = re.findall(r'[a-zA-Z]+@s', bare_line)
        spa = re.sub('[a-zA-Z]+@s', '', bare_line).split(' ')
        spa = [x for x in spa if x != '']
        speaker_dict[speaker]['eng'] += len(eng)
        speaker_dict[speaker]['spa'] += len(spa)
    
     

data = []
for speaker, languages in speaker_dict.items():
    english_count = languages.get('eng', 0)
    spanish_count = languages.get('spa', 0)

    if prim_lang == 'eng':
        if english_count > 0:  # avoid dividing by zero
            ratio = (spanish_count / english_count) * 100
    if prim_lang == 'spa':
        if spanish_count > 0:  # avoid dividing by zero
            ratio = (english_count / spanish_count) * 100

    if prim_lang == 'eng':
        data.append(f"Speaker: {speaker}, English word count: {english_count}, Spanish word count: {spanish_count}, Spanish to English Ratio: {ratio:.2f}%")
    else:
        data.append(f"Speaker: {speaker}, Spanish word count: {spanish_count}, English word count: {english_count}, English to Spanish Ratio: {ratio:.2f}%")



# Construct filename
file_name = re.search(r'([^/]*)\.cha$', file).group(1)
output_file = f'transcripts/{file_name}.txt'

# Output a filtered transcript
with open(output_file, 'w') as f:

    for line in data:
        f.write(line + '\n') 
    f.write('\n') 
    for line in filter_content:
        f.write(line + '\n')  




