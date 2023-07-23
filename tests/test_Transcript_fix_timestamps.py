import pytest
import re
import sys

# Always use CS-SpeakerDiarization-Thesis as root
root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.transcript import _fix_timestamps  # noqa: E402

def test_fix_timestamps():
    # Define the input data
    input_data = [
        "AAA Here is a line of text 1_2",
        "BBB Here is a line of text without a timestamp",
        "AAA Here is a line of text also without a timestamp",
        "BBB Now this line has a timestamp 3_4",
        "BBB But this line doesnt have a timestamp"
    ]
    
    # Define the expected output data
    expected_output = [
        "AAA Here is a line of text 1_2",
        "BBB Here is a line of text without a timestamp ! 1_2",
        "AAA Here is a line of text also without a timestamp ! 1_2",
        "BBB Now this line has a timestamp 3_4",
        "BBB But this line doesnt have a timestamp ! 3_4"
    ]

    # Assert that the _fix_timestamps function, when passed the input_data,
    # gives the same result as the expected_output.
    assert _fix_timestamps(input_data) == expected_output
