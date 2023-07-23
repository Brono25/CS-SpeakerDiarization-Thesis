import pytest

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.transcript import _get_speaker_content_from_cha  # noqa: E402


content = [
    r"@UTF8",
    r"@PID:   11312/t-00000050-1",
    r"@Begin",
    r"@Languages: eng, spa",
    r"@Participants:  KAY Kayla Adult, VAL Valeria Adult",
    r"@ID:    spa, eng|Miami|KAY|48;|female|||Adult|||",
    r"@ID:    spa, eng|Miami|VAL|60;|female|||Adult|||",
    r"@Situation: Informal conversation between two sisters at Kayla's",
    r"    workplace",
    r"@Date:  27-MAR-2008",
    r"@Transcriber:   M. Carmen Parafita Couto, Bangor University. Initial",
    r"    translation by Vanesa Bonavota García",
    r"@Comment:   Researcher: Lergia Sastre",
    r"@Time Duration: 00:40:02",
    r"@Media: sastre09, audio",
    r"*KAY:   so sí@s hay@s un@s range ahí@s . 470_2107",
    r"%mor:   adv|so L2|sí L2|hay L2|un n|range L2|ahí .",
    r"%gra:   1|2|JCT 2|0|INCROOT 3|2|PRED 4|3|CONJ 5|6|MOD 6|4|COORD 7|2|PUNCT",
    r"%eng:   so yes, there's a range .",
    r"*VAL:   m:hm . 2180_2490",
    r"%mor:   co|mhm=yes .",
    r"%gra:   1|0|INCROOT 2|1|PUNCT",
    r"*KAY:   +< [- spa] (d)onde los policías &~e practican . 2181_4321",
    r"%mor:   pro:rel|donde=where pro:obj|él&m-PL=he n|policía&f-PL=police",
    r"    v|practica-3P&PRES=practise .",
    r"%eng:   where the cops practice .",
    r"*KAY:   y@s [/] y@s la@s gente@s que@s están@s (.) <los@s trainees> [//]",
    r"    the police trainees . 4293_7486",
    r"%mor:   L2|y L2|la L2|gente L2|que L2|están det:art|the n|police",
    r"    n|trainee-PL .",
    r"%gra:   1|0|INCROOT 2|1|CONJ 3|2|COORD 4|3|CONJ 5|4|COORD 6|8|DET 7|8|MOD",
    r"    8|5|OBJ 9|1|PUNCT",
    r"%eng:   and people that are trainees, the police trainees .",
    r"*KAY:   they do it every day . 7387_8618",
    r"%mor:   pro:sub|they v|do pro:per|it qn|every n|day .",
    r"%gra:   1|2|SUBJ 2|0|ROOT 3|2|OBJ 4|5|QUANT 5|2|JCT 6|2|PUNCT",
    r"*KAY:   so when you come here don't be afraid if you hear it . 8575_10783",
    r"%mor:   co|so conj|when pro:per|you v|come adv|here mod|do~neg|not cop|be",
    r"    adj|afraid conj|if pro:per|you v|hear pro:per|it .",
    r"%gra:   1|4|COM 2|4|LINK 3|4|SUBJ 4|0|ROOT 5|8|JCT 6|8|AUX 7|6|NEG 8|4|COMP",
    r"    9|8|PRED 10|12|LINK 11|12|SUBJ 12|4|CJCT 13|12|OBJ 14|4|PUNCT",
    r"*KAY:   (be)cause you know they're practicing . 11095_12193",
    r"%mor:   conj|because pro:per|you v|know pro:sub|they~aux|be&PRES",
    r"    part|practice-PRESP .",
    r"%gra:   1|3|LINK 2|3|SUBJ 3|0|ROOT 4|6|SUBJ 5|6|AUX 6|3|COMP 7|3|PUNCT",
    r"*VAL:   yeah yeah they have to put these earphones . 12064_14786",
    r"%mor:   co|yeah co|yeah pro:sub|they v|have inf|to v|put&ZERO det:dem|these",
    r"    n|+n|ear+n|phone-PL .",
    r"%gra:   1|4|COM 2|4|COM 3|4|SUBJ 4|0|ROOT 5|6|INF 6|4|COMP 7|8|DET 8|6|OBJ",
    r"    9|4|PUNCT",
    r"%com:   background noise",
    r"*VAL:   [- spa] porque si no se puede quedar uno sordo . 14900_16643",
    r"%mor:   conj|porque=because conj|si=if adv|no=no pro:refl|se=itself",
    r"    v|pode-3S&PRES=can inf|queda-INF=stay pro:dem|uno-MASC=one",
    r"    adj|sordo-MASC=deaf .",
    r"%eng:   because otherwise you may go deaf .",
    r"*KAY:   +< really ? 16433_16794",
    r"%mor:   adv|real&dadj-LY ?",
    r"%gra:   1|0|INCROOT 2|1|PUNCT",
]

expected_output = [
    "*KAY: so sí@s hay@s un@s range ahí@s . 470_2107",
    "*VAL: m:hm . 2180_2490",
    "*KAY: +< [- spa] (d)onde los policías &~e practican . 2181_4321",
    "*KAY: y@s [/] y@s la@s gente@s que@s están@s (.) <los@s trainees> [//] the police trainees . 4293_7486",
    "*KAY: they do it every day . 7387_8618",
    "*KAY: so when you come here don't be afraid if you hear it . 8575_10783",
    "*KAY: (be)cause you know they're practicing . 11095_12193",
    "*VAL: yeah yeah they have to put these earphones . 12064_14786",
    "*VAL: [- spa] porque si no se puede quedar uno sordo . 14900_16643",
    "*KAY: +< really ? 16433_16794",
]


def test_get_speaker_content_from_cha():
    reduced_content = _get_speaker_content_from_cha(content)
    for i, line in enumerate(reduced_content):
        assert line == expected_output[i]
