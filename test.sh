#!/bin/bash

DATA_PATH='/srv/scratch/z5146619/'

for wav_file in "${DATA_PATH}/eng_wav/"* "${DATA_PATH}/spa_wav/"*; do

    filename=$(basename $wav_file)
    echo $wav_file

done

