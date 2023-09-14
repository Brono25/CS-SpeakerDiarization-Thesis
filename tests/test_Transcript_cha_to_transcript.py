import pytest
from pyannote.core import Segment
import tempfile
import os
from pprint import pformat 
# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.functions.cha_conversion import convert_cha_to_transcript_str_format
from src.functions.transcript import Transcript # noqa: E402
from src.functions.utilities import ROOT_DIR, get_uri_of_file, debug_transcript_comparison # noqa: E402



# Test data
tests = [
    (
        '\n'.join([
            "@Convert chafile to Transcript Test 1",
            "@Comment: Cha file in matrix language English",
            "@Primary Langugae: English"
            "@begin",
            "*AAA: Speaker A talking in English 0_1000",
            "*BBB: [- spa] Speaker B talking in Spanish 1000_2000",
            "*AAA: Using@s interswitching@s markers@s 2000_3000",
            "@end"
        ]),
        "tmp_eng",
        [(0, 1, "AAA", "ENG", "Speaker A talking in English"), 
         (1, 2, "BBB", "SPA", "Speaker B talking in Spanish"), 
         (2, 3, "AAA", "SPA", "Using@s interswitching@s markers@s")]
    ),
    (
        '\n'.join([
            "@Convert chafile to Transcript Test 2",
            "@Comment: Cha file in matrix language Spanish",
            "@Primary Langugae: Spanish"
            "@begin",
            "*AAA: [- eng] Speaker A talking in English 0_1000",
            "*BBB: Speaker B talking in Spanish 1000_2000",
            "*AAA: Using@s interswitching@s markers@s 2000_3000",
            "@end"
        ]),
        "tmp_spa",
        [(0, 1, "AAA", "ENG", "Speaker A talking in English"), 
         (1, 2, "BBB", "SPA", "Speaker B talking in Spanish"), 
         (2, 3, "AAA", "ENG", "Using@s interswitching@s markers@s")]
    ),
    (
        '\n'.join([
            "@Convert chafile to Transcript Test 3",
            "@Comment: Code-Swithching min sentence ",
            "@Primary Langugae: Spanish"
            "@begin",
            "*BBB: [- eng] some English 0_1000",
            "*AAA: Speaker@s A talking in code@s switched speech@s 1000_2000",
            "@end"
        ]),
        "tmp_spa",
        [(0.000, 1.000, "BBB", "ENG", "some English"), 
         (1.000, 2.000, "AAA", "ENG", "!Speaker@s"), 
         (1.001, 1.999, "AAA", "SPA", "!A talking in"), 
         (1.002, 1.998, "AAA", "ENG", "!code@s"), 
         (1.003, 1.997, "AAA", "SPA", "!switched"), 
         (1.004, 1.996, "AAA", "ENG", "!speech@s")]
    ),
        (
        '\n'.join([
            "@Convert chafile to Transcript Test 4",
            "@Comment: Code-Swithching min sentence ",
            "@Primary Langugae: English"
            "@begin",
            "*BBB: [- spa] some Spanish 0_1000",
            "*AAA: Speaker@s A talking in code@s switched@s speech@s 1000_2000",
            "@end"
        ]),
        "tmp_eng",
        [(0.000, 1.000, "BBB", "SPA", "some Spanish"), 
         (1.000, 2.000, "AAA", "SPA", "!Speaker@s"), 
         (1.001, 1.999, "AAA", "ENG", "!A talking in"), 
         (1.002, 1.998, "AAA", "SPA", "!code@s switched@s speech@s")]
    ),
        (
        '\n'.join([
            "@Convert chafile to Transcript Test 5",
            "@Comment: Missing timestamps",
            "@Primary Langugae: English"
            "@begin",
            "*BBB: [- spa] some Spanish 0_1000",
            "*AAA: This line doesnt have a timestamp",
            "*BBB: [- spa] Neither does this one",
            "*AAA: This one does tho 2000_3000",
            "@end"
        ]),
        "tmp_eng",
        [(0.000, 1.000, "BBB", "SPA", "some Spanish"), 
         (0.001, 0.999, "AAA", "ENG", "!This line doesnt have a timestamp"), 
         (0.002, 0.998, "BBB", "SPA", "!Neither does this one"), 
         (2.000, 3.000, "AAA", "ENG", "This one does tho")]
    ),
    
]

def create_temp_file(test_data, uri):
    with tempfile.NamedTemporaryFile(suffix=f'_{uri}.cha', delete=False) as temp:
        temp.writelines(line.encode() for line in test_data)
    return temp.name

@pytest.mark.parametrize("test_data, uri, expected_segments", tests)
def test_cha_to_transcript(test_data, uri, expected_segments):
    test_file_path = create_temp_file(test_data, uri)
    actual_output = convert_cha_to_transcript_str_format(test_file_path, uri='test', prim_lang='ENG')

    expected_output = [[start, end, speaker, language, text] for start, end, speaker, language, text in expected_segments]

    assert actual_output == expected_output, f"Expected:\n{pformat(expected_output)}\nGot:\n{pformat(actual_output)}"

    os.remove(test_file_path)
