#!/bin/sh

source "/Users/brono/miniconda3/etc/profile.d/conda.sh"
conda activate base


ROOT_PATH="/Users/brono/Desktop/thesis-dataset.tmp/cha"


while IFS= read -r line
do
  echo "Processing $line" 
  python "1-speech.py" "$ROOT_PATH/$line"
done < "index.txt"
