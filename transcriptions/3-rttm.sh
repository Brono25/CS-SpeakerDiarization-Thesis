#!/bin/sh

source "/Users/brono/miniconda3/etc/profile.d/conda.sh"
conda activate base


for file in "/Users/brono/GitHub/katana/transcriptions/2-fix_overlap"/*;do
    python "3-rttm.py" $file
done