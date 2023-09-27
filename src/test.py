import sys
import os
import re
import matplotlib.pyplot as plt
import numpy as np

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.functions.confusion_matrix import (
    ConfusionMatrix,
    ConfusionTimelineAnalyser,
    ConfusionAnalysisData,
)


def usage():
    print("Usage: python", os.path.basename(sys.argv[0]), "<{uri}.tr>")


def is_valid_input(file1, file2):
    if not os.path.isfile(file1) or not os.path.isfile(file2):
        print("One or both of the provided files do not exist.")
        print(file1, file2)
        sys.exit(1)

    # Check file extensions
    ext1 = os.path.splitext(file1)[1]
    ext2 = os.path.splitext(file2)[1]

    if (ext1 != ".rttm" and ext1 != ".tr") or (ext2 != ".rttm" and ext2 != ".tr"):
        print("Both files should have either .rttm or .tr extensions.")
        sys.exit(1)


def assign_input(file1, file2):
    if file1.endswith(".tr"):
        tr_file = file1
        hyp_rttm = file2
    elif file2.endswith(".tr"):
        tr_file = file2
        hyp_rttm = file1
    return tr_file, hyp_rttm


def confusion_analysis(data: ConfusionAnalysisData, cm: ConfusionMatrix):
    analyser = ConfusionTimelineAnalyser(data=data, min_dur=0.5)

    for step_result in analyser:
        non1_key = None
        non2_key = None
        if step_result["lag_label"]:
            if step_result["lag_label"] == step_result["ref_label"]:
                key1_spkr = "SS"
            else:
                key1_spkr = "DS"

            if step_result["lag_lang"] == step_result["ref_lang"]:
                key1_lang = "SL"
            else:
                key1_lang = "DL"
        else:
            non1_key = "None"

        if step_result["lead_label"]:
            if step_result["lead_label"] == step_result["ref_label"]:
                key2_spkr = "SS"
            else:
                key2_spkr = "DS"

            if step_result["lead_lang"] == step_result["ref_lang"]:
                key2_lang = "SL"
            else:
                key2_lang = "DL"
        else:
            non2_key = "None"
        
        if non1_key:
            key1 = non1_key
        else:
            key1 = key1_spkr + ":" + key1_lang

        if non2_key:
            key2 = non2_key
        else:    
            key2 = key2_spkr + ":" + key2_lang
        cm.increment_count(key1, key2)


def plot_heatmap(matrix_dict):
    labels = list(matrix_dict.keys())
    data = np.array([[matrix_dict[row][col] for col in labels] for row in labels])

    fig, ax = plt.subplots()
    im = ax.imshow(data, cmap='viridis')

    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))

    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)

    plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

    for i in range(len(labels)):
        for j in range(len(labels)):
            text = ax.text(j, i, data[i, j], ha="center", va="center", color="w")

    ax.set_title("Confusion Matrix Heatmap")
    fig.tight_layout()
    plt.colorbar(im)
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)

    cm = ConfusionMatrix()
    for file in sys.argv[1:]:
        print(f"Processing {file}")
        file1 = file
        uri = os.path.splitext(os.path.basename(file1))[0]
        file2 = f"{os.path.dirname(file1)}/pyannote/{uri}_pyannote.rttm"

        is_valid_input(file1, file2)
        tr_file, hyp_rttm = assign_input(file1, file2)
        data = ConfusionAnalysisData(tr_file=tr_file, hyp_file=hyp_rttm)

        confusion_analysis(data, cm)

    print(cm)
    plot_heatmap(cm.matrix)

    # data.plot_confusions()
