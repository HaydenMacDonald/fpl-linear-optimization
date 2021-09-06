from helpers.process_player_data import process_player_data
import os
import asyncio
import argparse
from helpers.get_player_data import get_player_data
from helpers.write_player_data import write_player_data
from helpers.clean_player_data import clean_player_data
from helpers.process_player_data import process_player_data
from helpers.transfer_optimization import transfer_optimization
from datetime import date

def main(analysis, season):

    if analysis == 'selection':
        ## Target data file
        data_file = f'.\data\json\players-{date.today()}.json'

        ## If data doesn't exist, get it
        if not os.path.isfile(data_file):
            players = asyncio.get_event_loop().run_until_complete(get_player_data(include_summary=True, return_json=True))
            write_player_data(players, f'.\data\json\players-{date.today()}.json')

        ## Clean data
        players = clean_player_data(data_file)

        ## Process player data and run solver
        process_player_data(players, season)
    
    elif analysis == 'transfer' or analysis == 'multitransfer':
        
        ## Current team selection
        current_team = f'.\data\json\selections\selection-{date.today()}.json'

        ## Player data
        data_file = f'.\data\json\players-{date.today()}.json';

        if not os.path.isfile(current_team) or not os.path.isfile(data_file):
            raise ValueError('Team data file not found')
        
        transfers = transfer_optimization(current_team, data_file, analysis)


if __name__ == "__main__":
    
    ## Parse arguments provided in terminal
    parser = argparse.ArgumentParser(description = 'Create a request to DataForSEO APIs')
    
    ## Parse endpoint argument
    parser.add_argument('--analysis', metavar = 'path', required = True, help = 'Whether to run selection analysis from scratch or a transfer analysis given an existing team')

    ## Add argument to control whether to use previous season's total_points or current season's form as the expected_scores value
    parser.add_argument('--season', metavar = 'path', required = False, help = 'Whether to run selection analysis on previous season total points or current season form')

    ## Parse arguments and input into main()
    args = parser.parse_args()
    main(analysis = args.analysis, season = args.season)