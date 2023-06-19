#!/bin/bash

#PBS -l select=1:ncpus=1:mem=4gb
#PBS -l walltime=01:00:00


FILE="eng_mp3/zeledon02.mp3"

cd "$HOME/data"

python diarization.py "$HOME/data/$FILE"