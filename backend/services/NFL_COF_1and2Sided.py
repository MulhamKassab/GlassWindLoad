import os
import json
import math
from config import DATA_DIR

def load_json_file(layer_type, supported_sides, nfl_or_cof, interlayer_types):
    """
    Load the appropriate JSON file based on the parameters.

    Args:
        layer_type (str): 'mono' or 'laminated'
        supported_sides (str): '1' or '2'
        nfl_or_cof (str): 'NFL' or 'COF'
        interlayer_types (list): e.g., ['PVB'] or ['SGP']

    Returns:
        dict or str: Parsed data or error message
    """
    interlayer_suffix = f"_{interlayer_types[0]}" if nfl_or_cof == "COF" else ""
    file_name = f"{nfl_or_cof}_{supported_sides}_{layer_type}{interlayer_suffix}.json"

    file_path = os.path.join(DATA_DIR, nfl_or_cof, layer_type, file_name)
    
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)

        top_level_key = os.path.splitext(file_name)[0]  # Remove `.json`
        return data.get(top_level_key, f"Top-level key '{top_level_key}' not found in JSON.")

    except FileNotFoundError:
        return f"File not found: {file_path}"
    except json.JSONDecodeError:
        return f"Error decoding JSON in file: {file_path}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"

def find_load_for_given_length(thickness, length, layer_type, supported_sides, nfl_or_cof, load, interlayerTypes):
    """
    Perform load interpolation for NFL or COF based on 1 or 2 supported sides.

    Args:
        thickness (float): Glass thickness in mm
        length (float): Glass length in mm
        layer_type (str): 'mono' or 'laminated'
        supported_sides (str): '1' or '2'
        nfl_or_cof (str): 'NFL' or 'COF'
        load (float): Applied load (only needed for COF)
        interlayerTypes (list): Interlayer type like ['PVB']

    Returns:
        float or str: Result or error
    """
    # Cap thickness to max supported value
    if thickness > 19:
        thickness = 19

    points_dict = load_json_file(layer_type, supported_sides, nfl_or_cof, interlayerTypes)
    if isinstance(points_dict, str):  # It's an error message
        return points_dict

    points = points_dict.get(str(thickness))
    if not points or len(points) != 2:
        return "Invalid data or number of interpolation points."

    (x1, y1), (x2, y2) = points

    try:
        if nfl_or_cof == "NFL":
            if y1 == y2:
                return "Length values y1 and y2 cannot be the same."
            x = x1 * (x2 / x1) ** (math.log(length / y1) / math.log(y2 / y1))
            return round(x, 5)

        elif nfl_or_cof == "COF":
            length_m = length / 1000
            load_l4 = length_m**4 * load
            log_x1, log_x2 = math.log10(x1), math.log10(x2)
            log_y1, log_y2 = math.log10(y1), math.log10(y2)
            log_load_l4 = math.log10(load_l4)
            log_y = log_y1 + ((log_load_l4 - log_x1) / (log_x2 - log_x1)) * (log_y2 - log_y1)
            return round(10 ** log_y, 5)

        return "Invalid calculation type."

    except ValueError as e:
        return f"Math error: {str(e)}"
