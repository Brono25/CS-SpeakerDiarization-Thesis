from transcript_player import TranscriptPlayer
import tkinter as tk
import os



def main():
    root = tk.Tk()
    TranscriptPlayer(root)
    root.mainloop()

if __name__ == "__main__":
    current_script_path = os.path.abspath(__file__)
    script_dir = os.path.dirname(current_script_path)
    tools_dir = os.path.dirname(script_dir)
    root_dir = os.path.dirname(tools_dir)
    os.chdir(root_dir)
    main()
