import aiohttp
from fpl import FPL
from datetime import date
import os
import json
from helpers.write_player_data import write_player_data

async def get_player_data(include_summary=True, return_json=True):

    ## Target data file
    data_file = f'.\data\json\players-{date.today()}.json'

    ## If data doesn't exist, get it
    if not os.path.isfile(data_file):
        
        async with aiohttp.ClientSession() as session:
            ## Instantiate session
            fpl = FPL(session)

            ## Fetch player data with async request
            players = await fpl.get_players(include_summary=include_summary, return_json=return_json)

            ## Write player data as json file
            write_player_data(players, data_file)
    
    ## Otherwise, access local copy
    else:
        with open(data_file) as json_file:
            players = json.load(json_file)
    
    return players