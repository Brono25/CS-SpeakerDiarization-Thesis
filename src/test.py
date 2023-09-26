import sys
import os
import re
from pyannote.database.util import load_rttm
from pyannote.core import Timeline, Annotation
import pandas as pd
import matplotlib.pyplot as plt

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

# local imports
from src.functions.transcript import (
    Transcript,
    Timeline,
    load_transcript_from_file,
)  # noqa: E402
from src.functions.cs_diarization_metrics import CSDiarizationMetrics
from src.functions.helper import plot_annotations
from src.functions.confusion_matrix import ConfusionMatrix






class Data:
    def __init__(self, tr_file, hyp_file):
        # Fie paths and IO
        self.tr_file = tr_file
        self.uri = self.get_uri()
        self.hyp_file = self.validate_hypothesis(hyp_file)
        self.root_dir = self.get_root()
        self.pyannote_dir = f"{self.root_dir}/pyannote"
        self.output_file = f"{self.root_dir}/pyannote/{self.uri}"

        # Transcripts and Annotations
        self.tr: Transcript = load_transcript_from_file(self.tr_file, self.uri)
        self.ref: Annotation = self.tr.get_ref_annotation()
        self.lang: Annotation = self.tr.get_language_annotation()
        self.hyp: Annotation = load_rttm(self.hyp_file)[self.uri]
        self.conf_lang: Annotation = self.get_language_confusion_annotation()
        self.conf_label: Annotation = self.hyp.crop(self.get_confusion_timeline())
        self.conf_til: Timeline = self.conf_label.get_timeline()

    def get_uri(self):
        file_name = os.path.basename(self.tr_file)
        uri = os.path.splitext(file_name)[0]
        return uri

    def get_root(self):
        root = os.path.dirname(self.tr_file)
        return root

    def get_confusion_timeline(self) -> Timeline:
        analysis = CSDiarizationMetrics(
            uri=self.uri, reference=self.ref, hypothesis=self.hyp
        )
        conf_tl = analysis._get_confusion_timeline()
        return conf_tl

    def get_language_confusion_annotation(self) -> Annotation:
        analysis = CSDiarizationMetrics(
            uri=self.uri,
            reference=self.ref,
            hypothesis=self.hyp,
            language_annotation=self.lang,
        )
        return analysis.language_confusion_annotation()

    def validate_hypothesis(self, hyp):
        hyp_name = os.path.basename(hyp)
        expected_filename = None
        if "_pyannote.rttm" in hyp_name:
            expected_filename = f"{self.uri}_pyannote.rttm"

        if hyp_name != expected_filename:
            print(f"{hyp_name} is not a hypothesis rttm file", file=sys.stderr)
            sys.exit(1)

        return hyp
    

    def __str__(self):
        info_str = (
            f"     URI : {self.uri}\n"
            f"      TR : {os.path.basename(self.tr_file)}\n"
            f"     HYP : {os.path.basename(self.hyp_file)}\n"
            f"    ROOT : {self.root_dir}\n"
            f"OUT_FILE : {self.output_file}\n"
        )
        return info_str

    def plot_confusions(self):
        to_plot = [
            (self.ref, "Reference"),
            (self.hyp, "Hypothesis"),
            (self.lang, "Reference Language"),
            (self.conf_label, "Labeled Confusions"),
            (self.conf_lang, "Language Confusions"),
        ]
        plot_annotations(to_plot)
        plt.show()


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




def process_confusion_matrix(self, data: Data) -> ConfusionMatrix:

    cm = ConfusionMatrix()
    non, sssl, ssdl, dssl, dsdl = cm.keys
        



if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    file1 = sys.argv[1]
    uri = os.path.splitext(os.path.basename(file1))[0]
    file2 = f"{os.path.dirname(file1)}/pyannote/{uri}_pyannote.rttm"

    is_valid_input(file1, file2)
    tr_file, hyp_rttm = assign_input(file1, file2)
    data = Data(tr_file=tr_file, hyp_file=hyp_rttm)
    data.build_confusion_matrix()
    print(data)

    #data.plot_confusions()
