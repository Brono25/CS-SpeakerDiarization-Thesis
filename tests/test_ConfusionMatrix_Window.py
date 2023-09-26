from pyannote.core import Annotation, Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

from src.functions.confusion_matrix import Window


def test_window_bounds():
    extent = 20.0
    segments = [Segment(0, 1), Segment(1, 2), Segment(10, 18)]
    expected_lagging_segments = [Segment(0, 0), Segment(0, 1), Segment(5, 10)]
    expected_leading_segments = [Segment(1, 6), Segment(2, 7), Segment(18, 20)]

    for i, segment in enumerate(segments):
        window = Window(segment=segment, extent=extent)
        assert expected_leading_segments[i] == window.leading_segment
        assert expected_lagging_segments[i] == window.lagging_segment



