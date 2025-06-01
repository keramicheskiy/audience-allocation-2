import os
from pathlib import Path
import yaml

BASE_DIR = Path(__file__).resolve().parent

config_file = os.environ.get('CONFIG_FILE')

with open(config_file, 'r') as file:
    config = yaml.safe_load(file)

BACKEND_URL = config["tests"]['backend'].get('URL', "http://backend:8080")

ADMIN_EMAIL = config["admin"].get("EMAIL")
ADMIN_PASSWORD = config["admin"].get("PASSWORD")
