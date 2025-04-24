import os

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Path to the data folder (replaces ./Json)
DATA_DIR = os.path.join(BASE_DIR, "data")

# Path to download folder (for PDFs and images)
DOWNLOAD_DIR = os.path.join(BASE_DIR, "download")

# Elasticity constant (used in deflection calculations)
MODULUS_OF_ELASTICITY = 71700000  # N/m² or Pa

# Logging (optional: for future enhancements)
LOGGING_LEVEL = "DEBUG"
