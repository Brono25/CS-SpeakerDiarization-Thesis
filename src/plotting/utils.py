import matplotlib.pylab as plt
from pyannote.core import notebook
from pyannote.core import Annotation, Segment

def plot_annotations(annotations_with_legends):
    num_subplots = len(annotations_with_legends)
    fig, axs = plt.subplots(num_subplots, 1, figsize=(5, 3 * num_subplots), sharex=True)
    if num_subplots == 1:
        axs = [axs]

    for idx, (annotation, legend) in enumerate(annotations_with_legends):
        notebook.plot_annotation(annotation, ax=axs[idx])
        axs[idx].set_title(legend)


def plot_timelines(timelines_with_legends):
    num_subplots = len(timelines_with_legends)
    fig, axs = plt.subplots(num_subplots, 1, figsize=(5, 3 * num_subplots), sharex=True)

    if num_subplots == 1:
        axs = [axs]

    for idx, (timeline, legend) in enumerate(timelines_with_legends):
        notebook.plot_timeline(timeline, ax=axs[idx])
        axs[idx].set_title(legend)


class LanguageErrorAnalysis:
    def __init__(self, uri):
        self.uri = uri
        self.ref_annotation = Annotation(uri=self.uri)
        self.lang_segments = Annotation(uri=self.uri)
        self.hyp_annotation = Annotation(uri=self.uri)
        self.confused_spa = 0
        self.confused_eng = 0
        self.missed_eng = 0
        self.missed_spa = 0

    def merge_annotations(self):
        self.merged_annotation = self.ref_annotation.update(self.lang_segments)

    def plot_annotation(self, ref_title="Reference", hyp_title="Hypothesis"):
        fig, axs = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        self.merge_annotations()
        annotations = [
            (self.merged_annotation, ref_title),
            (self.hyp_annotation, hyp_title),
        ]

        for idx, (annotation, legend) in enumerate(annotations):
            notebook.plot_annotation(annotation, ax=axs[idx])
            axs[idx].set_title(legend)

        fig.suptitle("Test Annotation")
        plt.show()


def combine_annotations(*annotations):
    combined_annotation = Annotation()
    offset = 0

    for annotation in annotations:
        for segment, track in annotation.itertracks():
            new_segment = Segment(segment.start + offset, segment.end + offset)
            combined_annotation[new_segment] = annotation[segment, track]

        offset += annotation.get_timeline().extent().duration

    return combined_annotation
