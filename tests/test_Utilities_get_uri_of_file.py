import pytest

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.functions.utilities import get_uri_of_file  # noqa: E402


def test_get_uri_of_file():
    input = [
        "/Users/brono/GitHub/CS-SpeakerDiarization-Thesis/cha_files",
        "/Users/brono/GitHub/CS-SpeakerDiarization-Thesis/cha_files/zeledon01.cha",
        "/Users/brono/GitHub/CS-SpeakerDiarization-Thesis/cha_files/zeledon14.cha",
        "/Users/brono/GitHub/CS-SpeakerDiarization-Thesis/wav_files/p_mono-sastre04.wav",
        "/Users/brono/GitHub/CS-SpeakerDiarization-Thesis/wav_files/p_mono-sastre12.wav",
        "/Users/brono/GitHub/CS-SpeakerDiarization-Thesis/wav_files/p_mono-herring09.wav",
        "/Users/brono/GitHub/CS-SpeakerDiarization-Thesis/rttm_files/ref_rttm/ref_sastre09_1.rttm",
    ]
    expected_output = [
        "zeledon01",
        "zeledon14",
        "sastre04",
        "sastre12",
        "herring09",
        "sastre09",
    ]

    # Checking ValueError for the first input
    with pytest.raises(ValueError, match=f"No URI found in filename {input[0]}"):
        get_uri_of_file(input[0])

    # Checking the rest of the inputs
    for i, filename in enumerate(input[1:], start=1):
        assert get_uri_of_file(filename) == expected_output[i - 1]
