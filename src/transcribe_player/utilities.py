
import shutil
import os
import json
import re
import glob

class Utilities:
    def __init__(self, session_data):
        self.save_file = "./tools/transcribePlayer/.session_save.json"
        self.session_data = session_data
        self.create_savefile()
        


    def load_savefile(self):
        data = None
        with open(self.save_file, 'r') as f:        
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                print("Error: JSON decoding failed")
        return data

    def write_session_data(self):
        with open(self.save_file, 'w') as f:
            json.dump(self.session_data, f, indent=4)

    def load_content(self, filename):
        with open(filename, 'r') as f:
            content = f.readlines()
        return content
    
    def update_content_timestamp(self):
        i = self.session_data["curr_index"]
        start = self.session_data["curr_start"]
        end = self.session_data["curr_end"]
        timestamp = f"{start}_{end}"
        content = self.session_data["content"]
        if content:
            content[i] = re.sub(r"\d+_\d+", timestamp, content[i])
   

    def create_savefile(self):
        expected_keys = {"filename", 
                        "audio_file", 
                        "id", 
                        "curr_index", 
                        "curr_start", 
                        "curr_end", 
                        "content"}

        if not os.path.exists(self.save_file):
            self.session_data.update({
                "filename": None,
                "audio_file": None,
                "id": None,
                "curr_index": None,
                "curr_start": None,
                "curr_end": None,
                "content": None
            })
            self.write_session_data()
        else:
            with open(self.save_file, 'r') as file:
                try:
                    data = json.load(file)
                    if not expected_keys.issubset(data.keys()):  
                        raise ValueError("JSON file does not contain all the expected keys.")
                    else:
                        self.session_data.update(data)
                except (json.JSONDecodeError, ValueError):
                    print("Error: Invalid JSON file.")
                    self.session_data.update({
                        "filename": None,
                        "audio_file": None,
                        "id": None,
                        "curr_index": None,
                        "curr_start": None,
                        "curr_end": None,
                        "content": None
                    })
                    self.write_session_data()

    def write_content(self):
        # Create a hidden folder if it doesn't exist
        if not os.path.exists(".backups"):
            os.mkdir(".backups")
            
        # Get the filename and extension
        filename, file_extension = os.path.splitext(self.session_data["filename"])
        filename = os.path.basename(filename)
        
        # Find the next available backup number
        existing_backups = glob.glob(os.path.join(".backups", f"{filename}_*{file_extension}"))
        backup_nums = [int(os.path.splitext(os.path.basename(b))[0].split('_')[-1]) for b in existing_backups]
        if backup_nums:
            next_backup_num = max(backup_nums) + 1
        else:
            next_backup_num = 0
        
        # Create the backup file path
        backup_file = os.path.join(".backups", f"{filename}_{next_backup_num}{file_extension}")
        
        # Copy the file to the .backups directory
        shutil.copy2(self.session_data["filename"], backup_file)
        
        # Overwrite the original file with new content
        with open(self.session_data["filename"], 'w') as f:
            f.write(''.join(self.session_data["content"]))  

          