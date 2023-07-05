


import sys
import re

file = "/Users/brono/GitHub/katana/test-files/test-overlap.txt"
file = "/Users/brono/GitHub/katana/transcriptions/1-speech/1-herring08.txt"
file = sys.argv[1]
out_path = "/Users/brono/GitHub/katana/transcriptions/2-fix_overlap"
filename = re.search(r".*/(.*)\.txt", file).group(1)



def get_speaker_and_times(line):
    match = re.search(r"(\d+)_(\d+)", line)
    if match:
        start, end = map(int, match.groups())
    match = re.search(r"\*([A-Z]{3}):", line)
    if match:
        speaker = match.group(1)
    return speaker, start, end



def is_overlap(prev_speaker, speaker, start, prev_end):
    return prev_speaker == speaker and start <= prev_end
        

def merge_lines(content, i, prev_start, end):
    new_time = f"{prev_start}_{end}"
    new_line = prev_line + re.search(r"\*[A-Z]{3}:(.*)",line).group(1)
    new_line = re.sub(r"\d+_\d+\n?", "", new_line) + new_time
    new_line = re.sub(r"[ ]+", " ", new_line)
    new_line = re.sub(r"\n", "", new_line) + '\n'
    content[i - 1] = new_line
    del content[i]
    return False, new_line


with open(file, 'r') as f:
    content = f.readlines()

prev_speaker, speaker = None, None
prev_start, prev_end = 0, 0
start, end = 1, 0
prev_line = None
i = 0



try:
    while(content[i]):

        increment = True
        line = content[i]
        speaker, start, end = get_speaker_and_times(line)
        if is_overlap(prev_speaker, speaker, start, prev_end):
            increment, prev_line = merge_lines(content, i, prev_start, end)
        prev_end = end
        if increment:
            i += 1
            prev_start = start
            prev_line = line
            prev_speaker = speaker
except IndexError:
    pass


with open(f"{out_path}/{filename}_fixed.txt", 'w') as f:
    
    for line in content:
        f.write(line)


