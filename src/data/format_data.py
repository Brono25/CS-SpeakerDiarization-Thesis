
import json

database_path = "src/data/database.json"
with open(database_path, 'r') as f:
    data = json.load(f)



def update_structure(data, template):
    for main_key in data.keys():
        new_data = {}
        for key, value in template.items():
            if key == "speakers":
                # Get existing speaker labels or create an empty dictionary
                existing_speakers = data[main_key].get(key, {})
                # Initialize with template if needed
                new_speakers = template[key].copy()
                # Update with existing values
                new_speakers.update(existing_speakers)
                new_data[key] = new_speakers
                continue

            if key in data[main_key]:
                new_data[key] = data[main_key][key]
            else:
                new_data[key] = None

            if isinstance(value, dict):
                if new_data[key] is None:
                    new_data[key] = {}
                for sub_key in value.keys():
                    if key in data[main_key] and sub_key in data[main_key][key]:
                        new_data[key][sub_key] = data[main_key][key][sub_key]
                    else:
                        new_data[key][sub_key] = None

        data[main_key] = new_data





template = {
    "category": None,
    "perceived_similarity_score": None,
    "duration_sec": None,
    "coverage": None,
    "speakers": {},
        "cs_metrics": {
        "i-index": None,
        "m-index": None,
        "burstiness": None,
        "change-point-freq": None,
        "speaker-change-freq": None,
    },
    "primary_language": None,
    "comment": None,

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
with open(database_path, "w") as f:
    json.dump(data, f, indent=4)