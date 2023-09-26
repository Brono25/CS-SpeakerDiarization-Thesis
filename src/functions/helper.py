import os

import matplotlib
import matplotlib.pylab as plt
from pyannote.core import notebook


fig_num = 0


def image_timeline(timeline, legend):
    uri = timeline.uri
    fig, axs = plt.subplots(1, 1, figsize=(10, 6), sharex=True)
    notebook.plot_timeline(timeline, ax=axs)
    plt.tight_layout()
    axs.set_title(legend)
    image_path = os.path.join("./images/", f"{legend}.png")
    plt.savefig(image_path)
    print(f"Plot saved as {image_path}")


def plot_annotations(annotations_with_legends):
    num_subplots = len(annotations_with_legends)

    # Create the appropriate number of subplots
    fig, axs = plt.subplots(num_subplots, 1, figsize=(5, 3 * num_subplots), sharex=True)

    # Make sure axs is a list even if num_subplots is 1
    if num_subplots == 1:
        axs = [axs]

    for idx, (annotation, legend) in enumerate(annotations_with_legends):
        notebook.plot_annotation(annotation, ax=axs[idx])
        axs[idx].set_title(legend)
        

    # plt.tight_layout()
    # plt.show(block=False)


def plot_timelines(timelines_with_legends):
    num_subplots = len(timelines_with_legends)

    # Create the appropriate number of subplots
    fig, axs = plt.subplots(num_subplots, 1, figsize=(5, 3 * num_subplots), sharex=True)

    # Make sure axs is a list even if num_subplots is 1
    if num_subplots == 1:
        axs = [axs]

    for idx, (timeline, legend) in enumerate(timelines_with_legends):
        notebook.plot_timeline(timeline, ax=axs[idx])
        axs[idx].set_title(legend)

    # plt.tight_layout()
    # plt.show(block=False)
