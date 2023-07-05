#!/bin/sh

source "/Users/brono/miniconda3/etc/profile.d/conda.sh"
conda activate thesis

#construct ref_file.txt name
ref_file() {
    filename=$(basename -- $1)
    filename=${filename##*_}
    ref_file="./test_bench/test_files/ref/ref_$filename"
    echo "$ref_file"
}

o_file() {
    filename=$(basename -- $1)
    filename=${filename##*_}
    o_file="./test_bench/test_files/output/o_$filename"
    echo "$o_file"
}

test_transcriber() {
    test_file="$1"
    ref_file=$(ref_file $test_file)
    o_file=$(o_file $test_file)
    filename=$(basename -s '.txt' -- $o_file)
    python ."/tools/transcriber.py" "$test_file" -o "./test_bench/test_files/output/"
    diff "$ref_file" "$o_file" && echo "PASS - $filename"
}


test_file="./test_bench/test_files/test/test_herring09.txt"

test_transcriber "./test_bench/test_files/test/test_herring09.txt"
test_transcriber "./test_bench/test_files/test/test_sastre02.txt"
test_transcriber "./test_bench/test_files/test/test_zeledon06.txt" 