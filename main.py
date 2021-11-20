import asyncio
import argparse
from helpers.get_player_data import get_player_data
from helpers.get_spi_data import get_spi_data
from helpers.clean_player_data import clean_player_data
from helpers.select_squad import select_squad
from helpers.transfer_optimization import transfer_optimization
from datetime import date

def main(analysis, season, budget, free_transfers):

    ## Get SPI Match data (local or remote)
    # spi_data = get_spi_data()

    ## Get player data (local or remote)
    players = asyncio.get_event_loop().run_until_complete(get_player_data())

    ## Clean player data
    players = clean_player_data(players)

    if analysis == 'selection':

        ## Process player data and run solver
        select_squad(players, season)
    
    elif analysis == 'transfer' or analysis == 'multitransfer':

        ## Check for budget variable type
        if budget is not None and isinstance(budget, str):
            budget = float(budget)

        ## Check for free_transfers variable
        if free_transfers is not None and isinstance(free_transfers, str):
            free_transfers = float(free_transfers)
        
        ## Run a transfer optimization analysis
        transfer_optimization(analysis, budget, free_transfers)


if __name__ == "__main__":
    
    ## Parse arguments provided in terminal
    parser = argparse.ArgumentParser(description = 'Create a request to DataForSEO APIs')
    
    ## Parse endpoint argument
    parser.add_argument('--analysis', metavar = 'path', required = True, help = 'Whether to run selection analysis from scratch or a transfer analysis given an existing team')

    ## Add argument to control whether to use previous season's total_points or current season's form as the expected_scores value
    parser.add_argument('--season', metavar = 'path', required = False, help = 'Whether to run selection analysis on previous season total points or current season form')

    ## Add argument to control whether to use previous season's total_points or current season's form as the expected_scores value
    parser.add_argument('--budget', metavar = 'path', required = False, help = 'Current budget leftover by a current squad selection')

    ## Add argument to control for the number of free transfers available at the time of analysis
    parser.add_argument('--free_transfers', metavar = 'path', required = False, help = 'Current number of free transfers available')

    ## Parse arguments and input into main()
    args = parser.parse_args()
    main(analysis = args.analysis, season = args.season, budget = args.budget, free_transfers = args.free_transfers)