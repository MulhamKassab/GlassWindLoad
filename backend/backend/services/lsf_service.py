import os
import json
from config import DATA_DIR

def get_lsf_values(input_data):
    """
    Fetch Load Share Factor (LSF) values for short and long duration for double-glazed units.

    Args:
        input_data (dict): Must contain 'layersThicknesses' and 'layersTypes'

    Returns:
        dict: {
            "short_duration": [LS1, LS2],
            "long_duration": [LS1, LS2]
        }
    """
    thicknesses = input_data.get("layersThicknesses", [])
    layer_types = input_data.get("layersTypes", [])

    if len(thicknesses) != 2 or len(layer_types) != 2:
        raise ValueError("LSF calculation requires exactly two layers")

    t1, t2 = str(thicknesses[0]), str(thicknesses[1])
    types = layer_types

    # Determine which file(s) to use
    if types == ['mono', 'lami']:
        short_file = os.path.join(DATA_DIR, "LSF", "LSF_DI.json")
        long_file = os.path.join(DATA_DIR, "LSF", "LSF_LongOnly.json")
    else:
        short_file = long_file = os.path.join(DATA_DIR, "LSF", "LSF_DI.json")

    def load_lsf_from_file(path):
        with open(path, 'r') as f:
            data = json.load(f)
        try:
            values = data["Load_Share_Factors"][t1][t2]
            return [values["LS1"], values["LS2"]]
        except KeyError:
            raise ValueError(f"LSF values not found for thickness pair {t1} & {t2}")

    return {
        "short_duration": load_lsf_from_file(short_file),
        "long_duration": load_lsf_from_file(long_file)
    }
