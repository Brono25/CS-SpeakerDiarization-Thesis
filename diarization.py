
import sys
from pathlib import Path
from pyannote.audio import Pipeline
import torch
# Make sure to visit these URLs and accept the user conditions and create an access token
# hf.co/pyannote/speaker-diarization
# hf.co/pyannote/segmentation
# hf.co/settings/tokens


print('MPS Available:',torch.backends.mps.is_available())
print('MPS Built:',torch.backends.mps.is_built())


# Instantiate pretrained speaker diarization pipeline

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                    use_auth_token="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")
#pipeline.to("mps")  # Use "mps" for Apple M1 GPU

# Get file_path from command line
if len(sys.argv) > 1:
    file_path = sys.argv[1]
    file_name = Path(file_path).stem

    # Apply the pipeline to an audio file
    diarization = pipeline(file_path)

    # Dump the diarization output to disk using RTTM format
    with open(f"{file_name}_output.rttm", "w") as rttm:
        diarization.write_rttm(rttm)
else:
    print("Please provide the file path as a command-line argument.")
