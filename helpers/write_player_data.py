import pandas as pd
import json
from datetime import date

def write_player_data(data, file_path):
    
    ## First save player data
    with open(file_path, 'w') as outfile:
        json.dump(data, outfile, ensure_ascii = True, indent = 4, separators=(',', ':'))