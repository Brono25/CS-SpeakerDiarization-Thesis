from pyannote.audio import Model, Inference
from pyannote.database.util import load_rttm
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np
import re
from collections import defaultdict
import pickle

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

SCIKIT_ORANGE = "#FE8025"
SCIKIT_DARK_ORANGE = "#7F4013"
SCIKIT_BLUE = "#387EB5"
SCIKIT_DARK_BLUE = "#1C3F5A"

YELLOW_ORANGE = "#FCB73B"

INTENSE_ORANGE = "#EF582C"
TEAL = "#25B7B2"

SPEAKER1_SPA = "#0172F1"
SPEAKER1_ENG = "#36BBF4"

SPEAKER2_SPA = "#E6A538"
SPEAKER2_ENG = "#EB8E29"



ACCESS_TOKEN = "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"
uri_list = ['sastre01', 'herring06', 'herring07', 'herring08', 'herring10', 'herring13', 'sastre11', 'zeledon04', 'sastre06', 'sastre09', 'zeledon08', 'zeledon14']

model = Model.from_pretrained("pyannote/embedding", use_auth_token=ACCESS_TOKEN)
inference = Inference(model, window="whole")

for uri in uri_list:
    embeddings = []  
    label_map = []
    audio = f"/Users/brono/GitHub/cs-dataset/code-switched/{uri}/{uri}.wav"
    lang_rttm = load_rttm(f"/Users/brono/GitHub/cs-dataset/code-switched/{uri}/lang_{uri}.rttm")[uri]
    ref = load_rttm(f"/Users/brono/GitHub/cs-dataset/code-switched/{uri}/ref_{uri}.rttm")[uri]

    overlaps = ref.get_overlap()
    ref = ref.extrude(overlaps)
    lang_rttm = lang_rttm.extrude(overlaps)
    speaker1, speaker2 = [x for x in ref.labels() if isinstance(x, str) and re.match(r"[A-Z]{3}", x)]
    lang1, lang2 = [x for x in lang_rttm.labels() if isinstance(x, str) and re.match(r"SPA|ENG", x)]

    ref_list = [(segment, label) for segment, _, label in ref.itertracks(yield_label=True)]
    lang_list = [(segment, lang) for segment, _, lang in lang_rttm.itertracks(yield_label=True)]

    assert len(ref_list) == len(lang_list)

    min_length = 1.0  
    for i, (segment, label) in enumerate(ref_list):
        lang_seg, lang = lang_list[i]
        assert lang_seg == segment
        if segment.end - segment.start >= min_length:
            if lang is not np.nan:
                label_map.append((label, lang))
                embedding = inference.crop(audio, segment)
                embeddings.append(embedding)
            
    embeddings_array = np.vstack(embeddings)

    bundle = {
        'embeddings': embeddings_array,
        'label_map': label_map,
        'speaker1': speaker1,
        'speaker2': speaker2
    }

    with open(f"embeddings/{uri}_embedding.pkl", 'wb') as f:
       pickle.dump(bundle, f)