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

def combine_annotations(*annotations):
    combined_annotation = Annotation()
    offset = 0

    for annotation in annotations:
        for segment, track in annotation.itertracks():
            new_segment = Segment(segment.start + offset, segment.end + offset)
            combined_annotation[new_segment] = annotation[segment, track]

        offset += annotation.get_timeline().extent().duration

    return combined_annotation
