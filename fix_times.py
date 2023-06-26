



import re

file = "/Users/brono/GitHub/katana/transcripts/herring06.txt"
out_path = "/Users/brono/Desktop/thesis-dataset.tmp/time-fixed-trans"
filename = re.search(r".*/(.*)\.txt", file).group(1)



def verify(content):
    prev_start = 0
    start = None
    for line in content:
        match = re.search(r"(\d+)_\d+", line)

        if match:
            start = int(match.group(1))
        if not start:
            continue
        if start < prev_start:
            print("Error")
        prev_start = start


with open(file, 'r') as f:
    content = f.readlines()

prev_speaker, speaker = None, None
prev_start, prev_end = 0, 0
start, end = 1, 0
prev_line = None
i = 0

try:
    while(content[i]):
        if i == 233:
            pass
        increment = True
        line = content[i]
        match = re.search(r"(\d+)_(\d+)", line)
        if match:
            start, end = map(int, match.groups())
        match = re.search(r"\*([A-Z]{3}):", line)
        if match:
            speaker = match.group(1)

        if prev_speaker == speaker and start <= prev_end:
            new_time = f"{prev_start}_{end}"
            new_line = prev_line + re.search(r"\*[A-Z]{3}:(.*)",line).group(1)
            new_line = re.sub(r"\d+_\d+\n?", "", new_line) + new_time + '\n'
            content[i - 1] = new_line
            del content[i]
            increment = False

        prev_speaker = speaker
        prev_end = end
        prev_start = start
        prev_line = line
        if increment:
            i += 1



except IndexError:
    pass

with open(f"{out_path}/{filename}_fixed.txt", 'w') as f:
    
    for line in content:
        f.write(line)

