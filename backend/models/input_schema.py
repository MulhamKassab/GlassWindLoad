def validate_input(data):
    """
    Basic manual input validation.

    Args:
        data (dict): Raw JSON input from frontend

    Returns:
        tuple: (bool, str) → is_valid, error_message
    """
    required_keys = [
        "glassLength", "glassWidth", "shortDurationLoad", "allowable_Deflection",
        "layersTypes", "layersThicknesses", "glassLayersStrengthType",
        "numberOfSupportedSides", "glazingType"
    ]

    for key in required_keys:
        if key not in data:
            return False, f"Missing required field: {key}"

    if not isinstance(data["glassLength"], (int, float)) or data["glassLength"] <= 0:
        return False, "glassLength must be a positive number."

    if data["numberOfSupportedSides"] not in [1, 2, 4]:
        return False, "numberOfSupportedSides must be 1, 2, or 4."

    return True, ""
