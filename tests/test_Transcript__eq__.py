import pytest
from pyannote.core import Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local import
from src.transcript import Transcript  # noqa: E402


def test_transcript_equality():
    # Creating two transcripts with identical content
    a = Transcript(uri="test")
    a[Segment(0, 1)] = ("A", "Hello World!", "ENG")
    a[Segment(1, 2)] = ("B", "Hola mundo", "SPA")

    b = Transcript(uri="test")
    b[Segment(0, 1)] = ("A", "Hello World!", "ENG")
    b[Segment(1, 2)] = ("B", "Hola mundo", "SPA")

    # Test that they are considered equal
    assert a == b

    # Creating two transcripts with different uri's but same content
    a = Transcript(uri="")
    a[Segment(0, 1)] = ("A", "Hello World!", "ENG")
    a[Segment(1, 2)] = ("B", "Hola mundo", "SPA")

    b = Transcript(uri="test")
    b[Segment(0, 1)] = ("A", "Hello World!", "ENG")
    b[Segment(1, 2)] = ("B", "Hola mundo", "SPA")

    # Test that they are considered unequal
    assert a != b

    # Creating two transcripts with same uri's but different content
    a = Transcript(uri="test")
    a[Segment(0, 1)] = ("A", "Hello World!", "ENG")
    a[Segment(1, 2)] = ("B", "Hola mundo", "SPA")

    b = Transcript(uri="test")
    b[Segment(0, 1)] = ("B", "Hello World!", "ENG")
    b[Segment(1, 2)] = ("B", "Hola mundo", "SPA")

    # Test that they are considered unequal
    assert a != b
