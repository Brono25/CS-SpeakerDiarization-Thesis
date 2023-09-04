
import json

DATA = "/Users/brono/GitHub/CS-SpeakerDiarization-Thesis/src/data/database.json"


with open(DATA, 'r') as f:
    data = json.load(f)



total_cs_sec = 0
total_spa_sec = 0
total_eng_sec = 0

total_cs = 0
total_eng = 0
total_spa = 0

total_tracks = 0

for k, v in data.items():

    total_tracks += 1

    if data[k]["category"] == "code-switching":
        total_cs_sec += data[k]["duration_sec"]
        total_cs += 1
        
    if data[k]["category"] == "english":
        total_eng_sec += data[k]["duration_sec"]
        total_eng += 1

    if data[k]["category"] == "spanish":
        total_spa_sec += data[k]["duration_sec"]
        total_spa += 1

def sec_to_min_sec(seconds):
    minutes, sec = divmod(seconds, 60)
    return f"{minutes} min {sec} sec"

print(f"Total Tracks: {total_tracks}")
print(f"Tracks Done: {total_cs + total_eng + total_spa}/{total_tracks} ({sec_to_min_sec(total_cs_sec + total_eng_sec + total_spa_sec)})")
print("---")
print(f"Code-Switching Tracks Done: {total_cs}(Duration: {sec_to_min_sec(total_cs_sec)})")
print(f"English Tracks Done: {total_eng}(Duration: {sec_to_min_sec(total_eng_sec)})")
print(f"Spanish Tracks Done: {total_spa}(Duration: {sec_to_min_sec(total_spa_sec)})")
