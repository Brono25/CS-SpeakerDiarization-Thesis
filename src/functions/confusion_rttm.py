from pyannote.core import Segment, Annotation
import copy
import numpy as np
from collections import defaultdict
from pyannote.database.util import load_rttm
from pyannote.metrics.diarization import DiarizationErrorRate

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.functions.transcript import Transcript  # noqa: E402
from src.functions.cs_diarization_metrics import CSDiarizationMetrics


from pyannote.core import Annotation

# Load RTTM file
uri = "zeledon14"
output = f"/Users/brono/GitHub/cs-dataset/code-switched/{uri}/pyannote/labeled_conf_{uri}_.rttm"
hyp = load_rttm(f"/Users/brono/GitHub/cs-dataset/code-switched/{uri}/pyannote/{uri}_pyannote.rttm")[uri]
#ref = load_rttm(f"/Users/brono/GitHub/cs-dataset/code-switched/{uri}/ref_{uri}.rttm")[uri]
#lang = load_rttm(f"/Users/brono/GitHub/cs-dataset/code-switched/{uri}/lang_{uri}.rttm")[uri]
conf = load_rttm(f"/Users/brono/GitHub/cs-dataset/code-switched/{uri}/pyannote/conf_{uri}.rttm")[uri]






def crop_annotation_from_timeline(uri, timeline, annotation):
    cropped_annotation = Annotation(uri=uri)
    for seg in timeline:
        temp_cropped_annotation = annotation.crop(seg, mode="intersection")
        cropped_annotation.update(temp_cropped_annotation)
    return cropped_annotation


conf_mask = conf.get_timeline()
#ref_cropped = crop_annotation_from_timeline(uri=uri, timeline=conf_mask, annotation=ref)
hyp_cropped = crop_annotation_from_timeline(uri=uri, timeline=conf_mask, annotation=hyp)
#lang_cropped = crop_annotation_from_timeline(uri=uri, timeline=conf_mask, annotation=hyp)




with open(output, "w") as f:
    hyp_cropped.write_rttm(f)






