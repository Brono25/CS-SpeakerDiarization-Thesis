import whisper
import os
import json

uri = "sastre09_1"
curr_dir = os.path.realpath(__file__)
root_dir = curr_dir[: curr_dir.index("katana") + len("katana")]
error_dir = f"{root_dir}/tools/metrics/error_rttm"
audio_file_path = f"{root_dir}/wav/{uri}.wav"
output_file = "whisper-result.json"

def run_transcribe(model):
    result = model.transcribe(audio_file_path)
    with open(output_file, 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=4)

def load_transcription(filename=output_file):
    with open(filename, 'r') as f:
        result = json.load(f)
    return result


model = whisper.load_model("base")

#run_transcribe(model) #not needed for below
data = load_transcription()

transcription = []
segments = data.get('segments', [])
for segment in segments:
    start = segment.get('start')
    end = segment.get('end')
    text = segment.get('text')
    transcription.append(f'AAA {text} {int(start * 1000)}_{int(end * 1000)}\n')


with open("whisper-transcription.txt", 'w') as f:
    for line in transcription:
        f.write(line)