
import tkinter as tk
from tkinter import filedialog
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GUI:
    def __init__(self, window, create_new_session, session_data, util, audio):
        self.create_new_session = create_new_session
        self.window = window
        self.window.geometry("1100x850")
        self.session_data = session_data
        self.util = util
        self.audio = audio
        self.ax, self.fig = None, None

        self.init_row_0_buttons()
        self.create_space(1)
        self.init_row_1_buttons()
        self.init_row_2_buttons()
        self.init_row_3_buttons()
        self.init_plot()
        self.init_bottom_row_buttons()
        

    def create_space(self, row_number):
        spacer = tk.Label(self.window, text="", height=1)
        spacer.grid(row=row_number, column=0)

  
    def init_row_0_buttons(self):
        # Initialize the file frame
        self.row_0_frame = tk.Frame(self.window)
        self.row_0_frame.grid(sticky='nw')

        # Initialise open button
        self.open_button = tk.Button(self.row_0_frame, 
                                     text="Open", 
                                     command=self.create_new_session)
        self.open_button.grid(row=0, column=0)

        # Initialise filename variable and label
        self.filename_var = tk.StringVar()
        if self.session_data["filename"]:
            self.filename_var.set(self.session_data["id"])
        else:
            self.filename_var.set("No file opened")
        self.filename_label = tk.Label(self.row_0_frame, 
                                       textvariable=self.filename_var)
        self.filename_label.grid(row=0, column=2)

        # Initialise save file button
        self.save_file_button = tk.Button(self.row_0_frame, 
                                          text="Save File", 
                                          command=self.save_file)
        self.save_file_button.grid(row=0, column=1)

    def init_row_1_buttons(self):
        self.row_1_frame = tk.Frame(self.window)
        self.row_1_frame.grid()

        self.new_start_label = tk.Label(self.row_1_frame, text="")
        self.new_start_label.grid(row=0, column=1)
        self.new_end_label = tk.Label(self.row_1_frame, text="")
        self.new_end_label.grid(row=0, column=3)
        
        self.start_label = tk.Label(self.row_1_frame, text="Start time (ms):")
        self.start_label.grid(row=1, column=0)
        self.start_time = tk.StringVar()
        self.start_time.trace_add("write", self.start_time_callback) 
        self.start_entry = tk.Entry(self.row_1_frame, textvariable=self.start_time)
        self.start_entry.grid(row=1, column=1)  

        self.end_label = tk.Label(self.row_1_frame, text="End time (ms):")  
        self.end_label.grid(row=1, column=2)
        self.end_time = tk.StringVar()
        self.end_time.trace_add("write", self.end_time_callback)  
        self.end_entry = tk.Entry(self.row_1_frame, textvariable=self.end_time)  
        self.end_entry.grid(row=1, column=3) 

        self.set_timestamp_boxes()

        self.save_edit_button = tk.Button(self.row_1_frame, text="Save Edit", command=self.save_edit)  
        self.save_edit_button.grid(row=1, column=4) 

    def update_bordertime_labels(self):
        if not self.session_data["filename"]:
            return
        prev_timestamp = ""
        next_timestamp = ""
        i = self.session_data["curr_index"]
        length = len(self.session_data["content"])
        if i <= 0:
            i = 0
        elif i >= length:
            i = length
     
        if i == 0:
            prev_timestamp = "0"
            next_timestamp = self.session_data["content"][i + 1]
            next_timestamp = re.search(r"(\d+)_\d+", next_timestamp).group(1)
        elif i == length:
            next_timestamp = self.session_data["content"][i]
            next_timestamp = re.search(r"\d)_(\d+)", next_timestamp).group(1)
            prev_timestamp = self.session_data["content"][i - 1]
            prev_timestamp = re.search(r"\d+_(\d+)", prev_timestamp).group(1)
        else:
            prev_timestamp = self.session_data["content"][i - 1]
            prev_timestamp = re.search(r"\d+_(\d+)", prev_timestamp).group(1)
            next_timestamp = self.session_data["content"][i + 1]
            next_timestamp = re.search(r"(\d+)_\d+", next_timestamp).group(1)

        self.new_start_label.config(text=prev_timestamp)
        self.new_end_label.config(text=next_timestamp)
        self.window.update_idletasks() 




    def init_row_2_buttons(self):
        self.row_3_frame = tk.Frame(self.window)
        self.row_3_frame.grid()

        self.zoom_out_button = tk.Button(self.row_3_frame, text="-",
                                        command=self.zoom_out)
        self.zoom_out_button.grid(row=0, column=0)
        self.zoom_in_button = tk.Button(self.row_3_frame, text="+",
                                        command=self.zoom_in)
        self.zoom_in_button.grid(row=0, column=1)
        self.prev_line_button = tk.Button(self.row_3_frame, text="Prev Line", 
                                        command=self.prev_line)
        self.prev_line_button.grid(row=0, column=2)
        self.next_line_button = tk.Button(self.row_3_frame, text="Next Line",
                                        command=self.next_line)
        self.next_line_button.grid(row=0, column=3)
        self.stop_button = tk.Button(self.row_3_frame, text="Delete Line",
                                        command=self.delete_line)
        self.stop_button.grid(row=0, column=4)
        self.play_button = tk.Button(self.row_3_frame, text="Play",
                                    command=self.audio.play_audio_slice)
        self.play_button.grid(row=0, column=5)
        self.stop_button = tk.Button(self.row_3_frame, text="Stop",
                                        command=self.audio.stop_audio)
        self.stop_button.grid(row=0, column=6)


    def init_row_3_buttons(self):
        # Initialize the frame for row 4
        self.row_4_frame = tk.Frame(self.window)
        self.row_4_frame.grid()

        # Initialise the StringVar for the content label
        self.content_var = tk.StringVar()
        self.content_var.set("")
        # Initialise content label
        self.content_label = tk.Label(self.row_4_frame,  # Added frame to the label
                                textvariable=self.content_var, 
                                fg="blue", 
                                font=("Helvetica", 20,),
                                wraplength=600)
        self.content_label.grid(row=0, column=0, columnspan=5)  
        self.update_next_line_state()
        self.print_content_line()

    def init_bottom_row_buttons(self):
        self.bottom_frame = tk.Frame(self.window)
        self.bottom_frame.grid()

        # Initialise label
        self.start_time_label = tk.Label(self.bottom_frame, text="Edit start time:")
        self.start_time_label.grid(row=0, column=0)

        # Initialise zoom out button
        self.m_start = tk.Button(self.bottom_frame, text="-50ms",
                                        command=self.decrement_start_time)
        self.m_start.grid(row=0, column=1)

        # Initialise zoom in button
        self.p_start = tk.Button(self.bottom_frame, text="+50ms",
                                        command=self.increment_start_time)
        self.p_start.grid(row=0, column=2)
        self.start_time_label = tk.Label(self.bottom_frame, text="Edit end time:")
        self.start_time_label.grid(row=0, column=3)

        # Initialise zoom out button
        self.m_start = tk.Button(self.bottom_frame, text="-50ms",
                                        command=self.decrement_end_time)
        self.m_start.grid(row=0, column=4)

        # Initialise zoom in button
        self.p_start = tk.Button(self.bottom_frame, text="+50ms",
                                        command=self.increment_end_time)
        self.p_start.grid(row=0, column=5)

    def increment_start_time(self):
        self.session_data["curr_start"] += 50
        self.audio.get_audio_slice_data()
        self.plot_audio_data()
        self.start_time.set(str())

    def decrement_start_time(self):
        self.session_data["curr_start"] -= 50
        if self.session_data["curr_start"] <= 0:
            self.session_data["curr_start"] = 0
        self.audio.get_audio_slice_data()
        self.plot_audio_data()

    def increment_end_time(self):
        self.session_data["curr_end"] += 50
        self.audio.get_audio_slice_data()
        self.plot_audio_data()
        self.start_time.set(str())

    def decrement_end_time(self):
        self.session_data["curr_end"] -= 50
        if self.session_data["curr_end"] <= 0:
            self.session_data["curr_end"] = 0
        self.audio.get_audio_slice_data()
        self.plot_audio_data()


    def open_file_button(self):
        return  filedialog.askopenfilename(filetypes=[("Transcript Files", ".txt")])
   

    def set_timestamp_boxes(self):
        start = "0"
        end = "0"
        if self.session_data["filename"] is not None:
            start = str(self.session_data["curr_start"])
            end = str(self.session_data["curr_end"])
        self.start_time.set(start)
        self.end_time.set(end)

    def start_time_callback(self, *args):
        if not self.ax:
            return 
        
        data = self.start_time.get()
        old_end_data = self.session_data["curr_end"]

        orig_data = self.session_data["content"][self.session_data["curr_index"]]
        orig_data = int(re.search(r"(\d+)_\d+", orig_data).group(1))

        if re.search(r"^\d+$", data):
            data = int(data)
            if data <= orig_data - 500:
                data = data - 500
            elif data <= old_end_data :
                self.session_data["curr_start"] = data
            else:
                self.session_data["curr_start"] = old_end_data
                self.start_time.set(old_end_data)
        else:
            print("Error: Invalid Entry")
        #self.util.update_content_timestamp()
        self.audio.get_audio_slice_data()
        self.plot_audio_data()

       
    def end_time_callback(self, *args):
        if not self.ax:
            return 
        data = self.end_time.get()
        old_data = self.session_data["curr_start"]
        if re.search(r"^\d+$", data) and old_data:
            data = int(data)
            if data >= old_data:
                self.session_data["curr_end"] = data
            else:
                self.session_data["curr_end"] = self.session_data["curr_start"]
        else:
            print("Error: Invalid Entry")
        #self.util.update_content_timestamp()
        self.audio.get_audio_slice_data()
        self.plot_audio_data()
       

    def update_next_line_state(self):
        self.next_line_button.configure(state="normal")
        self.window.update_idletasks()

    def print_content_line(self):

        if not self.session_data["filename"]:
            return
        i = self.session_data["curr_index"]
        length = len(self.session_data["content"])
        content = self.session_data["content"]
        if self.session_data["content"]:
            self.content_var.set(f"{i}/{length}: {content[i]}")
        else:
            self.content_var.set("No transcription loaded")
        self.window.update_idletasks()

    def next_line(self):
        # Ensure we don't go beyond the end of the content
        self.audio.stop_audio()
        self.plot_audio_data()
        if self.session_data["curr_index"] < len(self.session_data["content"]) - 1:
            self.session_data["curr_index"] += 1
            i = self.session_data["curr_index"]
            line = self.session_data["content"][i]
            match  = re.search(r"(\d+)_(\d+)", line)
            next_start = match.group(1)
            next_end = match.group(2)

            self.session_data["curr_start"] = int(next_start)
            self.session_data["curr_end"] = int(next_end)
            self.print_content_line()
            self.set_timestamp_boxes()
            self.util.write_session_data()
            self.play_media_slice()
            self.update_bordertime_labels()
            

    def prev_line(self):
        # Ensure we don't go beyond the start of the content
        self.audio.stop_audio()
        self.plot_audio_data()
        if self.session_data["curr_index"] > 0:
            self.session_data["curr_index"] -= 1
            i = self.session_data["curr_index"]
            line = self.session_data["content"][i]
            match  = re.search(r"(\d+)_(\d+)", line)
            prev_start = match.group(1)
            prev_end = match.group(2)

            self.session_data["curr_start"] = int(prev_start)
            self.session_data["curr_end"] = int(prev_end)
            self.util.write_session_data()
            self.print_content_line()
            self.set_timestamp_boxes()
            self.play_media_slice()
            self.update_bordertime_labels()

    def set_filename_label(self):
        self.filename_var.set(self.session_data["id"])

    def save_file(self):
        self.util.write_content()

    def init_plot(self):
        # Create a new matplotlib Figure and an Axes which fills it
        self.fig, self.ax = plt.subplots(figsize=(5, 3))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)  # A tk.DrawingArea

        # This will place the matplotlib figure on the GUI
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=5, column=0)
        self.ax.grid(True)



    def plot_audio_data(self):
        self.ax.clear()
        self.ax.plot(self.audio.time_vector, self.audio.sliced_array)
        self.ax.set_xlabel('Time (ms)')  # now it's in milliseconds
        self.ax.set_ylabel('Amplitude')
        self.ax.set_ylim(-1,1)
        self.ax.set_xlim(self.audio.time_vector[0], self.audio.time_vector[-1])
        self.ax.set_xticks([self.audio.time_vector[0], self.audio.time_vector[-1]])
        self.canvas.draw()
        self.window.update_idletasks()  # update GUI display

    def play_media_slice(self):
        self.audio.get_audio_slice_data()
        self.plot_audio_data()
        self.audio.play_audio_slice()
    
    def save_edit(self):
        
        self.util.update_content_timestamp()
        self.util.write_session_data()
        self.start_time.set(str(self.session_data["curr_start"]))
        self.end_time.set(str(self.session_data["curr_end"]))
        self.print_content_line()

    def zoom_in(self):
        self.audio.get_audio_slice_data()
        self.audio.zoom += 1
        if self.audio.zoom >= 10:
            self.audio.zoom = 10
        self.plot_audio_data()


    def zoom_out(self):
        self.audio.get_audio_slice_data()
        self.audio.zoom -= 1
        if self.audio.zoom <= 1:
            self.audio.zoom = 1
        self.plot_audio_data()
    
    def delete_line(self):
        i = self.session_data["curr_index"]
        line = self.session_data["content"][i]
        self.session_data["content"][i] = "[DEL] " + line
        self.util.write_session_data()

    
#change deteciton
#false alarm'
#true detect
#fasle alarm
# map pyannote metrics
