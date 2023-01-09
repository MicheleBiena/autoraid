import json
import os

file_dir = os.path.dirname(os.path.realpath("__file__"))
config = {}

# EXTRACT JSON DATA
config_file = "Autoraid.Windows\\config.json"
if os.path.exists(config_file):
    with open(config_file) as file:
        config = json.load(file)
