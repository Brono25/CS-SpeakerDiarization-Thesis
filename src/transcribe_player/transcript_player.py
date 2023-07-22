
from audio_player import AudioPlayer
import re
import sys 
from gui import GUI
from utilities import Utilities
import os

class TranscriptPlayer:
    def __init__(self, window):

        self.session_data = {}
        self.util = Utilities(session_data=self.session_data)
        self.initialise_session()
        self.audio = AudioPlayer(self.session_data)
        self.gui = GUI(window=window, 
                       create_new_session=self.create_new_session,
                       session_data=self.session_data,
                       util=self.util,
                       audio=self.audio)
        
        self.audio.get_audio_slice_data()
        self.gui.plot_audio_data()
        self.gui.update_bordertime_labels()

    def initialise_session(self):
        loaded_data = self.util.load_savefile()
        if loaded_data is not None:
            self.session_data.clear()
            self.session_data.update(loaded_data)
            

        


    #called by the open button
    def create_new_session(self):
        new_filename = self.gui.open_file_button()
        self.update_session_data(new_filename)
        self.util.write_session_data()
        self.gui.set_timestamp_boxes()
        self.gui.update_next_line_state()
        self.gui.print_content_line()
        self.gui.set_filename_label()
        self.audio.load_audio_file()
        self.audio.get_audio_slice_data()
        self.gui.update_bordertime_labels()
        self.gui.plot_audio_data()
        


    def update_session_data(self, file):
        filename = os.path.basename(file)
        id = re.search(r"([a-zA-Z0-9_]*?_)?(.*)\.txt", filename).group(2)
        curr_index = 0
        audio_file = f"./wav/{id}.wav"
        content = self.util.load_content(file)
        match = re.search(r"(\d+)_(\d+)", content[0])
        if match:
            curr_start = int(match.group(1))
            curr_end = int(match.group(2))
        else:
            print("Error: No timestamp found", file=sys.stderr)
            sys.exit(1)

        self.session_data["filename"] = file
        self.session_data["id"] = id
        self.session_data["audio_file"] = audio_file
        self.session_data["curr_index"] = curr_index
        self.session_data["curr_start"] = curr_start
        self.session_data["curr_end"] = curr_end
        self.session_data["content"] = content

    
