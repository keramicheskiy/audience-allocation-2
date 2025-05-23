import os
from pathlib import Path
import sqlite3
import yaml

BASE_DIR = Path(__file__).resolve().parent

MODE = os.environ.get('MODE', 'local')

with open('/config.yaml', 'r') as file:
    config = yaml.safe_load(file)

env = config[MODE][BASE_DIR.name]

TOKEN = env['telegram'].get("TG_TOKEN")
ADMINS = env['telegram'].get("ADMINS").split(' ')
BACKEND_URL = env["backend"].get("BACKEND_URL")

conn = sqlite3.connect('db.sqlite', check_same_thread=False)
cursor = conn.cursor()

