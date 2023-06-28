

import sys
import re

file = sys.argv[1]
#file = "/Users/brono/GitHub/katana/time-fixed-trans/herring06_fixed.txt"
out_path = "/Users/brono/GitHub/katana/transcriptions/3-rttm"
# Ensure a command line argument has been provided

with open(file, 'r') as f:
    content = f.readlines()



# Construct filename
file_name = re.match(r'.*/(.*)_fixed.txt$', file).group(1)
output_file = f'{out_path}/{file_name}_truth.rttm'
print(f"converting {file_name}")


#construct the RTTM file
segment_type='SPEAKER'
channel_ID = 1 
turn_onset = None
turn_duration = None
spkr_name = None


with open(output_file, 'w') as file:
    for item in content:
        match = re.search(r'(\d+)_(\d+)', item)
        if match:
            start_sec, end_sec = int(match.group(1)) / 1000.0 , int(match.group(2)) / 1000.0
        else:
            continue
        spkr_name = re.search(r'^\*([A-Z]+)', item).group(1)
        turn_onset = round(start_sec, 3)
        turn_duration = round(end_sec - start_sec, 3)
        rttm_line = (f"{segment_type} {file_name} {channel_ID} {turn_onset} {turn_duration} "
                    f"<NA> <NA> {spkr_name} <NA> <NA>")
        file.write(rttm_line + '\n')
