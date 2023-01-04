import json
import os

file_dir = os.path.dirname(os.path.realpath('__file__'))

# EXTRACT JSON DATA
with open('connection_info.json') as file:
    CONFIG = json.load(file)