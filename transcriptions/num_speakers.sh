#!/bin/sh


CHA_DIR="/Users/brono/Desktop/thesis-dataset.tmp/cha"

for file in "$CHA_DIR"/*;do
cat $file |grep "@Participants:" | cut -d':' -f2 | sed 's/,/\n/g'|tr '\t ' ' '
done | sort -u |grep -v 'OSE'|wc -l
