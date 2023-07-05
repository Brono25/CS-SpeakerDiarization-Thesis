
from pyannote.core import Annotation, Segment
from pyannote.metrics.diarization import DiarizationErrorRate

# Initialize the metric
metric = DiarizationErrorRate()

# Function to parse RTTM file
def load_rttm(rttm_file):
    annotation = Annotation()
    with open(rttm_file, 'r') as file:
        for line in file:
            fields = line.strip().split()
            start_time = float(fields[3])
            duration = float(fields[4])
            speaker_id = fields[7]
            segment = Segment(start_time, start_time + duration)
            annotation[segment] = speaker_id
    return annotation

# Load reference and hypothesis from RTTM files
ref_uri = '/Users/brono/GitHub/database/ref_rttm/o_sastre09_part1_ref.rttm'
hyp_uri = '/Users/brono/GitHub/database/hypo_rttm/p_mono-sastre09_part1_output.rttm'

reference = load_rttm(ref_uri)
hypothesis = load_rttm(hyp_uri)

# Compute the diarization error rate
error_rate = metric(reference, hypothesis)

print(f"Diarization Error Rate: {error_rate:.2%}")
