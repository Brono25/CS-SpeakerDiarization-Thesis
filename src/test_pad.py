from pyannote.core import Annotation, Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.transcript import Transcript


"""
This is an area to test code snippets
"""

ref = Transcript(uri="test")
ref[Segment(0, 10)] = ("ENG", "A", "Hello World")
ref[Segment(8, 25)] = ("ENG", "B", "Goodbye World")
ref[Segment(25, 35)] = ("SPA", "A", "si")

ref.save_as_rttm()