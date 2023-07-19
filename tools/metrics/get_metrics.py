import os

import matplotlib.pyplot as plt
from english_spanish_error_rate import EnglishSpanishErrorRate
from pyannote.core import notebook
from pyannote.database.util import load_rttm
from pyannote.metrics.diarization import DiarizationErrorRate


uri = "sastre09_1"

curr_dir = os.path.realpath(__file__)
root_dir = curr_dir[: curr_dir.index("katana") + len("katana")]
error_dir = f"{root_dir}/tools/metrics/error_rttm"

audio_file_path = f"{root_dir}/wav/{uri}.wav"
ref = load_rttm(f"{root_dir}/ref_rttm/ref_{uri}.rttm")[uri]
hyp = load_rttm(f"{root_dir}/hyp_rttm/hyp_{uri}.rttm")[uri]
lang = load_rttm(f"{root_dir}/lang_rttm/lang_{uri}.rttm")[uri]


def plot_annotations(annotations_with_legends):
    num_subplots = len(annotations_with_legends)
    fig, axs = plt.subplots(num_subplots, 1, figsize=(5, 3 * num_subplots), sharex=True)
    if num_subplots == 1:
        axs = [axs]

    for idx, (annotation, legend) in enumerate(annotations_with_legends):
        notebook.plot_annotation(annotation, ax=axs[idx])
        axs[idx].set_title(legend)


def compute_lang_error_rates(uri, ref, hyp, lang):
    analysis = EnglishSpanishErrorRate(
        uri=uri, reference=ref, hypothesis=hyp, language_map=lang
    )
    components = analysis.compute_components()
    lang_metric = analysis.compute_metric(components=components)
    for k, v in lang_metric.items():
        print(f"{k} = {v*100:.2f}%")
    return analysis


def compute_der(ref, hyp):
    der_metric = DiarizationErrorRate(skip_overlap=True, collar=0.0)
    der = der_metric(reference=ref, hypothesis=hyp, detailed=True)
    for k, v in der.items():
        print(f"{k} = {v:.2f}")


if __name__ == "__main__":
    compute_der(ref, hyp)
    analysis = compute_lang_error_rates(uri, ref, hyp, lang)
    conf_annotation = analysis.language_confusion_annotation()
    miss_annotation = analysis.language_missed_annotation()

    with open(f"{error_dir}/conf_{uri}.rttm", "w") as f:
        conf_annotation.write_rttm(f)

    with open(f"{error_dir}/miss_{uri}.rttm", "w") as f:
        miss_annotation.write_rttm(f)
