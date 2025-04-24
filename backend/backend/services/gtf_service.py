import os
import json
from config import DATA_DIR

def get_gtf_values(input_data):
    """
    Retrieve GTF values (Glass Type Factor) for each layer based on strength and glazing type.

    Args:
        input_data (dict): The user input including 'glassLayersStrengthType' and 'glazingType'

    Returns:
        dict: {
            "short": [GTF1, GTF2, ...],
            "long": [GTF1, GTF2, ...]
        }
    """
    glazing_type = input_data.get("glazingType")
    strength_types = input_data.get("glassLayersStrengthType", [])

    gtf_result = {
        "short": [],
        "long": []
    }

    if glazing_type == "single":
        json_path = os.path.join(DATA_DIR, "GTF", "GTF_SL.json")
        with open(json_path, 'r') as f:
            data = json.load(f)
            short_data = data["GTF_Single_Lite"]["short"]
            long_data = data["GTF_Single_Lite"]["long"]

        for strength in strength_types:
            if strength not in short_data or strength not in long_data:
                raise ValueError(f"GTF type not found: {strength}")
            gtf_result["short"].append(short_data[strength])
            gtf_result["long"].append(long_data[strength])

    elif glazing_type == "double":
        if len(strength_types) != 2:
            raise ValueError("Double glazing requires exactly two strength types")

        lite1, lite2 = strength_types
        short_path = os.path.join(DATA_DIR, "GTF", "GTF_IG_SD.json")
        long_path = os.path.join(DATA_DIR, "GTF", "GTF_IG_LD.json")

        with open(short_path, 'r') as f1, open(long_path, 'r') as f2:
            short_data = json.load(f1)["GTF"]
            long_data = json.load(f2)["GTF"]

        try:
            gtf_result["short"].append(short_data[lite1][lite2]["GTF1"])
            gtf_result["short"].append(short_data[lite1][lite2]["GTF2"])
            gtf_result["long"].append(long_data[lite1][lite2]["GTF1"])
            gtf_result["long"].append(long_data[lite1][lite2]["GTF2"])
        except KeyError:
            raise ValueError(f"Invalid strength pair: {lite1}, {lite2}")

    else:
        raise ValueError(f"Invalid glazing type: {glazing_type}")

    return gtf_result
