import os
import re
import sys
import threading
import tkinter as tk
from tkinter import filedialog

import numpy as np
import pyaudio
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from pyannote.database.util import load_rttm
from pydub import AudioSegment


class MediaPlayer:
    def __init__(self, audio_file):
        self.audio = AudioSegment.from_file(audio_file)
        self.play_thread = None
        self.stop_flag = False

    @property
    def duration(self):
        return self.audio.duration_seconds

    def play_segment(self, start, end):
        start = start * 1000  # convert to milliseconds
        end = end * 1000
        self.sliced_audio = self.audio[start:end]
        p = pyaudio.PyAudio()
        stream = p.open(
            format=p.get_format_from_width(self.sliced_audio.sample_width),
            channels=self.sliced_audio.channels,
            rate=self.sliced_audio.frame_rate,
            output=True,
        )

        if self.play_thread is not None and self.play_thread.is_alive():
            self.stop_playback()

        self.stop_flag = False
        self.play_thread = threading.Thread(
            target=self._play_audio_in_thread, args=(self.sliced_audio, p, stream)
        )
        self.play_thread.start()

    def _play_audio_in_thread(self, sliced_audio, p, stream):
        chunk_size = 1024
        for i in range(0, len(sliced_audio.raw_data), chunk_size):
            if self.stop_flag:
                break
            stream.write(sliced_audio.raw_data[i : i + chunk_size])
        stream.stop_stream()
        stream.close()
        p.terminate()

    def stop_playback(self):
        self.stop_flag = True
        if self.play_thread is not None:
            self.play_thread.join()  # Wait for the completion of the thread.

    def get_audio_array(self, start, end):
        slice = self.audio[start * 1000 : end * 1000]
        audio_array = np.array(slice.get_array_of_samples())
        num_samples = audio_array.shape[0]
        time_array = np.linspace(start, end, num_samples)
        return time_array, audio_array


class AudioGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("RTTM Player")
        self.session_state = {
            "curr_index": 0,
            "audio_start": 0,
            "audio_end": 0,
            "segment_start": 0,
            "segment_end": 0,
        }
        self.session_data = {
            "uri": None,
            "rttm_path": None,
            "audio_path": None,
            "annotation": None,
        }

        self.init_figure()
        self.init_open()
        self.init_state_frame()
        self.init_buttons()
        self.window.mainloop()

    def open_button_file(self):
        rttm_path = filedialog.askopenfilename(filetypes=[("RTTM files", "*.rttm")])
        self.load_rttm_file(rttm_path)
        self.file_label.config(text=self.session_data["uri"])

    def load_rttm_file(self, rttm_path):
        filename = os.path.basename(rttm_path).split(".")[0]

        with open(rttm_path, 'r') as file:
            uri = file.readline().strip().split(' ')[1]



        
        annotation = load_rttm(rttm_path)[uri]  #all related rttms must have same uri

        segments_with_labels = [
            (segment, label) for segment, _, label in annotation.itertracks(yield_label=True)
        ]

        self.session_data["uri"] = uri
        self.session_data["rttm_path"] = rttm_path
        self.session_data["segments_with_labels"] = segments_with_labels
        segment, label = segments_with_labels[0]

        self.session_state = {
            "curr_index": 0,
            "audio_start": segment.start,
            "audio_end": segment.end,
            "segment_start": segment.start,
            "segment_end": segment.end,
            "label": label
        }
        if self.session_data["rttm_path"] and self.session_data["audio_path"]:
            self.activate_buttons()
            self.draw_audio()
        self.update_state_info()





    def activate_buttons(self):
        self.play_button["state"] = tk.NORMAL
        self.stop_button["state"] = tk.NORMAL
        self.prev_button["state"] = tk.NORMAL
        self.next_button["state"] = tk.NORMAL
        self.extend_button["state"] = tk.NORMAL
        self.decrease_button["state"] = tk.NORMAL
 
    def deactivate_buttons(self):
        self.play_button["state"] = tk.DISABLED
        self.stop_button["state"] = tk.DISABLED
        self.prev_button["state"] = tk.DISABLED
        self.next_button["state"] = tk.DISABLED
        self.extend_button["state"] = tk.DISABLED
        self.decrease_button["state"] = tk.DISABLED


    def open_audio_file(self):
        audio_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav")]) 
        self.audio_file_label.config(text=os.path.basename(audio_path))
        self.media_player = MediaPlayer(audio_path)

        self.session_data["audio_path"] = audio_path
        if self.session_data["rttm_path"] and self.session_data["audio_path"]:
            self.activate_buttons()
            self.draw_audio()
   

    def draw_audio(self):
        self.ax.clear()
        audio_start = self.session_state["audio_start"]
        audio_end = self.session_state["audio_end"]
        time, amplitude = self.media_player.get_audio_array(audio_start, audio_end)
        self.ax.plot(time, amplitude) 
        segment_start = self.session_state["segment_start"]
        segment_end = self.session_state["segment_end"]
        label = self.session_state["label"]  
        self.ax.axvline(segment_start, color="r", label=label)  
        self.ax.axvline(segment_end, color="r")  
        self.ax.legend(loc='best') 
        self.ax.legend(loc='upper right') 
        self.canvas.draw()



    def play_audio(self):
        self.media_player.stop_playback()
        audio_start = self.session_state["audio_start"]
        audio_end = self.session_state["audio_end"]
        self.media_player.play_segment(audio_start, audio_end)

    def stop_audio(self):
        self.media_player.stop_playback()

    def prev_state(self):
        index = self.session_state["curr_index"]
        if index > 0:
            index -= 1
            self.initialise_state(index)
            self.media_player.stop_playback()
            self.media_player.play_segment(
                self.session_state["audio_start"], self.session_state["audio_end"]
            )
            self.draw_audio()

    def next_state(self):
        index = self.session_state["curr_index"]

        if index < len(self.session_data["segments_with_labels"]) - 1:
            index += 1
            self.initialise_state(index)
            self.media_player.stop_playback()
            self.media_player.play_segment(
                self.session_state["audio_start"], self.session_state["audio_end"]
            )
            self.draw_audio()

    def go_to_state(self, event):
        if not self.session_data["rttm_path"]:
            return
        try:
            index = int(self.state_entry.get())
            if index <= len(self.session_data["segments_with_labels"]) and index >= 0:
                self.initialise_state(index)
                self.media_player.stop_playback()
                self.media_player.play_segment(
                    self.session_state["audio_start"], self.session_state["audio_end"]
                )
                self.draw_audio()
            else:
                print("Error: index out of bounds")
        except ValueError:
            print("Error: invalid index")

    def initialise_state(self, index):
        segment, label = self.session_data["segments_with_labels"][index]

        self.session_state = {
            "curr_index": index,
            "audio_start": segment.start,
            "audio_end": segment.end,
            "segment_start": segment.start,
            "segment_end": segment.end,
            "label": label
        }
        self.update_state_info()



    def extend_audio(self):
        self.session_state["audio_start"] -= 0.1
        self.session_state["audio_end"] += 0.1
        if self.session_state["audio_start"] < 0:
            self.session_state["audio_start"] = 0
        if self.session_state["audio_end"] > self.media_player.duration:
            self.session_state["audio_end"] = self.media_player.duration
        self.draw_audio()

    def decrease_audio(self):
        self.session_state["audio_start"] += 0.1
        self.session_state["audio_end"] -= 0.1
        if self.session_state["audio_start"] > self.session_state["segment_start"]:
            self.session_state["audio_start"] = self.session_state["segment_start"]
        if self.session_state["audio_end"] < self.session_state["segment_end"]:
            self.session_state["audio_end"] = self.session_state["segment_end"]
        self.draw_audio()

    def update_state_info(self):
        index = self.session_state["curr_index"]
        total_states = len(self.session_data["segments_with_labels"])
        state = f"{index + 1} / {total_states}"
        self.state_info_label.config(text=state)

    def run(self):
        self.window.mainloop()

    def init_buttons(self):
        self.frame = tk.Frame(self.window)
        self.frame.grid(row=1, column=0, columnspan=5)

        self.state_label = tk.Label(self.frame, text="Go to state:")
        self.state_label.pack(side="left")

        self.state_entry = tk.Entry(self.frame, width=5)
        self.state_entry.bind("<Return>", self.go_to_state)
        self.state_entry.pack(side="left")

        self.prev_button = tk.Button(
            self.frame, text="Previous", command=self.prev_state, state=tk.DISABLED
        )
        self.prev_button.pack(side="left")

        self.next_button = tk.Button(
            self.frame, text="Next", command=self.next_state, state=tk.DISABLED
        )
        self.play_button = tk.Button(
            self.frame, text="Play", command=self.play_audio, state=tk.DISABLED
        )
        self.play_button.pack(side="left")

        self.next_button.pack(side="left")

        self.stop_button = tk.Button(
            self.frame, text="Stop", command=self.stop_audio, state=tk.DISABLED
        )
        self.stop_button.pack(side="left")

        self.decrease_button = tk.Button(
            self.frame, text="-", command=self.decrease_audio, state=tk.DISABLED
        )
        self.decrease_button.pack(side="left")

        self.extend_button = tk.Button(
            self.frame, text="+", command=self.extend_audio, state=tk.DISABLED
        )
        self.extend_button.pack(side="left")

    def init_open(self):
        self.open_frame = tk.Frame(self.window)
        self.open_frame.grid(row=0, column=0, columnspan=5, sticky="w")
        
        # Open RTTM File Button
        self.open_button = tk.Button(self.open_frame, text="Open RTTM", command=self.open_button_file)
        self.open_button.pack(side="left")
        self.file_label = tk.Label(self.open_frame, text="No RTTM file selected")
        self.file_label.pack(side="left")

        # Open Audio File Button
        self.open_audio_button = tk.Button(self.open_frame, text="Open Audio", command=self.open_audio_file)
        self.open_audio_button.pack(side="left")
        
        # Audio File Label
        self.audio_file_label = tk.Label(self.open_frame, text="No audio file selected")
        self.audio_file_label.pack(side="left")


    def init_figure(self):
        self.fig = Figure(figsize=(9, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=5, column=0, columnspan=5, sticky="s")

    def init_state_frame(self):
        self.state_frame = tk.Frame(self.window)
        self.state_frame.grid(row=2, column=0, columnspan=5)
        self.state_label = tk.Label(self.state_frame, text="Current Index: ")
        self.state_label.pack(side="left")
        self.state_info_label = tk.Label(self.state_frame, text="No rttm file loaded")
        self.state_info_label.pack(side="left")


if __name__ == "__main__":
    gui = AudioGUI()
    gui.run()
