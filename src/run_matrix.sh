#!/bin/sh

cd /Users/brono/GitHub/CS-SpeakerDiarization-Thesis/src

files=(
"/Users/brono/GitHub/cs-dataset/code-switched/sastre01/sastre01.tr"
"/Users/brono/GitHub/cs-dataset/code-switched/herring06/herring06.tr"
"/Users/brono/GitHub/cs-dataset/code-switched/herring07/herring07.tr"
"/Users/brono/GitHub/cs-dataset/code-switched/herring08/herring08.tr"
"/Users/brono/GitHub/cs-dataset/code-switched/herring10/herring10.tr"
"/Users/brono/GitHub/cs-dataset/code-switched/herring13/herring13.tr"
"/Users/brono/GitHub/cs-dataset/code-switched/sastre11/sastre11.tr"
"/Users/brono/GitHub/cs-dataset/code-switched/zeledon04/zeledon04.tr"
"/Users/brono/GitHub/cs-dataset/code-switched/sastre06/sastre06.tr"
"/Users/brono/GitHub/cs-dataset/code-switched/sastre09/sastre09.tr"
"/Users/brono/GitHub/cs-dataset/code-switched/zeledon08/zeledon08.tr"
"/Users/brono/GitHub/cs-dataset/code-switched/zeledon14/zeledon14.tr"
)

python test.py "${files[@]}"
