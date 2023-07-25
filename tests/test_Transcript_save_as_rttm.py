import os
import pytest
from pyannote.core import Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.transcript import load_transcript_from_file, cha_to_transcript, Transcript  # noqa: E402
from src.utilities import TEST_FILES, get_uri_of_file, debug_transcript_comparison


t = cha_to_transcript(f"{TEST_FILES}/test_sastre09.cha")

debug_transcript_comparison(t)