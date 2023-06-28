


TRUTH_PATH="/Users/brono/GitHub/katana/transcriptions/3-rttm"
OUT_PATH="/Users/brono/GitHub/katana/output_rttm"


der () {
	truth_file="$1"
	out_file="$2"
	"/Volumes/T7/SCTK/src/md-eval/md-eval.pl" -c 0.5 -o -r "$truth_file" -s "$out_file" 
}



der "/Users/brono/GitHub/katana/transcriptions/3-rttm/1-herring09_truth.rttm" "/Users/brono/GitHub/katana/output_rttm/herring09_output.rttm"