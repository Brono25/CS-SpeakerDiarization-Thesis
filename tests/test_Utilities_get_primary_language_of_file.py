import pytest
import sys
import re

# Always use CS-SpeakerDiarization-Thesis as root
root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.functions.utilities import get_primary_language_of_file  # noqa: E402

def test_get_primary_language_of_file():
    input_data = ["herring06", "sastre01", "zeledon14"]
    expected_output = ["ENG", "SPA", "SPA"]
    
    for i, uri in enumerate(input_data):
        assert get_primary_language_of_file(uri) == expected_output[i]
