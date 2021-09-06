import os
from pathlib import Path

# General info about the API
API_TITLE = "DeepFire"
API_DESCRIPTION = "A REST API for detecting the presence of fire in an image."
API_VERSION = "0.0.2"

# Info about what data users can request.
# These are intended shown on the UI, related only to a specific endpoint.
API_ENDPOINTS = (
    {
        "name": "Detect Fire",
        "description": "Predicts the possibility that a color image contains fire.",
    },
)

# Tells the app how to find the config.yaml (for running ML inference)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_PATH = os.path.join(BASE_DIR, 'app', 'config.yaml')

# Wraps all the API metadata as one dictionary
API = {
    "title": API_TITLE,
    "description": API_DESCRIPTION,
    "version": API_VERSION,
    "endpoints": API_ENDPOINTS,
    "config_path": CONFIG_PATH,
}