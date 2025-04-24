from services.old_style_nfl_lookup import find_lookup_nfl
from utils.cof_math import calculate_cof
from config import MODULUS_OF_ELASTICITY

def calculate_cof_values(input_data):
    """
    Calculates center of glass deflection (COF) for each layer.

    Handles both short and long duration if applicable.
    
    Returns:
        tuple: (short_cof_list, long_cof_list)
    """
    supported_sides = input_data.get("numberOfSupportedSides")
    short_load = input_data.get("shortDurationLoad", 0)
    long_load = input_data.get("longDurationLoad", 0)
    length = input_data.get("glassLength")
    width = input_data.get("glassWidth")
    types = input_data.get("layersTypes", [])
    thicknesses = input_data.get("layersThicknesses", [])

    short_results = []
    long_results = []

    for i, (layer_type, thickness) in enumerate(zip(types, thicknesses)):
        if supported_sides == 4:
            # Use equation-based deflection model
            try:
                short_val = calculate_cof(short_load, length, width, MODULUS_OF_ELASTICITY, thickness)
                short_results.append(round(short_val, 2))
                if long_load > 0:
                    long_val = calculate_cof(long_load, length, width, MODULUS_OF_ELASTICITY, thickness)
                    long_results.append(round(long_val, 2))
            except Exception as e:
                raise ValueError(f"COF calculation error for layer {i}: {e}")
        else:
            # Use JSON lookup-based model
            interlayer_types = input_data.get("interlayerTypes", [])
            short_val = find_lookup_nfl(
                input_data=input_data,
                thickness=thickness,
                layer_type=layer_type,
                nfl_or_cof="COF",
                load=short_load
            )
            short_results.append(round(short_val, 2) if not isinstance(short_val, str) else 0)

            if long_load > 0:
                long_val = find_lookup_nfl(
                    input_data=input_data,
                    thickness=thickness,
                    layer_type=layer_type,
                    nfl_or_cof="COF",
                    load=long_load
                )
                long_results.append(round(long_val, 2) if not isinstance(long_val, str) else 0)

    return short_results, long_results
