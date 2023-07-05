from pydub import AudioSegment
import pyaudio
import threading
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class AudioPlayer:
    def __init__(self, session_data):
        self.session_data = session_data
        self.stop_flag = False  
        self.normalizer = None
        self.zoom = 5
        self.audio = None
        self.time_vector = [0]
        self.sliced_array = [0]
        if self.session_data["audio_file"]:
            self.load_audio_file()
    


    def load_audio_file(self):
        self.audio = AudioSegment.from_file(self.session_data["audio_file"])
        samples = np.array(self.audio.get_array_of_samples())
        self.max_amp = np.abs(samples).max()
        self.get_audio_slice_data()

    
    def get_audio_slice_data(self):
        if not self.session_data["audio_file"]:
            return
        start_ms = self.session_data["curr_start"]
        end_ms = self.session_data["curr_end"]
        self.sliced_audio = self.audio[start_ms:end_ms]
        self.normalizer = self.max_amp / self.zoom
        samples = np.array(self.sliced_audio.get_array_of_samples())
        self.sliced_array = samples / self.normalizer
        self.time_vector = np.arange(len(samples)) / self.sliced_audio.frame_rate * 1000 
        self.time_vector += self.session_data["curr_start"]


    def play_audio_slice(self):
        if self.sliced_audio is None:  
            print("Error: sliced_audio is None")
            return

        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(self.sliced_audio.sample_width),
                        channels=self.sliced_audio.channels,
                        rate=self.sliced_audio.frame_rate,
                        output=True)

        if hasattr(self, 'play_thread') and self.play_thread.is_alive():
            self.stop_audio()

        self.stop_flag = False  # reset stop flag before playing audio
        self.play_thread = threading.Thread(target=self.play_audio_in_thread, 
                         args=(self.sliced_audio, p, stream))
        self.play_thread.start()

    def play_audio_in_thread(self, sliced_audio, p, stream):
        chunk_size = 1024  # size of audio data to write to the stream at a time
        for i in range(0, len(sliced_audio.raw_data), chunk_size):
            if self.stop_flag:  # stop writing more data to the stream if stop flag is set
                break
            stream.write(sliced_audio.raw_data[i:i+chunk_size])
        stream.stop_stream()
        stream.close()
        p.terminate()


    def stop_audio(self):  # method to stop the audio
        self.stop_flag = True
        if hasattr(self, 'play_thread'):
            self.play_thread.join()  # wait for the audio playing thread to stop

