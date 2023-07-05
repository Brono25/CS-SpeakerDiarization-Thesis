
import numpy as np
import tkinter as tk
from tkinter import filedialog
from pydub import AudioSegment
import pyaudio
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import threading

class AudioPlotter:
    def __init__(self, sliced_audio, start_time_ms):

        # Get audio samples and normalize them
        samples = np.array(sliced_audio.get_array_of_samples())
        normalized_samples = samples / np.max(np.abs(samples))
        # Create a time vector for x-axis in milliseconds
        # Add the start time to each time point in the vector
        time_vector = np.arange(len(normalized_samples)) / sliced_audio.frame_rate * 1000  # milliseconds
        time_vector += start_time_ms
        # Clear previous plot
        self.ax.clear()
        # Plot normalized samples with time vector as x-axis
        self.ax.plot(time_vector, normalized_samples)
        # Set plot labels and y-axis limits
        self.ax.set_xlabel('Time (ms)')  # now it's in milliseconds
        self.ax.set_ylabel('Amplitude')
        self.ax.set_ylim(-1,1)
        # Set x-axis limits to match the audio segment
        self.ax.set_xlim(time_vector[0], time_vector[-1])
        # Manually set x-ticks to include first and last value
        self.ax.set_xticks([time_vector[0], time_vector[-1]])
        # Draw plot
        #plt.xticks(rotation=45)
        self.graph.draw()
        self.window.update_idletasks()  # update GUI display


       
