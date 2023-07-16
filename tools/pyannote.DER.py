
import matplotlib.pyplot as plt
from pyannote.core import notebook
from pyannote.database.util import load_rttm
from pyannote.metrics.diarization import DiarizationErrorRate


def plot_segments(ref, hyp):
    fig, axs = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    notebook.plot_annotation(ref, ax=axs[0], time=False)
    axs[0].set_title('Reference Annotation')
    notebook.plot_annotation(hyp, ax=axs[1], time=False)
    axs[1].set_title('Hypothesis Annotation')
    plt.tight_layout()
    plt.show()



ref_sastre09_1 = load_rttm("./ref_rttm/ref_sastre09_1.rttm")["sastre09_1"]
hyp_sastre09_1 = load_rttm("./hyp_rttm/hyp_sastre09_1.rttm")["sastre09_1"]


metric = DiarizationErrorRate(skip_overlap=True, collar=0.0)
der = metric(reference=ref_sastre09_1, hypothesis=hyp_sastre09_1) * 100
print(f"The DER is {der:.2f}%")


plot_segments(ref_sastre09_1, hyp_sastre09_1)