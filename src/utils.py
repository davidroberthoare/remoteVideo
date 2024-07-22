import json, os

def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            data = json.load(f)
        return data
    else:
        print(f"The file {file_path} does not exist.")
        return {}

def save_json(data, path):
    sorted_data = dict(sorted(data.items()))
    try:
        with open(path, 'w') as f:
            json.dump(sorted_data, f, indent=4)
    except Exception as e:
        print(f"An error occurred while saving JSON: {e}")
