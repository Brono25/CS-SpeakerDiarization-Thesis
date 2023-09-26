from pyannote.audio import Model
from pyannote.audio import Inference
from pyannote.audio.pipelines.utils.getter import get_model


ACCESS_TOKEN = "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"
MODEL = "speechbrain/spkrec-ecapa-voxceleb"


model = get_model(MODEL, use_auth_token=ACCESS_TOKEN)

