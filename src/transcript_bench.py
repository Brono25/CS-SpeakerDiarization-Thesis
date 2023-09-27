import matplotlib.pyplot as plt
import numpy as np

data_dict = {
    "None": {"None": 0, "SS:SL": 2, "SS:DL": 1, "DS:SL": 0, "DS:DL": 2},
    "SS:SL": {"None": 0, "SS:SL": 42, "SS:DL": 23, "DS:SL": 84, "DS:DL": 32},
    "SS:DL": {"None": 0, "SS:SL": 18, "SS:DL": 15, "DS:SL": 29, "DS:DL": 16},
    "DS:SL": {"None": 1, "SS:SL": 91, "SS:DL": 19, "DS:SL": 253, "DS:DL": 49},
    "DS:DL": {"None": 0, "SS:SL": 39, "SS:DL": 19, "DS:SL": 42, "DS:DL": 52},
}

keys = list(data_dict.keys())
vals = np.array([[data_dict[row][col] for col in keys] for row in keys])

fig, ax = plt.subplots()
cax = ax.matshow(vals, cmap='inferno')
fig.colorbar(cax)

ax.set_xticklabels([''] + keys)
ax.set_yticklabels([''] + keys)
plt.show()
