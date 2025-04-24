import os
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from scipy.spatial import cKDTree
import json
from config import DATA_DIR

plt.switch_backend('Agg')  # For headless environments (no GUI)

# === Helper: Load and validate JSON data ===
def load_nfl_json(file_path, key):
    with open(file_path, 'r') as f:
        data = json.load(f)
    if key not in data:
        raise ValueError(f"Key '{key}' not found in JSON: {file_path}")
    return data[key]

# === Helper: Group points by NFL value ===
def group_points_by_nfl(data_list):
    grouped = defaultdict(list)
    for item in data_list:
        grouped[item["NFL"]].append((item["X"], item["Y"]))
    return grouped

# === Helper: Basic Catmull-Rom spline ===
def catmull_rom_spline(P0, P1, P2, P3, n_points=100):
    alpha = 0.5
    def tj(ti, Pi, Pj): return (np.linalg.norm(Pj - Pi))**alpha + ti
    t0 = 0
    t1, t2, t3 = tj(t0, P0, P1), tj(t0, P0, P1) + tj(t0, P1, P2), tj(t0, P0, P1) + tj(t0, P1, P2) + tj(t0, P2, P3)
    t = np.linspace(t1, t2, n_points)
    A1 = (t1 - t)[:, None] * P0 + (t - t0)[:, None] * P1
    A1 /= (t1 - t0)
    A2 = (t2 - t)[:, None] * P1 + (t - t1)[:, None] * P2
    A2 /= (t2 - t1)
    A3 = (t3 - t)[:, None] * P2 + (t - t2)[:, None] * P3
    A3 /= (t3 - t2)
    B1 = (t2 - t)[:, None] * A1 + (t - t0)[:, None] * A2
    B1 /= (t2 - t0)
    B2 = (t3 - t)[:, None] * A2 + (t - t1)[:, None] * A3
    B2 /= (t3 - t1)
    C = (t2 - t)[:, None] * B1 + (t - t1)[:, None] * B2
    C /= (t2 - t1)
    return C

# === Helper: Interpolate via inverse distance weighting ===
def inverse_distance_weighting(x, y, points):
    weights = []
    epsilon = 1e-10
    for pt in points:
        dist = np.sqrt((pt['X'] - x)**2 + (pt['Y'] - y)**2) + epsilon
        if dist == 0:
            return pt['NFL']
        weights.append(1 / dist)
    return float(sum(p['NFL'] * w for p, w in zip(points, weights)) / sum(weights))

# === Main Plot Function ===
def plot_nfl_from_json(length, width, supported_sides, thickness, save_path, calculated_nfls, layer_type, index):
    """
    Generates NFL curves and saves plot to disk.
    Returns (interpolated_nfl: float, [plot_image_path])
    """
    key = f"NFL{thickness}mm{supported_sides}S"
    json_file_path = os.path.join("DATA_DIR", "NFL", layer_type, f"{supported_sides}Sided", f"{key}.json")
    data_list = load_nfl_json(json_file_path, key)
    grouped_points = group_points_by_nfl(data_list)

    fig, ax = plt.subplots()

    # Plot each NFL curve
    for nfl, pts in grouped_points.items():
        coords = np.array(pts)
        if len(coords) >= 4:
            coords = np.vstack([coords[0], coords[0], coords, coords[-1], coords[-1]])
            curve = []
            for i in range(1, len(coords) - 2):
                P0, P1, P2, P3 = coords[i - 1], coords[i], coords[i + 1], coords[i + 2]
                curve.extend(catmull_rom_spline(P0, P1, P2, P3))
            curve = np.array(curve)
            ax.plot(curve[:, 0], curve[:, 1], label=f'NFL {nfl}')
        else:
            ax.plot(coords[:, 0], coords[:, 1], label=f'NFL {nfl}')

    # Add aspect ratio line and target point
    ax.plot([0, length * 1.2], [0, width * 1.2], 'g--')
    ax.scatter([length], [width], color='black', label='Input Point')

    ax.set_title(f'NFL Interpolation Plot ({thickness} mm, {supported_sides}-sided)')
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    ax.legend()

    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    image_path = f"{save_path}_plot_{index + 1}.png"
    plt.savefig(image_path)
    plt.close()

    # Compute weighted NFL based on closest points (for extra validation)
    points = [{"X": p["X"], "Y": p["Y"], "NFL": p["NFL"]} for p in data_list]
    tree = cKDTree([(p["X"], p["Y"]) for p in data_list])
    _, idxs = tree.query([[length, width]], k=4)
    close_points = [points[i] for i in idxs[0]]
    weighted_nfl = inverse_distance_weighting(length, width, close_points)

    return round(weighted_nfl, 2), [image_path]
