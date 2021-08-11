from helpers.process_player_data import process_player_data
import os
import asyncio
from helpers.get_player_data import get_player_data
from helpers.write_player_data import write_player_data
from helpers.clean_player_data import clean_player_data
from helpers.process_player_data import process_player_data
from datetime import date

def main():

    ## Target data file
    data_file = f'.\data\json\players-{date.today()}.json'

    ## If data doesn't exist, get it
    if os.path.isfile(data_file):
        players = asyncio.get_event_loop().run_until_complete(get_player_data(include_summary=True, return_json=True))
        write_player_data(players, f'.\data\json\players-{date.today()}.json')

    ## Clean data
    players = clean_player_data(data_file)
    process_player_data(players)

if __name__ == "__main__":
    main()