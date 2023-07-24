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
    transcript[Segment(0, 1)] = ("AAA", "Hello how are you", "ENG")
    transcript[Segment(1, 2)] = ("BBB", "Estoy bien y tú", "SPA")
    transcript[Segment(2, 3)] = ("AAA", "Im doing well", "ENG")
    transcript[Segment(3, 4)] = ("AAA", "Y tú qué haces", "SPA")
    transcript[Segment(4, 5)] = ("BBB", "Estoy estudiando", "SPA")
    transcript[Segment(5, 6)] = ("BBB", "And", "ENG")
    transcript[Segment(6, 7)] = ("BBB", "tengo una prueba mañana", "SPA")
    transcript[Segment(7, 8)] = ("AAA", "Oh I see", "ENG")
    transcript[Segment(8, 9)] = ("AAA", "Buena", "SPA")
    transcript[Segment(9, 10)] = ("AAA", "luck with that", "ENG")
    transcript[Segment(10, 11)] = ("BBB", "Gracias lo necesitaré", "SPA")

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
