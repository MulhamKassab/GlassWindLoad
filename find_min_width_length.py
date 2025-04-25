import math

def find_min_width_or_length(load, fixed_side, modulus_of_elasticity, thickness, vary='length'):
    """
    Calculate the minimum required length or width to avoid math domain error in COF.

    Parameters:
    - load: Applied load (kPa)
    - fixed_side: The known width or length (mm)
    - modulus_of_elasticity: Typically 71700000 (Pa)
    - thickness: Glass thickness (mm)
    - vary: 'length' if width is fixed, 'width' if length is fixed

    Returns:
    - float: Minimum length or width (mm) required
    - None: If invalid input
    """
    if load <= 0 or modulus_of_elasticity <= 0 or thickness <= 0 or fixed_side <= 0:
        return None

    try:
        # Use formula: A > sqrt(e * E * t^4 / load)
        threshold = math.e  # ≈ 2.718
        thickness_m = thickness / 1000  # convert mm to meters
        required_area_m2 = math.sqrt(threshold * modulus_of_elasticity * thickness_m ** 4 / (load * 1000))
        required_side_m = required_area_m2 / (fixed_side / 1000)  # divide by fixed side in meters
        return round(required_side_m * 1000, 2)  # return in mm
    except:
        return None
