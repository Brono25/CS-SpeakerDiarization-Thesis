#!/bin/sh

source /Users/brono/miniconda3/etc/profile.d/conda.sh
conda  activate pydub-audio
for file in "/Users/brono/GitHub/katana/time-fixed-trans"/*; do

    python convert_2_rttm.py "$file" || echo error
done

