#!/bin/sh

source "/Users/brono/miniconda3/etc/profile.d/conda.sh"
conda activate thesis-env

for pyfile in test_bench/*.py; do
    python $pyfile || exit 1
 
done


