
truth_file="$1"
out_file="$2"

TRUTH_PATH="/Users/brono/GitHub/katana/truth_rttm"
OUT_PATH="/Users/brono/GitHub/katana/output_rttm"



for out_rttm in "$OUT_PATH/"* ; do

	file_suffix=${out_rttm##*.}
	if [[ $file_suffix != 'rttm' ]]; then
		continue
	fi

	out_rttm_filename=${out_rttm##*/}
	filename=${out_rttm_filename%%_*}
	truth_rttm=$TRUTH_PATH/${filename}_truth.rttm

	/Volumes/T7/SCTK/src/md-eval/md-eval.pl -1 -r $truth_file -s $out_file || grep 'DER'
	

done

