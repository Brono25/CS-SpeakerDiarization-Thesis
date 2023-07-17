import matplotlib.pyplot as plt
from pyannote.core import notebook
from pyannote.database.util import load_rttm
from pyannote.metrics.diarization import DiarizationErrorRate
from pyannote.core import Annotation, Segment
from language_metrics import EnglishSpanishErrorRate

uri = "sastre09_1"

ref = load_rttm("/Users/brono/GitHub/katana/ref_rttm/ref_sastre09_1.rttm")[uri]
hyp = load_rttm("/Users/brono/GitHub/katana/hyp_rttm/hyp_sastre09_1.rttm")[uri]
lang = load_rttm("/Users/brono/GitHub/katana/lang_rttm/lang_sastre09_1.rttm")[uri]


analysis = EnglishSpanishErrorRate(uri=uri, reference=ref, hypothesis=hyp, language_map=lang)
components = analysis.compute_components()
metric = analysis.compute_metric(components=components)

for k, v in metric.items():
    print(f"{k} = {v*100:.2f}%")