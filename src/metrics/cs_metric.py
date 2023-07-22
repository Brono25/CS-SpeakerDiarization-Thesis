from pyannote.core import Segment
from pyannote.metrics.base import BaseMetric

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.transcription.transcript import Transcript  # noqa: E402


class CSMetric(BaseMetric):
    """Code-Switching (CS) speech metrics"""

    def m_index(self):
        pass

    def language_entropy(self):
        pass

    def i_index(self):
        pass

    def burstiness(self):
        pass

    def span_entropy(self):
        pass

    def memory(self):
        pass


# Initialize a transcript
trans = Transcript(uri="test")

# Add a segment with label and text
trans[Segment(0, 1)] = ("A", "Hello World!")


# Iterate over segments
for seg in trans.itersegments():
    # Fetch label and text for each segment
    label = trans[seg]
    text = trans.get_text(seg)
    print(f"Segment: {seg}, Label: {label}, Text: {text}")
