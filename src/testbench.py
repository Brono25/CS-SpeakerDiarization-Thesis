from pyannote.core import Annotation, Segment
import os

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

from src.transcript import Transcript
from src.utilities import get_uri_of_file, get_primary_language_of_file, LOG_FILES

