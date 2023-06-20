

import sys
import re


# Ensure a command line argument has been provided
if len(sys.argv) < 2:
    print("Please provide a file name as a command line argument.")
    sys.exit(1)

try:
    with open(sys.argv[1], 'r') as f:
        content = f.readlines()

except FileNotFoundError:
    print(f"No such file or directory: '{sys.argv[1]}'")
    sys.exit(1)


# Filter CHA file to the relevent details
filter_content = []
start_capture = False
for line in content:
    if line[0] == '*':
        start_capture = True
        filter_content.append(line.replace('\t', ' '))
        continue
    if line[0] == '%':
        start_capture = False
    
    if start_capture is True:
        filter_content[-1] += line.replace('\t', ' ')


# Construct filename
file_name = re.search(r'([^/]*)\.cha$', sys.argv[1]).group(1)
output_file = f'transcripts/{file_name}.txt'

# Extract a filtered transcript
with open(output_file, 'w') as f:
    for line in filter_content:
        f.write(line)  




#construct the RTTM file
segment_type='SPEAKER'
channel_ID = 1 
turn_onset = None
turn_duration = None
spkr_name = None


with open(f"truth_rttm/{file_name}_truth.rttm", 'w') as file:
    for item in filter_content:
        match = re.search(r'(\d+)_(\d+)', item)
        if match:
            start_sec, end_sec = int(match.group(1)) / 1000.0 , int(match.group(2)) / 1000.0
        else:
            print('Error - no time stamp found')
            sys.exit(1)
        spkr_name = re.search(r'^\*([A-Z]+)', item).group(1)
        turn_onset = round(start_sec, 3)
        turn_duration = round(end_sec - start_sec, 3)
        rttm_line = (f"{segment_type} {file_name} {channel_ID} {turn_onset} {turn_duration} "
                    f"<NA> <NA> {spkr_name} <NA> <NA>")
        file.write(rttm_line + '\n')
