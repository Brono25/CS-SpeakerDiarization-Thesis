
import json


with open("database.json", 'r') as f:
    data = json.load(f)



def update_structure(data, template):
    for main_key in data.keys():
        for key, value in template.items():
            if key not in data[main_key]:
                data[main_key][key] = None
            elif isinstance(value, dict):
                for sub_key in value.keys():
                    if sub_key not in data[main_key][key]:
                        data[main_key][key][sub_key] = None


template = {
    "primary_language": None,
    "comment": None,
    "category": None,
    "speakers": {
        "JES": None,
        "NIC": None,
    },
    "duration_sec": None,
    "coverage": None,
    "cs_metrics": {
        "i-index": None,
        "m-index": None,
        "burstiness": None,
        "change-point-freq": None,
        "speaker-change-freq": None,
    },
    "pyannote": {
        "diarization": {
            "der_pc": None,
            "confusion_sec": None,
            "missed_sec": None,
            "false_sec": None,
        },
        "error_rates": {
            "english_conf_error_rate": None,
            "spanish_conf_error_rate": None,
            "english_miss_error_rate": None,
            "spanish_miss_error_rate": None,
            "english_error_rate": None,
            "spanish_error_rate": None,
        },
    }
}


update_structure(data, template)

# Save the updated data back to the JSON file
with open("database.json", "w") as f:
    json.dump(data, f, indent=4)