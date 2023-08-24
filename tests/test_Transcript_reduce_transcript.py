import pytest
import sys
import re

# Always use CS-SpeakerDiarization-Thesis as root
root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

from src.functions.transcript import Transcript, reduce_transcript
from pyannote.core import Segment



def create_transcript(segments_data):
    transcript = Transcript(uri="test")
    for segment_data in segments_data:
        start, end, label, language, text = segment_data
        transcript[Segment(start, end)] = (label, language, text)
    return transcript

def test_empty_transcript():
    transcript = Transcript(uri="test")
    assert reduce_transcript(transcript) == transcript

def test_single_segment_transcript():
    transcript_data = [[0, 1, "A", "ENG", "one"]]
    transcript = create_transcript(transcript_data)
    assert reduce_transcript(transcript) == transcript

def test_non_combining_segments():
    transcript_data = [
        [0, 1, "A", "ENG", "one"],
        [1, 2, "B", "ENG", "two"],
    ]
    transcript = create_transcript(transcript_data)
    assert reduce_transcript(transcript) == transcript

def test_combining_with_support_gap():
    transcript_data = [
        [0, 1, "A", "ENG", "one"],
        [1.24, 2, "A", "ENG", "two"],
    ]
    transcript = create_transcript(transcript_data)
    expected_result_data = [[0, 2, "A", "ENG", "one two"]]
    expected_result = create_transcript(expected_result_data)
    assert reduce_transcript(transcript, support=0.25) == expected_result

def test_combining_without_gap():
    transcript_data = [
        [0, 1, "A", "ENG", "one"],
        [1, 2, "A", "ENG", "two"],
    ]
    transcript = create_transcript(transcript_data)
    expected_result_data = [[0, 2, "A", "ENG", "one two"]]
    expected_result = create_transcript(expected_result_data)
    assert reduce_transcript(transcript) == expected_result

def test_combining_overlapping_segments():
    transcript_data = [
        [0, 1.5, "A", "ENG", "one"],
        [1, 2, "A", "ENG", "two"],
    ]
    transcript = create_transcript(transcript_data)
    expected_result_data = [[0, 2, "A", "ENG", "one two"]]
    expected_result = create_transcript(expected_result_data)
    assert reduce_transcript(transcript) == expected_result

def test_combining_completely_overlapping_segment():
    transcript_data = [
        [0, 10, "A", "ENG", "one"],
        [5, 8, "A", "ENG", "two"],
    ]
    transcript = create_transcript(transcript_data)
    expected_result_data = [[0, 10, "A", "ENG", "one two"]]
    expected_result = create_transcript(expected_result_data)
    assert reduce_transcript(transcript) == expected_result

def test_complex_multi_segment_combination():
    transcript_data = [
        [0, 1, "A", "ENG", "one"],
        [1.2, 2, "A", "ENG", "two"],
        [2, 3, "B", "ENG", "three"],
        [3.1, 4, "A", "ENG", "four"],
        [4, 5, "A", "ENG", "five"],
    ]
    transcript = create_transcript(transcript_data)
    expected_result_data = [
        [0, 2, "A", "ENG", "one two"],
        [2, 3, "B", "ENG", "three"],
        [3.1, 5, "A", "ENG", "four five"],
    ]
    expected_result = create_transcript(expected_result_data)
    assert reduce_transcript(transcript, support=0.25) == expected_result


def test_change_language():
    transcript_data = [
        [1, 2, "A", "ENG", "one"],
        [1.01, 2.01, "A", "SPA", "two"],
        [1.02, 2.02, "A", "ENG", "three"],
        [1.03, 2.03, "A", "ENG", "four"],
    ]
    transcript = create_transcript(transcript_data)
    expected_result_data = [
        [1, 2, "A", "ENG", "one"],
        [1.01, 2.01, "A", "SPA", "two"],
        [1.02, 2.03, "A", "ENG", "three four"],
    ]
    expected_result = create_transcript(expected_result_data)
    result = reduce_transcript(transcript, support=0.25)
    print(result)
    assert result == expected_result


def test_complex_multi_segment_combination2():
    transcript_data = [
        [0, 3.8, "A", "ENG", "one"],
        [1.2, 2, "B", "ENG", "two"],
        [2, 3, "C", "ENG", "three"],
        [3.1, 4, "D", "ENG", "four"],
        [4, 5, "A", "ENG", "five"],
        [5.2, 6, "A", "ENG", "six"],
        [5, 7, "A", "ENG", "seven"],
    ]
    transcript = create_transcript(transcript_data)
    expected_result_data = [
        [0, 7, "A", "ENG", "one five six seven"],
        [1.2, 2, "B", "ENG", "two"],
        [2, 3, "C", "ENG", "three"],
        [3.1, 4, "D", "ENG", "four"],
    ]
    expected_result = create_transcript(expected_result_data)
    assert reduce_transcript(transcript, support=0.25) == expected_result

def test_real_transcript_segment():
    transcript_data = [
        [22.003, 23.477, "NIC", "ENG", "that had to have been there when I went outside"],
        [23.460, 24.940, "NIC", "ENG", "that I went outside to smoke for a minute"],
        [24.922, 26.072, "NIC", "ENG", "and then I came back in"],
        [26.055, 27.059, "NIC", "ENG", "and he went outside"],
        [27.048, 29.709, "NIC", "ENG", "!and he goes"],
        [27.049, 29.708, "NIC", "SPA", "!estaba@s buscando@s"],
        [29.626, 31.123, "NIC", "SPA", "!estaba@s"],
        [29.627, 31.122, "NIC", "ENG", "!I love when he uses his hand"],
        [31.097, 32.089, "JES", "ENG", "oh"],
        [31.491, 34.562, "NIC", "SPA", "estaba buscando estaba buscando"]
    ]
    transcript = create_transcript(transcript_data)
    expected_result_data = [
        [22.003, 27.059, "NIC", "ENG", "that had to have been there when I went outside that I went outside to smoke for a minute and then I came back in and he went outside"],
        [27.048, 29.709, "NIC", "ENG", "!and he goes"],
        [27.049, 29.708, "NIC", "SPA", "!estaba@s buscando@s"],
        [29.626, 31.123, "NIC", "SPA", "!estaba@s"],
        [29.627, 31.122, "NIC", "ENG", "!I love when he uses his hand"],
        [31.097, 32.089, "JES", "ENG", "oh"],
        [31.491, 34.562, "NIC", "SPA", "estaba buscando estaba buscando"]
    ]
    expected_result = create_transcript(expected_result_data)
    assert reduce_transcript(transcript, support=0.25) == expected_result



def test_real_transcript_segment2():
    transcript_data = [
        [73.684, 174.822, "JES", "ENG", "mhm"],
        [174.816, 179.520, "NIC", "ENG", "and he said you know I was reading about what had to be done and and and and I go"],
        [179.527, 179.719, "NIC", "ENG", "look"],
        [180.450, 182.836, "NIC", "ENG", "I said chill he goes youve done it before I said Ive been doing it for ten years"],
        [183.664, 187.559, "NIC", "ENG", "okay I said dont worry about it I know how to do everything you concentrate on your homily"]
    ]
    transcript = create_transcript(transcript_data)
    expected_result_data = [
        [73.684, 174.822, "JES", "ENG", "mhm"],
        [174.816, 179.719, "NIC", "ENG", "and he said you know I was reading about what had to be done and and and and I go look"],
        [180.450, 182.836, "NIC", "ENG", "I said chill he goes youve done it before I said Ive been doing it for ten years"],
        [183.664, 187.559, "NIC", "ENG", "okay I said dont worry about it I know how to do everything you concentrate on your homily"]
    ]
    expected_result = create_transcript(expected_result_data)
    assert reduce_transcript(transcript, support=0.25) == expected_result



def test_real_transcript_segment3():
    transcript_data = [
        [1.538, 4.342, "KEV", "SPA", "bueno y qué tú crees de de aquí la cuadra lo que están haciendo"],
        [4.336, 6.914, "KEV", "SPA", "!la rotondita esa"],
        [4.337, 6.913, "KEV", "ENG", "!do@s you@s like@s that@s"],
        [5.989, 7.005, "SOF", "SPA", "!pero"],
        [5.990, 7.004, "SOF", "ENG", "!thats@s illegal@s"],
        [7.005, 9.588, "SOF", "SPA", "!esa rotonda es"],
        [7.006, 9.587, "SOF", "ENG", "!illegal@s"],
        [9.583, 10.564, "SOF", "ENG", "from what I know"],
        [10.579, 11.821, "SOF", "SPA", "!supuesto de eso es"],
        [10.580, 11.820, "SOF", "ENG", "!illegal@s"],
        [4.336, 6.914, "KEV", "SPA", "extra"],
    ]
    transcript = create_transcript(transcript_data)
    expected_result_data = [
        [1.538, 6.914, "KEV", "SPA", "bueno y qué tú crees de de aquí la cuadra lo que están haciendo !la rotondita esa extra"],
        [4.337, 6.913, "KEV", "ENG", "!do@s you@s like@s that@s"],
        [5.989, 7.005, "SOF", "SPA", "!pero"],
        [5.990, 7.004, "SOF", "ENG", "!thats@s illegal@s"],
        [7.005, 9.588, "SOF", "SPA", "!esa rotonda es"],
        [7.006, 10.564, "SOF", "ENG", "!illegal@s from what I know"],
        [10.579, 11.821, "SOF", "SPA", "!supuesto de eso es"],
        [10.580, 11.820, "SOF", "ENG", "!illegal@s"],
    ]
    expected_result = create_transcript(expected_result_data)
    result = reduce_transcript(transcript, support=0.25)

    print(result)
    print()
    print(expected_result)
    assert expected_result == result


test_real_transcript_segment3()