#!/bin/sh



for file in cha/*; do


	if [[ ${file##*.} == 'cha' ]]; then
		python make_transcript.py $file || echo "Processed ${file##*/} failed"
	fi
	
done