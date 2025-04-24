from services.NFL_COF_1and2Sided import find_load_for_given_length

def find_lookup_nfl(input_data, thickness, layer_type):
    """
    Retrieves the NFL value for 1 or 2 supported sides using predefined JSON lookup tables.

    Args:
        input_data (dict): Full user input data.
        thickness (float): Glass layer thickness in mm.
        layer_type (str): 'mono' or 'laminated'.

    Returns:
        float: Interpolated NFL value.
    """
    length = input_data.get("glassLength")
    supported_sides = str(input_data.get("numberOfSupportedSides"))  # '1' or '2'
    interlayer_types = input_data.get("interlayerTypes", [])

    nfl_value = find_load_for_given_length(
        thickness=thickness,
        length=length,
        layer_type=layer_type,
        supported_sides=supported_sides,
        nfl_or_cof="NFL",
        load=0,  # not used for NFL
        interlayerTypes=interlayer_types
    )

    if isinstance(nfl_value, str):
        raise ValueError(f"NFL lookup failed: {nfl_value}")

    return round(float(nfl_value), 2)
