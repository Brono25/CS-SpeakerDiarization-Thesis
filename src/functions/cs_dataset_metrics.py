from pyannote.core import Segment
import copy
import numpy as np
from collections import defaultdict

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.functions.transcript import Transcript  # noqa: E402


class DatasetMetrics:
    """Code-Switching (CS) speech metrics"""

    def __init__(self, transcript: Transcript):
        self.transcript = copy.deepcopy(transcript)
        self.spanish = "SPA"
        self.english = "ENG"

    def m_index_token(self):
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
            elif language == "NA":
                pass
            else:
                raise ValueError(f"Invalid language: {language}")
            total += len(words)

        p_1 = english_total / total
        p_2 = spanish_total / total
        k = 2
        m_index = (1 - (p_1**2 + p_2**2)) / ((k - 1) * (p_1**2 + p_2**2))
        return m_index

    def m_index(self):
        """
        Calculates the m-index of the conversation transcript based on time.
        The m-index is a measure of the linguistic diversity of the conversation
        and is computed using the formula:

        m-index = (1 - sum(p_i^2)) / ((k-1) * sum(p_i^2))

        Where:
        - p_i is the total time in language i divided by total time.
        - k is the total number of languages.

        An m-index = 1 means that there is an equal amount of languages.

        Returns:
            float: The m-index value representing the linguistic diversity of
            the conversation transcript.
        """
        spanish_total = 0.0
        english_total = 0.0
        total_time = 0.0

        for start, end, _, language, _ in self.transcript.itertr():
            segment_duration = end - start
            if language == self.english:
                english_total += segment_duration
            elif language == self.spanish:
                spanish_total += segment_duration
            elif language == "NA":
                pass
            else:
                raise ValueError(f"Invalid language: {language}")

            total_time += segment_duration

        p_1 = english_total / total_time
        p_2 = spanish_total / total_time
        sum_of_squares = p_1**2 + p_2**2


        k = 2
        m_index = (1 - sum_of_squares) / ((k - 1) *  sum_of_squares)

        if m_index > 1:
            m_index = 1.0
        return m_index

    def language_entropy(self):
        pass

    def i_index_token(self):
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
    

    def i_index(self):
        """
        Calculates the I-index of the conversation transcript based on time.
        The I-index is a measure of the frequency of code-switching within the
        conversation and is computed using the formula:

                    I-index = num_switch_points / total_time

        Returns:
            float: The I-index value representing the frequency of code-switching within
            the conversation transcript.
        """
        num_switch_points = 0
        total_time = 0.0
        prev_language = None

        for start, end, _, language, _ in self.transcript.itertr():
            segment_time = end - start  
            total_time += segment_time  

            if prev_language is not None and prev_language != language:
                num_switch_points += 1 

            prev_language = language

        if total_time == 0:  
            return 0.0

        i_index = num_switch_points / total_time
        return i_index
    

    def change_point_frequency(self):
        """
        Calculates the I-index of the conversation transcript based on time.
        The I-index is a measure of the frequency of code-switching within the
        conversation and is computed using the formula:

                    I-index = num_switch_points / total_time

        Returns:
            float: The I-index value representing the frequency of code-switching within
            the conversation transcript.
        """
        num_switch_points = 0
        total_time = 0.0
        prev_language = None
        prev_speaker = None

        for start, end, speaker, language, _ in self.transcript.itertr():
            segment_time = end - start
            total_time += segment_time

            if (prev_language is not None and prev_language != language) or \
            (prev_speaker is not None and prev_speaker != speaker):
                num_switch_points += 1

            prev_language = language
            prev_speaker = speaker

        if total_time == 0:
            return 0.0

        i_index = num_switch_points / total_time
        return i_index

    def speaker_change_frequency(self):
        """
        Calculates the frequency of speaker changes within the conversation transcript,
        based on time. The frequency is computed using the formula:

                    Speaker Change Frequency = num_switch_points / total_time

        Returns:
            float: The value representing the frequency of speaker changes within
            the conversation transcript.
        """
        num_switch_points = 0
        total_time = 0.0
        prev_speaker = None

        for start, end, speaker, _, _ in self.transcript.itertr():
            segment_time = end - start
            total_time += segment_time

            if prev_speaker is not None and prev_speaker != speaker:
                num_switch_points += 1

            prev_speaker = speaker

        if total_time == 0:
            return 0.0

        speaker_change_frequency = num_switch_points / total_time
        return speaker_change_frequency


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
        span_lengths = self.get_spans_between_switchpoints_seconds()
        time_durations = span_lengths["time"]

        if len(time_durations) == 0:
            return 0.0  

        mean_spans = np.mean(time_durations)
        std_spans = np.std(time_durations)

        burstiness = (std_spans - mean_spans) / (std_spans + mean_spans)
        return burstiness


    def get_switchpoint_span_density(self, normalise=False):
        spans = self.get_spans_between_switchpoints()

        span_freq = defaultdict(int)
        for span in spans:
            span_freq[span] += 1

        total_counts = sum(span_freq.values())
        
        spans = list(span_freq.items())
        spans.sort(key=lambda x: x[0])
        span_lengths, counts = zip(*spans)
        
        # Normalize the counts
        if normalise:
            counts = [count / total_counts for count in counts]
        
        return span_lengths, counts


    def span_entropy(self):
        pass

    def memory(self):
        pass

    
    def get_spans_between_switchpoints_seconds(self):
        span_lengths = {"language": [], "time": []}
        span_length = 0
        prev_language = None
        for start, end, _, language, _ in self.transcript.itertr():
            segment_duration = end - start 

            if prev_language is not None and prev_language != language:
                span_lengths["language"].append(prev_language)
                span_lengths["time"].append(span_length)
                span_length = segment_duration
            else:
                span_length += segment_duration

            prev_language = language

        span_lengths["language"].append(prev_language)
        span_lengths["time"].append(span_length)
        return span_lengths

    def get_spans_between_switchpoints(self):
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
        return span_lengths