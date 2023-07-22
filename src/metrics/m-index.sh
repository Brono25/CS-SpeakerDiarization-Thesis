#!/bin/sh

source "/Users/brono/miniconda3/etc/profile.d/conda.sh"
conda activate base


transcript_dir="/Users/brono/GitHub/katana/transcriptions/1-speech"


for file in $transcript_dir/*; do

python "m-index.py" $file

done