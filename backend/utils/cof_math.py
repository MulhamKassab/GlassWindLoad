import os
import math
import json
from config import DATA_DIR

def load_thickness_spec():
    """
    Load nominal and minimum thickness mapping from JSON.
    """
    path = os.path.join(DATA_DIR, "Glass_Thicknesses.json")
    if not os.path.exists(path):
        raise FileNotFoundError(f"Glass thickness data not found at: {path}")
    
    with open(path, "r") as f:
        data = json.load(f)
    
    return data["Glass_Thicknesses"]

def get_minimum_thickness(nominal_thickness, spec_data):
    """
    Match the minimum thickness for a given nominal value.
    """
    for item in spec_data:
        if float(item["Nominal_mm"]) == float(nominal_thickness):
            return float(item["Minimum_mm"])
    raise ValueError(f"No matching minimum thickness for nominal value: {nominal_thickness}")

def calculate_coefficients(length, width):
    """
    Calculate r0, r1, r2 based on L/W ratio.
    """
    ratio = length / width
    r0 = 0.553 - 3.83 * ratio + 1.11 * ratio**2 - 0.0969 * ratio**3
    r1 = -2.29 + 5.83 * ratio - 2.17 * ratio**2 + 0.2067 * ratio**3
    r2 = 1.485 - 1.908 * ratio + 0.815 * ratio**2 - 0.0822 * ratio**3
    return r0, r1, r2

def calculate_x(load, length, width, E, min_thickness):
    """
    Calculate X used in the COF equation.
    """
    return math.log(math.log((load * (length * width)**2) / (E * min_thickness**4)))

def calculate_cof(load, length, width, E, nominal_thickness):
    """
    Final COF value using ASTM E1300 formula.
    """
    spec_data = load_thickness_spec()
    min_thickness = get_minimum_thickness(nominal_thickness, spec_data)
    r0, r1, r2 = calculate_coefficients(length, width)
    x = calculate_x(load, length, width, E, min_thickness)
    return min_thickness * math.exp(r0 + r1 * x + r2 * x**2)
