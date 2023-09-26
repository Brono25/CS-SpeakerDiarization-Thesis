import sys
from pathlib import Path
from pyannote.audio import Pipeline
import torch
from typing import Mapping
from pyannote.core import Annotation
from pyannote.database.util import load_rttm
from pathlib import Path

# Make sure to visit these URLs and accept the user conditions and create an access token
# hf.co/pyannote/speaker-diarization
# hf.co/pyannote/segmentation
# hf.co/settings/tokens

# Check if CUDA is available and set device to GPU if it is
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print('Running on device:', device)

# Instantiate pretrained speaker diarization pipeline
pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
                                    use_auth_token="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")

pipeline = pipeline.to(device)  # Move the pipeline model to GPU if available

# Get file_path from command line


if len(sys.argv) > 1:
    file_path = sys.argv[1]
    root = Path(file_path).parent
    uri = Path(file_path).stem
    rttm_file = f"{root}/ref_{uri}.rttm"
    ref_annotation = load_rttm(rttm_file)[uri]
    file: Mapping = {'audio': file_path, 'annotation': ref_annotation}

    # Apply the pipeline to an audio file
    diarization = pipeline(file)

    # Dump the diarization output to disk using RTTM format
    with open(f"/srv/scratch/z5146619/katana-sync/{uri}_pyannote.rttm", "w") as rttm:
        diarization.write_rttm(rttm)
else:
    print("Please provide the file path as a command-line argument.")