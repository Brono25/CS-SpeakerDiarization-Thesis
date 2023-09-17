import pytest
from pyannote.core import Segment
import tempfile
import os
import re

# Local imports
from src.functions.cha_conversion import convert_cha_to_transcript_str_format
from src.functions.transcript import Transcript
from src.functions.utilities import ROOT_DIR, get_uri_of_file, debug_transcript_comparison

def create_temp_file(test_data, uri):
    with tempfile.NamedTemporaryFile(suffix=f'_{uri}.cha', delete=False) as temp:
        temp.writelines(line.encode() for line in test_data)
    return temp.name

def compare(actual_output, expected_output):
    for i, (act_line, exp_line) in enumerate(zip(actual_output, expected_output)):
        for j, (act_element, exp_element) in enumerate(zip(act_line, exp_line)):
            if act_element != exp_element:
                raise AssertionError(
                    f"Test failed:\n"
                    f"  Line: {i + 1}\n"
                    f"  Element: {j + 1}\n"
                    f"  Expected: {exp_element}\n"
                    f"  Got: {act_element}"
                )

def test_cha_to_transcript_1():
    test_data = '\n'.join([
        "@Convert chafile to Transcript Test 1",
        "@Comment: Cha file in matrix language English",
        "@Primary Langugae: English",
        "@begin",
        "*AAA: Speaker A talking in English 0_1000",
        "*BBB: [- spa] Speaker B talking in Spanish 1000_2000",
        "*AAA: Using@s interswitching@s markers@s 2000_3000",
        "@end"
    ])
    uri = "tmp_eng"
    prim_lang = "ENG"
    expected_segments = [
        (0, 1, "AAA", "ENG", "Speaker A talking in English"), 
        (1, 2, "BBB", "SPA", "Speaker B talking in Spanish"), 
        (2, 3, "AAA", "SPA", "Using@s interswitching@s markers@s")
    ]
    
    test_file_path = create_temp_file(test_data, uri)
    actual_output = convert_cha_to_transcript_str_format(test_file_path, uri='test', prim_lang=prim_lang)

    expected_output = [[start, end, speaker, language, text] for start, end, speaker, language, text in expected_segments]
    
    compare(actual_output, expected_output)

    os.remove(test_file_path)

def test_cha_to_transcript_2():
    test_data = '\n'.join([
        "@Convert chafile to Transcript Test 2",
        "@Comment: Cha file in matrix language Spanish",
        "@Primary Langugae: Spanish",
        "@begin",
        "*AAA: [- eng] Speaker A talking in English 0_1000",
        "*BBB: Speaker B talking in Spanish 1000_2000",
        "*AAA: Using@s interswitching@s markers@s 2000_3000",
        "@end"
    ])
    uri = "tmp_spa"
    prim_lang = "SPA"
    expected_segments = [
        (0, 1, "AAA", "ENG", "Speaker A talking in English"), 
        (1, 2, "BBB", "SPA", "Speaker B talking in Spanish"), 
        (2, 3, "AAA", "ENG", "Using@s interswitching@s markers@s")
    ]

    test_file_path = create_temp_file(test_data, uri)
    actual_output = convert_cha_to_transcript_str_format(test_file_path, uri='test', prim_lang=prim_lang)

    expected_output = [[start, end, speaker, language, text] for start, end, speaker, language, text in expected_segments]
    
    compare(actual_output, expected_output)

    os.remove(test_file_path)

def test_cha_to_transcript_3():
    test_data = '\n'.join([
        "@Convert chafile to Transcript Test 3",
        "@Comment: Code-Switching min sentence ",
        "@Primary Langugae: Spanish",
        "@begin",
        "*BBB: [- eng] some English 0_1000",
        "*AAA: Speaker@s A talking in code@s switched speech@s 1000_2000",
        "@end"
    ])
    uri = "tmp_spa"
    prim_lang = "SPA"
    expected_segments = [
        (0.000, 1.000, "BBB", "ENG", "some English"), 
        (1.000, 2.000, "AAA", "ENG", "!Speaker@s"), 
        (1.010, 2.010, "AAA", "SPA", "!A talking in"), 
        (1.020, 2.020, "AAA", "ENG", "!code@s"), 
        (1.030, 2.030, "AAA", "SPA", "!switched"), 
        (1.040, 2.040, "AAA", "ENG", "!speech@s")
    ]

    test_file_path = create_temp_file(test_data, uri)
    actual_output = convert_cha_to_transcript_str_format(test_file_path, uri='test', prim_lang=prim_lang)

    expected_output = [[start, end, speaker, language, text] for start, end, speaker, language, text in expected_segments]
    
    compare(actual_output, expected_output)

    os.remove(test_file_path)

def test_cha_to_transcript_4():
    test_data = '\n'.join([
        "@Convert chafile to Transcript Test 4",
        "@Comment: Code-Switching min sentence ",
        "@Primary Langugae: English",
        "@begin",
        "*BBB: [- spa] some Spanish 0_1000",
        "*AAA: Speaker@s A talking in code@s switched@s speech@s 1000_2000",
        "@end"
    ])
    uri = "tmp_eng"
    prim_lang = "ENG"
    expected_segments = [
        (0.000, 1.000, "BBB", "SPA", "some Spanish"), 
        (1.000, 2.000, "AAA", "SPA", "!Speaker@s"), 
        (1.01, 2.01, "AAA", "ENG", "!A talking in"), 
        (1.02, 2.02, "AAA", "SPA", "!code@s switched@s speech@s")
    ]

    test_file_path = create_temp_file(test_data, uri)
    actual_output = convert_cha_to_transcript_str_format(test_file_path, uri='test', prim_lang=prim_lang)

    expected_output = [[start, end, speaker, language, text] for start, end, speaker, language, text in expected_segments]
    
    compare(actual_output, expected_output)

    os.remove(test_file_path)

def test_cha_to_transcript_5():
    test_data = '\n'.join([
        "@Convert chafile to Transcript Test 5",
        "@Comment: Missing timestamps",
        "@Primary Langugae: English",
        "@begin",
        "*BBB: [- spa] some Spanish 0_1000",
        "*AAA: This line doesnt have a timestamp",
        "*BBB: [- spa] Neither does this one",
        "*AAA: This one does tho 2000_3000",
        "@end"
    ])
    uri = "tmp_eng"
    prim_lang = "ENG"
    expected_segments = [
        (0.000, 1.000, "BBB", "SPA", "some Spanish"), 
        (0.01, 1.01, "AAA", "ENG", "!This line doesnt have a timestamp"), 
        (0.02, 1.02, "BBB", "SPA", "!Neither does this one"), 
        (2.000, 3.000, "AAA", "ENG", "This one does tho")
    ]

    test_file_path = create_temp_file(test_data, uri)
    actual_output = convert_cha_to_transcript_str_format(test_file_path, uri='test', prim_lang=prim_lang)

    expected_output = [[start, end, speaker, language, text] for start, end, speaker, language, text in expected_segments]
    
    compare(actual_output, expected_output)

    os.remove(test_file_path)
