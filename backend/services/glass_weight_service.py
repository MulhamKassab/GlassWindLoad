def calculate_glass_weight(glass_length, glass_width, layers_thickness, glass_types, pvb_thicknesses=None):
    """
    Calculate the total weight of the glass, including the interlayer weight for laminated glass.

    Args:
        glass_length (float): The length of the glass in mm.
        glass_width (float): The width of the glass in mm.
        layers_thickness (list): A list of thickness values (in mm) for each glass layer.
        glass_types (list): A list of types ('mono' or 'laminated') for each layer of glass.
        pvb_thicknesses (list, optional): A list of PVB (interlayer) thicknesses for laminated glass.

    Returns:
        float: The total calculated weight of the glass (in kg), rounded to two decimal places.
    """

    GLASS_WEIGHT_MAP = {
        2.5: 5.7, 3.0: 7.6, 4.0: 9.9, 5.0: 11.9, 6.0: 14.6,
        8.0: 19.5, 10.0: 24.4, 12.0: 31.2, 16.0: 39.5, 19.0: 47.8
    }

    INTERLAYER_WEIGHT_MAP = {
        0.38: 0.40, 0.76: 0.84, 1.14: 1.20, 1.52: 1.60, 2.29: 2.50
    }

    def find_closest_value(thickness, weight_map):
        return weight_map[min(weight_map.keys(), key=lambda x: abs(x - thickness))]

    area = (glass_length / 1000) * (glass_width / 1000)
    total_weight = 0
    if pvb_thicknesses is None:
        pvb_thicknesses = []

    for i, (thickness, glass_type) in enumerate(zip(layers_thickness, glass_types)):
        weight_per_m2 = GLASS_WEIGHT_MAP.get(thickness) or find_closest_value(thickness, GLASS_WEIGHT_MAP)
        weight = weight_per_m2 * area
        total_weight += weight

        if glass_type == 'laminated' and i < len(pvb_thicknesses):
            pvb_thickness = pvb_thicknesses[i]
            interlayer_weight_per_m2 = INTERLAYER_WEIGHT_MAP.get(pvb_thickness) or find_closest_value(pvb_thickness, INTERLAYER_WEIGHT_MAP)
            interlayer_weight = interlayer_weight_per_m2 * area
            total_weight += interlayer_weight

    return round(total_weight, 2)
