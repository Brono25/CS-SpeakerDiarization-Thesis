from pyannote.core import Segment
import copy
import numpy as np

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.transcript import Transcript  # noqa: E402


class CSMetrics:
    """Code-Switching (CS) speech metrics"""

    def __init__(self, transcript: Transcript):
        self.transcript = copy.deepcopy(transcript)
        self.spanish = "SPA"
        self.english = "ENG"

    def m_index(self):
        """
        Calculates the m-index of the conversation transcript.
        The m-index is a measure of the linguistic diversity of the conversation
        and is computed using the formula:

        m-index = (1 - sum(p_i^2)) / ((k-1) * sum(p_i^2))

        Where:
        - p_i is the total words in language i divided by total words.
        - k is the total number of languages.

        An m-index = 1 means that there is an equal amount of languages.

        Returns:
            float: The m-index value representing the linguistic diversity of
            the conversation transcript.
        """

        spanish_total = 0
        english_total = 0
        total = 0
        for _, (_, language, text) in self.transcript.items():
            words = [word for word in text.split(" ") if word]
            if language == self.english:
                english_total += len(words)
            elif language == self.spanish:
                spanish_total += len(words)
            else:
                raise ValueError(f"Invalid language: {language}")
            total += len(words)

        p_1 = english_total / total
        p_2 = spanish_total / total
        k = 2
        m_index = (1 - (p_1**2 + p_2**2)) / ((k - 1) * (p_1**2 + p_2**2))
        return m_index

    def language_entropy(self):
        pass

    def i_index(self):
        """
        Calculates the I-index of the conversation transcript.
        The I-index is a measure of the frequency of code-switching within the
        conversation and is computed using the formula:

                    I-index = num_switch_points / (total_words - 1)

        Returns:
            float: The I-index value representing the frequency of code-switching within
            the conversation transcript.
        """
        num_switch_points = 0
        total_words = 0
        prev_language = None

        for _, (_, language, text) in self.transcript.items():
            words = [word for word in text.split(" ") if word]
            total_words += len(words)
            if prev_language is not None and prev_language != language:
                num_switch_points += 1
            prev_language = language
        i_index = num_switch_points / (total_words - 1)
        return i_index

    def burstiness(self):
        """
        Calculates the burstiness of code-switching behavior in the corpus.
        Burstiness measures whether code-switching occurs in bursts or has a more
        periodic nature. It compares the code-switching behavior in the corpus
        to a Poisson behavior where code-switching occurs at random.

        Returns:
            float: The burstiness value of code-switching behavior in the corpus.
            The value is bounded within the interval [-1, 1]. For corpora with
            periodic code-switching, the value tends to be closer to -1, and for
            corpora with less predictable code-switching patterns, the
            value tends to be closer to 1.
        """
        span_lengths = []
        span_length = 0
        prev_language = None
        for _, (_, language, text) in self.transcript.items():
            words = [word for word in text.split(" ") if word]

            if prev_language is not None and prev_language != language:
                span_lengths.append(span_length)
                span_length = len(words)
            else:
                span_length += len(words)

            prev_language = language

        span_lengths.append(span_length)

        mean_spans = np.mean(span_lengths)
        std_spans = np.std(span_lengths)

        burstiness = (std_spans - mean_spans) / (std_spans + mean_spans)
        return burstiness

    def span_entropy(self):
        pass

    def memory(self):
        pass
