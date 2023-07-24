import pytest

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.transcript import _seperate_content_languages  # noqa: E402


def test_seperate_content_languages():
    input = [
        "KAY so sí@s hay@s un@s range ahí@s 470_2107",
        "VAL mhm 2180_2490",
        "KAY _SPA donde los policías e practican 2181_4321",
        "KAY y@s y@s la@s gente@s que@s están@s los@s trainees the police trainees 4293_7486",
        "KAY they do it every day 7387_8618",
        "KAY so when you come here dont be afraid if you hear it 8575_10783",
        "KAY because you know theyre practicing 11095_12193",
        "VAL yeah yeah they have to put these earphones 12064_14786",
        "VAL _SPA porque si no se puede quedar uno sordo 14900_16643",
        "KAY really 16433_16794",
    ]
    expected_output = [
        "KAY ! so 470_2107",
        "KAY ! sí@s hay@s un@s 471_2106",
        "KAY ! range 472_2105",
        "KAY ! ahí@s 473_2104",
        "VAL mhm 2180_2490",
        "KAY _SPA donde los policías e practican 2181_4321",
        "KAY ! y@s y@s la@s gente@s que@s están@s los@s 4293_7486",
        "KAY ! trainees the police trainees 4294_7485",
        "KAY they do it every day 7387_8618",
        "KAY so when you come here dont be afraid if you hear it 8575_10783",
        "KAY because you know theyre practicing 11095_12193",
        "VAL yeah yeah they have to put these earphones 12064_14786",
        "VAL _SPA porque si no se puede quedar uno sordo 14900_16643",
        "KAY really 16433_16794",
    ]
    output = _seperate_content_languages(input)
    assert output == expected_output

