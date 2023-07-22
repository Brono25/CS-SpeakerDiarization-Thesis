#!/bin/sh

file="raw_sastre09_part1.txt"
o_file="filtered_sastre09_part1.txt"

cat $file | sed -E 's/\[- spa\]/ _SPA /' | 
            sed -E 's/\[- eng\]/ _ENG  /'| 
            sed -E 's/\*([A-Z]{3}):/\1 /'|
            tr -d '!?+<>./\"[]:&()~,-'    |
            tr -d "'"|
            sed -E 's/= ?[a-z]+//g' |
            tr -s ' ' >  $o_file