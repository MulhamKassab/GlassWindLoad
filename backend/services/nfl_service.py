from services.new_style_nfl_interpolation import calculate_interpolated_nfl
from services.old_style_nfl_lookup import find_lookup_nfl

def calculate_nfl_for_supported_sides(input_data):
    """
    Dispatch NFL calculation based on the number of supported sides.
    For 4 sides, we use interpolation. For 1 or 2, we use lookup.
    """

    supported_sides = input_data.get("numberOfSupportedSides")
    glazing_type = input_data.get("glazingType")
    layer_types = input_data.get("layersTypes")
    layer_thicknesses = input_data.get("layersThicknesses")

    if supported_sides == 4:
        interpolated_nfls = []
        plots = []

        for i, thickness in enumerate(layer_thicknesses):
            result, plot_paths = calculate_interpolated_nfl(
                input_data=input_data,
                thickness=thickness,
                layer_type=layer_types[i],
                index=i
            )
            interpolated_nfls.append(result)
            plots.append(plot_paths)

        return interpolated_nfls, plots

    else:
        # For 1 or 2 sided support
        lookup_nfls = []
        for i, thickness in enumerate(layer_thicknesses):
            result = find_lookup_nfl(
                input_data=input_data,
                thickness=thickness,
                layer_type=layer_types[i]
            )
            lookup_nfls.append(result)

        return lookup_nfls, []  # no plot paths
