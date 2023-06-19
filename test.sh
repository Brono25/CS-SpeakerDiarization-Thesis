#!/bin/bash

#PBS -N mp3_2_wav
#PBS -l select=1:ncpus=4:ngpus=1:mem=16gb
#PBS -l walltime=01:00:00
#PBS -M b.ashford@student.unsw.edu.au
#PBS -m ae
#PBS -j oe
#PBS -o /home/z5146619/katana/output_rttm

# load necessary modules
module load ffmpeg || exit 1

cd $PBS_O_WORKDIR

DEST_PATH_ENG="/home/z5146619/data/eng_wav"
DEST_PATH_SPA="/home/z5146619/data/spa_wav"

for file in /home/z5146619/data/eng_mp3/* ; do
    ext="${file##*.}"
    ext="${ext,,}"
    if [[ $ext == 'mp3' ]]; then
        filename=$(basename -- "$file" .mp3)
        echo "Processing $file"
        echo ffmpeg -i "$file" "$DEST_PATH_ENG/${filename}.wav" || echo "Failed to convert $file"
    fi
done

for file in /home/z5146619/data/spa_mp3/* ; do
    ext="${file##*.}"
    ext="${ext,,}"
    if [[ $ext == 'mp3' ]]; then
        filename=$(basename -- "$file" .mp3)
        echo "Processing $file"
        echo ffmpeg -i "$file" "$DEST_PATH_SPA/${filename}.wav" || echo "Failed to convert $file"
    fi
done
