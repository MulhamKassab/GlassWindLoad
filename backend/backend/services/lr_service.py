def calculate_lr_values(input_data, nfl_result, gtf, lsf_value):
    """
    Calculate Load Resistance (LR) for each layer and duration.

    Args:
        input_data (dict): User input including glazing type
        nfl_result (list): Interpolated or lookup NFL values (one per layer)
        gtf (dict): GTF values {'short': [...], 'long': [...]}
        lsf_value (dict or None): LSF values for double glazing, or None for single

    Returns:
        dict: {
            "short": [LR1, LR2, ...],
            "long": [LR1, LR2, ...]
        }
    """
    glazing_type = input_data.get("glazingType")

    lr_result = {
        "short": [],
        "long": []
    }

    for duration in ["short", "long"]:
        if duration not in gtf:
            continue

        gtf_vals = gtf[duration]

        if glazing_type == "double":
            lsf_vals = lsf_value[f"{duration}_duration"]

            if len(nfl_result) != 2 or len(gtf_vals) != 2 or len(lsf_vals) != 2:
                raise ValueError("Double glazing requires exactly two values for NFL, GTF, and LSF")

            lr_result[duration] = [
                round(nfl_result[0] * gtf_vals[0] * lsf_vals[0], 2),
                round(nfl_result[1] * gtf_vals[1] * lsf_vals[1], 2)
            ]
        else:
            # Single glazing — just apply GTF to each NFL
            lr_result[duration] = [round(nfl_result[i] * gtf_vals[i], 2) for i in range(len(gtf_vals))]

    return lr_result
