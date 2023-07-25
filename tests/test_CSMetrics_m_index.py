import pytest
import numpy as np
from pyannote.core import Segment

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.transcript import Transcript  # noqa: E402
from src.cs_metrics import CSMetrics  # noqa: E402

def test_m_index():
    transcript = Transcript(uri="CS test")
    transcript[Segment(0, 1)] = ("AAA", "ENG", "Hello how are you")
    transcript[Segment(1, 2)] = ("BBB", "SPA", "Estoy bien y tú")
    transcript[Segment(2, 3)] = ("AAA", "ENG", "Im doing well")
    transcript[Segment(3, 4)] = ("AAA", "SPA", "Y tú qué haces")
    transcript[Segment(4, 5)] = ("BBB", "SPA", "Estoy estudiando")
    transcript[Segment(5, 6)] = ("BBB", "ENG", "And")
    transcript[Segment(6, 7)] = ("BBB", "SPA", "tengo una prueba mañana")
    transcript[Segment(7, 8)] = ("AAA", "ENG", "Oh I see")
    transcript[Segment(8, 9)] = ("AAA", "SPA", "Buena")
    transcript[Segment(9, 10)] = ("AAA", "ENG", "luck with that")
    transcript[Segment(10, 11)] = ("BBB", "SPA", "Gracias lo necesitaré")


    english_total_words = 14
    spanish_total_wrods = 18
    total_words = 32
    k = 2  # tot num languages
    p1 = english_total_words / total_words
    p2 = spanish_total_wrods / total_words
    m_index_expected = (1 - (p1**2 + p2**2)) / ((k - 1) * (p1**2 + p2**2))

    analysis = CSMetrics(transcript=transcript)
    m_index_result = analysis.m_index()

    assert np.isclose(m_index_expected, m_index_result, rtol=1e-05, atol=1e-08)
