#!/bin/sh


source "/Users/brono/miniconda3/etc/profile.d/conda.sh"
conda activate base

DIR="/Users/brono/GitHub/katana/transcriptions/1-speech"
DIR="/Users/brono/GitHub/katana/transcriptions/2-fix_overlap"

for file in "$DIR"/*.txt; do
    cat $file |grep -E -v '^\*[A-Z]{3}:' && echo $file && exit 1
done
