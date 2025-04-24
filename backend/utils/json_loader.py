import json
import os

def load_json_data(file_path, key=None):
    """
    Load and optionally extract a key from a JSON file.

    Args:
        file_path (str): Absolute or relative path to the JSON file.
        key (str, optional): If provided, extracts this key from the top-level JSON.

    Returns:
        dict, list, or None: Loaded JSON content, or the value at the key if provided.

    Raises:
        FileNotFoundError: If the file doesn't exist.
        ValueError: If key not found or JSON is malformed.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Error decoding JSON: {e}")

    if key:
        if key not in data:
            raise ValueError(f"Key '{key}' not found in {file_path}")
        return data[key]

    return data
