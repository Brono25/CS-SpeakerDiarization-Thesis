

# Always use CS-SpeakerDiarization-Thesis as root
import sys
import re

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)
import os
import matplotlib.pyplot as plt
from pyannote.core import Segment
from pyannote.metrics.diarization import DiarizationErrorRate
from src.functions.transcript import Transcript, create_tr_from_rttm
from src.functions.cs_dataset_metrics import DatasetMetrics
import numpy as np
from src.functions.transcript import Transcript, create_tr_from_rttm
from src.functions.cs_dataset_metrics import DatasetMetrics

files = [
    "/Users/brono/GitHub/confusion_analysis/data/herring08.tr",
    "/Users/brono/GitHub/confusion_analysis/data/sastre01.tr",
    "/Users/brono/GitHub/confusion_analysis/data/herring13.tr",
    "/Users/brono/GitHub/confusion_analysis/data/zeledon14.tr",
    "/Users/brono/GitHub/confusion_analysis/data/sastre06.tr",
    "/Users/brono/GitHub/confusion_analysis/data/sastre09.tr",
    "/Users/brono/GitHub/confusion_analysis/data/sastre11.tr",
    "/Users/brono/GitHub/confusion_analysis/data/zeledon08.tr",
    "/Users/brono/GitHub/confusion_analysis/data/herring06.tr",
    "/Users/brono/GitHub/confusion_analysis/data/zeledon04.tr",
    #"/Users/brono/GitHub/confusion_analysis/data/herring10.tr",
    #"/Users/brono/GitHub/confusion_analysis/data/herring07.tr",
]

min_length = 500


def clamp_transcript(tr, min_time, max_time):
    sub_tr = tr[min_time:max_time]
    new_tr = Transcript(uri=tr.uri)

    # Handle first segment
    first_segment = list(sub_tr.items())[0][0]
    if first_segment.start < min_time:
        new_first_segment = Segment(min_time, first_segment.end)
        if new_first_segment.duration > 0:  # Check added here
            label, lang, text = sub_tr[first_segment]
            new_tr[new_first_segment] = (label, lang, text)
    else:
        label, lang, text = sub_tr[first_segment]
        new_tr[first_segment] = (label, lang, text)

    # Handle segments between first and last
    for segment, values in list(sub_tr.items())[1:-1]:
        new_tr[segment] = values

    # Handle last segment
    last_segment = list(sub_tr.items())[-1][0]
    if last_segment.end > max_time:
        new_last_segment = Segment(last_segment.start, max_time)
        if new_last_segment.duration > 0:  # Check added here
            label, lang, text = sub_tr[last_segment]
            new_tr[new_last_segment] = (label, lang, text)
    else:
        label, lang, text = sub_tr[last_segment]
        new_tr[last_segment] = (label, lang, text)

    return new_tr


class SlidingWindow:
    def __init__(self, window_len, min_val, max_val):
        self.initial_window_len = window_len
        self.window_len = window_len
        self.step = window_len / 2

        self.min_val = min_val
        self.max_val = max_val

        self.current_start = self.min_val
        self.current_end = None

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_start + self.step > self.max_val:
            if self.window_len >= (self.max_val - self.min_val):
                raise StopIteration
            self.window_len *= 1.5
            self.step = self.window_len / 2
            self.current_start = self.min_val

        window_start = self.current_start

        if self.current_start + self.window_len > self.max_val:
            window_end = self.max_val
            self.current_start = (
                self.max_val + self.step
            )  
        else:
            window_end = self.current_start + self.window_len
            self.current_start += self.step

        self.current_end = window_end

        if window_end != window_start:
            return (window_start, window_end)


def process_file(file):
    i_indices = []
    m_indices = []
    ders = []

    uri = os.path.basename(file).split(".")[0]
    print(f"processing {uri}")
    hyp_file = f"/Users/brono/GitHub/confusion_analysis/data/pyannote/{uri}_pyannote.rttm"
    hyp = create_tr_from_rttm(hyp_file, uri=uri)
    tr = Transcript.load_transcript_from_file(file, uri=uri)

    sw = SlidingWindow(window_len=150, min_val=0.0, max_val=tr.length_time)
    for start_time, end_time in sw:
        sub_tr = clamp_transcript(tr, start_time, end_time)
        sub_hyp = clamp_transcript(hyp, start_time, end_time)
        metrics = DatasetMetrics(sub_tr)
        i_index = metrics.i_index()
        m_index = metrics.m_index()

        hyp_ann = sub_hyp.get_ref_annotation()
        ref_ann = sub_tr.get_ref_annotation()

        der = DiarizationErrorRate(collar=0.5, skip_overlap=True)
        der_value = der(ref_ann, hyp_ann)

        i_indices.append(i_index)
        m_indices.append(m_index)
        ders.append(der_value)
    
    return i_indices, m_indices, ders

def plot_grid(indices, ders, title, xlim, ylim):
    rows, cols = 3, 4
    fig, axs = plt.subplots(rows, cols, figsize=(12, 8))  

    for idx, file in enumerate(files):
        row, col = divmod(idx, cols)
        ax = axs[row][col]
        ax.scatter(indices[idx], ders[idx])
        
        # Calculate the line of best fit
        m, b = np.polyfit(indices[idx], ders[idx], 1)
        x = np.array(indices[idx])
        ax.plot(x, m*x + b, color='red')  
        
        # Add text for the slope
        slope_text = f"m = {m:.2f}"
        ax.text(0.05, 0.45, slope_text, transform=ax.transAxes, color='red')  
        
        uri = os.path.basename(file).split(".")[0]
        ax.set_title(f"{uri}: {title}")
        ax.set_xlabel(title)
        ax.set_ylabel("DER")
        ax.set_xlim(xlim)
        ax.set_ylim(ylim)
    
    plt.tight_layout()
    plt.show()

def plot_combined(indices_all, ders_all, title):
    fig, ax = plt.subplots(figsize=(10, 5))
    colour_map = plt.cm.viridis(np.linspace(0, 1, len(files)))
    
    # Flattening the indices_all and ders_all for the global LOBF calculation
    flat_indices = [idx for sublist in indices_all for idx in sublist]
    flat_ders = [der for sublist in ders_all for der in sublist]

    for idx, indices in enumerate(indices_all):
        ders = ders_all[idx]
        ax.scatter(indices, ders, c=[colour_map[idx] for _ in indices], label=os.path.basename(files[idx]).split(".")[0])

    # Calculate the line of best fit for combined data
    m, b = np.polyfit(flat_indices, flat_ders, 1)
    x_vals = np.linspace(min(flat_indices), max(flat_indices), 400)
    ax.plot(x_vals, m*x_vals + b, color='red', linestyle='--')
    
    # Add text for the slope
    slope_text = f"m = {m:.2f}"
    ax.text(0.05, 0.9, slope_text, transform=ax.transAxes, color='red')
    
    ax.set_title(f"{title} vs. DER (All Files)")
    ax.set_xlabel(title)
    ax.set_ylabel("DER")
    ax.legend(loc='upper left')
    
    plt.tight_layout()
    plt.show()
if __name__ == "__main__":
    i_indices_all = []
    m_indices_all = []
    ders_all = []

    for file in files:
        i_indices, m_indices, ders = process_file(file)
        i_indices_all.append(i_indices)
        m_indices_all.append(m_indices)
        ders_all.append(ders)

    #plot_grid(i_indices_all, ders_all, "I-index", [0, 0.5], [0, 0.41])
    #plot_grid(m_indices_all, ders_all, "M-index",[0, 1.05], [0, 0.55])
    plot_combined(i_indices_all, ders_all, "I-index")
    plot_combined(m_indices_all, ders_all, "M-index")