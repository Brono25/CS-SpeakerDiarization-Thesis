import matplotlib.pyplot as plt
from pyannote.core import notebook
from pyannote.database.util import load_rttm
from pyannote.metrics.diarization import DiarizationErrorRate
from pyannote.core import Annotation, Segment
from language_metrics import EnglishSpanishErrorRate
import time
from pydub import AudioSegment
from pydub.playback import play
import sys


audio_file_path = "/Users/brono/GitHub/katana/wav/sastre09_1.wav"
uri = "sastre09_1"

ref = load_rttm("/Users/brono/GitHub/katana/ref_rttm/ref_sastre09_1.rttm")[uri]
hyp = load_rttm("/Users/brono/GitHub/katana/hyp_rttm/hyp_sastre09_1.rttm")[uri]
lang = load_rttm("/Users/brono/GitHub/katana/lang_rttm/lang_sastre09_1.rttm")[uri]


def play_audio_between(start_time_sec, end_time_sec, audio_file_path):
    start_time_ms = start_time_sec * 1000
    end_time_ms = end_time_sec * 1000
    audio = AudioSegment.from_file(audio_file_path)
    segment = audio[start_time_ms:end_time_ms]
    play(segment)
    time.sleep(2)


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
    # compute_der(ref, hyp)
    # analysis = compute_lang_error_rates(uri, ref, hyp, lang)

    """
    for i, seg in enumerate(analysis.lang_conf_error_map.itersegments()):

        play_audio_between(seg.start, seg.end, audio_file_path )
        print(f"{i}: {seg.start:.2f} - {seg.end:.2f}")
        time.sleep(3)
    """
    ref = Annotation()
    ref[Segment(0, 10)] = 'Speaker A'
    hyp = Annotation()
    hyp[Segment(0, 4)] = 'Speaker A'
    hyp[Segment(4, 7)] = 'Speaker B'
    hyp[Segment(7, 10)] = 'Speaker A'

    ref[Segment(0, 4)] = "ENG"
    ref[Segment(4, 5)] = "SPA"
    ref[Segment(5, 10)] = "ENG"
    crop = Annotation()
    crop[Segment(4, 5)] = "SPA"
    crop[Segment(5, 7)] = "ENG"



    plot_annotations([(ref, 'Reference'), (crop, "Confusion Segment"), (hyp, 'Hypothesis'), ])
    plt.show()
    sys.exit()
    #conf errors
    play_audio_between(44.16, 44.50, audio_file_path)
    play_audio_between(60.02, 60.78, audio_file_path)
    play_audio_between(76.96, 77.71, audio_file_path)
    play_audio_between(105.91, 106.20, audio_file_path)
    play_audio_between(156.34, 156.88, audio_file_path)
    play_audio_between(199.66, 200.60, audio_file_path)
    play_audio_between(202.54, 203.11, audio_file_path)
    play_audio_between(231.87, 232.92, audio_file_path)
    play_audio_between(232.92, 233.47, audio_file_path)
    play_audio_between(238.15, 239.05, audio_file_path)
    play_audio_between(286.12, 286.65, audio_file_path)
    play_audio_between(299.92, 300.69, audio_file_path)
    play_audio_between(387.37, 388.25, audio_file_path)
    play_audio_between(400.01, 400.86, audio_file_path)
    play_audio_between(409.53, 411.23, audio_file_path)
    play_audio_between(437.98, 438.66, audio_file_path)
    play_audio_between(438.66, 439.20, audio_file_path)
    play_audio_between(446.11, 446.46, audio_file_path)
    play_audio_between(472.00, 472.69, audio_file_path) 
    
