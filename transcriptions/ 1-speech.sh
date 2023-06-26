#!/bin/sh


ROOT_PATH="/Users/brono/GitHub/katana/cha"

source "/Users/brono/miniconda3/etc/profile.d/conda.sh"
conda activate base
while IFS= read -r line
do
  python "1-speech.py" "$ROOT_PATH/$line"
done < "index.txt"
