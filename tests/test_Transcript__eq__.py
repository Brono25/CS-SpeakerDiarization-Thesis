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
    spkr1 = "A"
    spkr2 = "B"
    # Creating two transcripts with identical content
    a = Transcript(uri="test")
    a[Segment(0, 1)] = (spkr1, "ENG", "Hello World!")
    a[Segment(1, 2)] = (spkr2, "SPA", "Hola mundo")

    b = Transcript(uri="test")
    b[Segment(0, 1)] = (spkr1, "ENG", "Hello World!")
    b[Segment(1, 2)] = (spkr2, "SPA", "Hola mundo")

    label, lang, text = a[Segment(0, 1)]
    assert label == spkr1
    assert lang == "ENG"
    assert text == "Hello World!"
    assert a == b

    # Creating two transcripts with different uri's but same content
    a = Transcript(uri="test")
    a[Segment(0, 1)] = (spkr1, "ENG", "Hello World!")
    a[Segment(1, 2)] = (spkr2, "SPA", "Hola mundo")

    b = Transcript(uri="test different")
    b[Segment(0, 1)] = (spkr1, "ENG", "Hello World!")
    b[Segment(1, 2)] = (spkr2, "SPA", "Hola mundo")

    assert a != b

    # Creating two transcripts with same uri's but different text
    a = Transcript(uri="test")
    a[Segment(0, 1)] = (spkr1, "ENG", "Hello World!")
    a[Segment(1, 2)] = (spkr2, "SPA", "Hola mundo")

    b = Transcript(uri="test")
    b[Segment(0, 1)] = (spkr1, "ENG", "-")
    b[Segment(1, 2)] = (spkr2, "SPA", "Hola mundo")

    assert a != b

    # Creating two transcripts with different labels
    a = Transcript(uri="test")
    a[Segment(0, 1)] = (spkr1, "ENG", "Hello World!")
    a[Segment(1, 2)] = (spkr2, "SPA", "Hola mundo")

    b = Transcript(uri="test")
    b[Segment(0, 1)] = (spkr1, "ENG", "-")
    b[Segment(1, 2)] = (spkr1, "SPA", "Hola mundo")

    assert a != b

    # Creating two transcripts with different languages
    a = Transcript(uri="test")
    a[Segment(0, 1)] = (spkr1, "ENG", "Hello World!")
    a[Segment(1, 2)] = (spkr2, "SPA", "Hola mundo")

    b = Transcript(uri="test")
    b[Segment(0, 1)] = (spkr1, "ENG", "-")
    b[Segment(1, 2)] = (spkr1, "ENG", "Hola mundo")

    assert a != b
