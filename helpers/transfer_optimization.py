import pandas as pd
import numpy as np
from datetime import date
import os
import glob
import json
from helpers.transfers import TransferOptimiser, MultiHorizonTransferOptimiser
from helpers.save_team_selection import save_team_selection

def transfer_optimization(analysis, budget_now, free_transfers):

    ## Current team selection file path
    current_team_file = f'./data/selections/selection-{date.today()}.json'

    ## Player data file path
    player_data_file = f'./data/cleaned/players-{date.today()}.json';

    ## If player data from today cannot be found, return error
    if not os.path.isfile(player_data_file):
        raise ValueError('Player data file not found')

    ## If a current_team_file from today cannot be found...
    if not os.path.isfile(current_team_file):

        ## Find the most recently created/modified file
        files = glob.glob('./data/selections/*')
        latest_file = max(files, key=os.path.getctime) 

        ## and assign to current_team_file   
        current_team_file = latest_file

    ## Load player and current squad data
    with open(player_data_file) as player_data, open(current_team_file) as current_team_data:
        players = json.load(player_data)
        current_team = json.load(current_team_data)

        ## Parse player data
        names = [player['web_name'] for player in players]
        codes = [player['player_code'] for player in players]
        clubs = [player['team_code'] for player in players]
        positions = [player['element_type'] for player in players]
        expected_scores = [player['ep_next'] for player in players]

        ## Parse price data
        buy_prices = [player.get('price') for player in players]
        sell_prices = [player.get('price') for player in players]

        # Parse current squad ids and indices in player data file
        current_squad_ids = [player.get('code') for player in current_team]
        current_squad_indices = [i for i, player in enumerate(players) if player.get('player_code') in current_squad_ids]
        
        ## Introduce one week transfer method
        if analysis == "transfer":

            opt = TransferOptimiser(free_transfers, expected_scores, buy_prices, sell_prices, positions, clubs)

            transfer_in_decisions, transfer_out_decisions, starters, sub_decisions, captain_decisions = opt.solve(current_squad_indices, budget_now=budget_now, sub_factor=0.2)

            for i in range(len(transfer_in_decisions)):
                if transfer_in_decisions[i].value() == 1:
                    print(f"Transferred in: {names[i]}, Price: {buy_prices[i]}, Expected Score: {expected_scores[i]}")
                if transfer_out_decisions[i].value() == 1:
                    print(f"Transferred out: {names[i]}, Price: {sell_prices[i]}, Expected Score: {expected_scores[i]}")

            player_indices = []
            print()
            print("First Team:")
            for i in range(len(starters)):
                if starters[i].value() == 1:
                    print("{}{}, Expected Score: {}".format(names[i], "*" if captain_decisions[i].value() == 1 else "", expected_scores[i]))
                    player_indices.append(i)
            print()
            print("Subs:")
            for i in range(len(sub_decisions)):
                if sub_decisions[i].value() == 1:
                    print(f"{names[i]}, Expected Score: {expected_scores[i]}")
                    player_indices.append(i)
            
            print()
            total_points = 0
            for i in range(len(transfer_in_decisions)):
                if starters[i].value() == 1 or sub_decisions[i].value() == 1:
                    total_points += expected_scores[i]
            print(f"Total expected score = {total_points}")

            ## Save team selection
            save_team_selection("transfers", players, starters, sub_decisions, codes, names, expected_scores, clubs, positions, buy_prices)

        ## Multitransfer horizon method
        elif analysis == "multitransfer":
            pass
            # HORIZON = 4
            # multi_score_forecast = pd.DataFrame({"week_{}".format(i): df["total_points"] / 38 for i in range(HORIZON)})
            # multi_score_forecast.head()


            # ## Instantiate MultiHorizonTransferOptimiser class
            # opt = MultiHorizonTransferOptimiser(multi_score_forecast.values.T, buy_prices.values, sell_prices.values, positions.values, clubs.values, 4)

            # ## Run solver
            # transfer_in_decisions, transfer_out_decisions, starters, sub_decisions, captain_decisions = opt.solve(current_squad_indices, budget_now=0, sub_factor=0.2)

            # for week in range(len(transfer_in_decisions)):
            #     print("Week {}".format(week))
            #     for i in range(len(transfer_in_decisions[week])):
            #         if transfer_in_decisions[week][i].value() == 1:
            #             print("Transferred in: {} {} {}".format(names[i], buy_prices[i], multi_score_forecast.values.T[week][i]))
            #         if transfer_out_decisions[week][i].value() == 1:
            #             print("Transferred out: {} {} {}".format(names[i], sell_prices[i], multi_score_forecast.values.T[week][i]))
