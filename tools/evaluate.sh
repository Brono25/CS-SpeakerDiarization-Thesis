

TRUTH_PATH="./ref_rttm"
OUT_PATH="./output_rttm"


der () {
	truth_file="$1"
	out_file="$2"
	"/Volumes/T7/SCTK/src/md-eval/md-eval.pl" -c 0.5 -o -r "$truth_file" -s "$out_file" 
}



der "./ref_rttm/o_sastre09_part1_ref.rttm" "/Users/brono/GitHub/database/output_rttm/p_mono-sastre09_part1_output.rttm"

#der "/Users/brono/GitHub/database/output_rttm/r.rttm" "/Users/brono/GitHub/database/output_rttm/o.rttm"