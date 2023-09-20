import pyaudio
from pyannote.audio import Inference
from pyannote.core import Segment
import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt

# Replace 'audio' with the path to your audio file
audio = "/Users/brono/GitHub/tr-editer/demo/count.wav"

# Load the pre-trained embedding model
from pyannote.audio import Model

model = Model.from_pretrained(
    "pyannote/embedding", use_auth_token="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"
)

# Initialize inference
inference = Inference(model, window="whole")

# Define the time segments you want to extract embeddings from
x1 = Segment(0.050, 0.625)
x2 = Segment(0.750, 1.250)
x3 = Segment(1.350, 1.800)
x4 = Segment(1.950, 2.500)
x5 = Segment(2.550, 3.200)
x6 = Segment(3.225, 3.850)
x7 = Segment(3.875, 4.500)
x8 = Segment(4.525, 5.200)
x9 = Segment(5.275, 5.725)
x10 = Segment(5.750, 6.366)


# Extract the embeddings from the audio segments
e1 = inference.crop(audio, x1).reshape(1, -1)
e2 = inference.crop(audio, x2).reshape(1, -1)
e3 = inference.crop(audio, x3).reshape(1, -1)
e4 = inference.crop(audio, x4).reshape(1, -1)
e5 = inference.crop(audio, x5).reshape(1, -1)
e6 = inference.crop(audio, x6).reshape(1, -1)
e7 = inference.crop(audio, x7).reshape(1, -1)
e8 = inference.crop(audio, x8).reshape(1, -1)
e9 = inference.crop(audio, x9).reshape(1, -1)
e10 = inference.crop(audio, x10).reshape(1, -1)


# Concatenate the reshaped embeddings
combined_embedding = np.concatenate((e1, e2, e3, e4, e5, e6, e7, e8, e9, e10), axis=0)

# Create a t-SNE model with 2D output dimensions
tsne_model = TSNE(n_components=2, random_state=0, perplexity=2)

# Fit the t-SNE model to your combined reshaped embeddings
tsne_embeddings = tsne_model.fit_transform(combined_embedding)

# Visualize the t-SNE embeddings as a scatter plot
plt.scatter(tsne_embeddings[:, 0], tsne_embeddings[:, 1])
plt.title("t-SNE Visualization of Embeddings")
plt.show()
