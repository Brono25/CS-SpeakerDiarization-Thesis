from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import re
from collections import defaultdict
import sys
import re
import pickle
import glob

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

ORANGE = "#FF8100"
LIGHT_ORANGE = "#FBCA04"
LIGHT_BLUE = "#79DCFF"
BLUE = "#007EFF"

SPEAKER1_SPA = LIGHT_BLUE
SPEAKER1_ENG = BLUE
SPEAKER2_SPA = ORANGE
SPEAKER2_ENG = LIGHT_ORANGE


def load_embedding(filename):
    with open(filename, "rb") as f:
        bundle = pickle.load(f)
    return bundle


def get_colours(data):
    colour_map = defaultdict(dict)
    colour_map[data["speaker1"]]["SPA"] = SPEAKER1_SPA
    colour_map[data["speaker1"]]["ENG"] = SPEAKER1_ENG
    colour_map[data["speaker2"]]["SPA"] = SPEAKER2_SPA
    colour_map[data["speaker2"]]["ENG"] = SPEAKER2_ENG
    colours = []
    for label, lang in data["label_map"]:
        colours.append(colour_map[label][lang])
    return colours


from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import re
from collections import defaultdict
import sys
import re
import pickle
import glob

root = re.search(r"(.*/CS-SpeakerDiarization-Thesis)", __file__).group(1)
sys.path.append(root)

file_list = [
    "embeddings/herring08_embedding.pkl",
    "embeddings/sastre01_embedding.pkl",
    "embeddings/herring13_embedding.pkl",
    "embeddings/zeledon14_embedding.pkl",
    "embeddings/sastre06_embedding.pkl",
    "embeddings/sastre09_embedding.pkl",
    "embeddings/sastre11_embedding.pkl",
    "embeddings/zeledon08_embedding.pkl",
    "embeddings/herring06_embedding.pkl",
    "embeddings/zeledon04_embedding.pkl",
    "embeddings/herring10_embedding.pkl",
    "embeddings/herring07_embedding.pkl",
]


ORANGE = "#FF8100"
LIGHT_ORANGE = "#FBCA04"
LIGHT_BLUE = "#79DCFF"
BLUE = "#007EFF"

SPEAKER1_SPA = LIGHT_BLUE
SPEAKER1_ENG = BLUE
SPEAKER2_SPA = ORANGE
SPEAKER2_ENG = LIGHT_ORANGE


def load_embedding(filename):
    with open(filename, "rb") as f:
        bundle = pickle.load(f)
    return bundle


def get_colours(data):
    colour_map = defaultdict(dict)
    colour_map[data["speaker1"]]["SPA"] = SPEAKER1_SPA
    colour_map[data["speaker1"]]["ENG"] = SPEAKER1_ENG
    colour_map[data["speaker2"]]["SPA"] = SPEAKER2_SPA
    colour_map[data["speaker2"]]["ENG"] = SPEAKER2_ENG
    colours = []
    for label, lang in data["label_map"]:
        colours.append(colour_map[label][lang])
    return colours


fig, axes = plt.subplots(3, 4, figsize=(15, 10))

for idx, file in enumerate(file_list):
    data = load_embedding(file)
    colours = get_colours(data)

    ax = axes[idx // 4, idx % 4]

    tsne = TSNE(n_components=2, random_state=1)
    X_tsne = tsne.fit_transform(data["embeddings"])

    for i, (x, y) in enumerate(X_tsne):
        ax.scatter(x, y, c=colours[i])

    ax.set_title(file.split("/")[-1].replace("_embedding.pkl", ""), fontsize=12)
    ax.tick_params(axis="both", which="major", labelsize=8)

legend_labels = {
    SPEAKER1_SPA: f"\nSpeaker 1\n Spanish\n",
    SPEAKER1_ENG: f"\nSpeaker 1\n English\n",
    SPEAKER2_SPA: f"\nSpeaker 2\n Spanish\n",
    SPEAKER2_ENG: f"\nSpeaker 2\n English\n",
}
handles = [
    plt.Line2D(
        [0],
        [0],
        marker="o",
        color="w",
        label=legend_labels[color],
        markersize=11,
        markerfacecolor=color,
    )
    for color in legend_labels
]
fig.legend(
    handles=handles,
    loc="lower center",
    fontsize=12,
    labelspacing=0.5,
    ncol=len(legend_labels),
    frameon=False,
)  # Set ncol and turned off frame

fig.suptitle(
    "Code-Switching Speech Embeddings", fontsize=30, y=0.99
)  # Increase font size and adjust y value

fig.subplots_adjust(top=0.9)  # Adjust the top margin to push subplots down

plt.show()
