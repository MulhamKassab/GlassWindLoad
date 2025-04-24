import os
from config import DATA_DIR, DOWNLOAD_DIR
from utils.interpolation import interpolate_nfl_griddata
from utils.json_loader import load_json_data
from utils.plotting import plot_nfl_from_json  # You can refactor this into utils later

def calculate_interpolated_nfl(input_data, thickness, layer_type, index):
    """
    Calculates NFL using grid interpolation for 4-sided supported glass.
    Also generates plot using plotting function.
    """
    length = input_data.get("glassLength")
    width = input_data.get("glassWidth")
    sides = input_data.get("numberOfSupportedSides")

    key = f"NFL{thickness}mm{sides}S"
    json_file_path = os.path.join(DATA_DIR, "NFL", layer_type, f"{sides}Sided", f"{key}.json")

    # Load data from the corresponding JSON
    data_list = load_json_data(json_file_path, key)

    if width > length:
        width, length = length, width  # Normalize

    AR = length / width

    # Prepare for interpolation
    jsonNFL = [d["NFL"] for d in data_list]
    jsonX = [d["X"] for d in data_list]
    jsonY = [d["Y"] for d in data_list]

    interpolated_nfl, _, _, _ = interpolate_nfl_griddata(length, width, AR, jsonX, jsonY, jsonNFL)

    if interpolated_nfl is None or interpolated_nfl == 0:
        raise ValueError(f"Could not interpolate NFL for thickness {thickness}mm")

    # Generate Plot
    save_path = os.path.join(DOWNLOAD_DIR, f"nfl_plot_{thickness}")
    final_nfl, plot_paths = plot_nfl_from_json(
        length, width, sides, thickness, save_path,
        [interpolated_nfl], layer_type, index
    )

    return round(final_nfl, 2), plot_paths
