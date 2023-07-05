#!/bin/sh

source "/Users/brono/miniconda3/etc/profile.d/conda.sh"
conda activate base

SOURCE="/Users/brono/GitHub/katana/transcriptions/1-speech"

for file in $SOURCE/*.txt;do
    python "2-fix_overlap.py" $file
done