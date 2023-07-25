from pyannote.core import Annotation, Segment
import os

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.transcript import (  # noqa: E402
    Transcript,
    cha_to_transcript,
    save_transcript_to_file,
)  # noqa: E402
from src.utilities import ( # noqa: E402
    ROOT_DIR,
    CHA_FILES_DIR,
    debug_transcript_comparison,
)  


# Process files one at a time
uri = "sastre09"
cha_file = f"{CHA_FILES_DIR}/{uri}.cha"
if not os.path.isfile(cha_file):
    print(f"{cha_file} not found.")


# Create Transcript and RTTM files
transcript = cha_to_transcript(cha_file=cha_file)
#debug_transcript_comparison(transcript)
# save_transcript_to_file(transcript=transcript)
