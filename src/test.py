import sys
import os
import re



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


def confusion_analysis(data: ConfusionAnalysisData) -> ConfusionMatrix:
    cm = ConfusionMatrix()
    analyser = ConfusionTimelineAnalyser(
        data=data,
        confusion_matrix=cm,
        min_dur=0.5
    )
    for window in analyser:
        pass
        #print(window)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)
    
    file1 = sys.argv[1]
    uri = os.path.splitext(os.path.basename(file1))[0]
    file2 = f"{os.path.dirname(file1)}/pyannote/{uri}_pyannote.rttm"

    is_valid_input(file1, file2)
    tr_file, hyp_rttm = assign_input(file1, file2)
    data = ConfusionAnalysisData(tr_file=tr_file, hyp_file=hyp_rttm)
    confusion_analysis(data)
    print(data)

    # data.plot_confusions()
