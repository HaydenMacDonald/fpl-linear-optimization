import pandas as pd
import numpy as np
from helpers.transfers import MultiHorizonTransferOptimiser

def transfer_optimization(current_team, data_file, analysis):

    ## TODO: correctly parse current_team and data_file
    
    ## Parse data_file
    names = data_file
    clubs = data_file
    positions = data_file
    expected_scores = data_file

    # Parse current squad
    # current_squad_indices = ...
    # current_squad_decisions = np.zeros(num_players) 
    # current_squad_decisions[current_team_indices] = 1
    
    # # Budget and Prices
    # budget_now = 0
    # buy_prices = 
    # sell_prices = 

    ## Introduce one week transfer method
    if analysis == "transfer":
        pass
    
    ## Multitransfer horizon method
    elif analysis == "multitransfer":
        HORIZON = 4
        multi_score_forecast = pd.DataFrame({"week_{}".format(i): df["total_points"] / 38 for i in range(HORIZON)})
        multi_score_forecast.head()


        ## Instantiate MultiHorizonTransferOptimiser class
        opt = MultiHorizonTransferOptimiser(multi_score_forecast.values.T, prices.values, prices.values, positions.values, clubs.values, 4)

        ## Run solver
        transfer_in_decisions, transfer_out_decisions, starters, sub_decisions, captain_decisions = opt.solve(player_indices, budget_now=0, sub_factor=0.2)

        for week in range(len(transfer_in_decisions)):
            print("Week {}".format(week))
            for i in range(len(transfer_in_decisions[week])):
                if transfer_in_decisions[week][i].value() == 1:
                    print("Transferred in: {} {} {}".format(names[i], prices[i], multi_score_forecast.values.T[week][i]))
                if transfer_out_decisions[week][i].value() == 1:
                    print("Transferred out: {} {} {}".format(names[i], prices[i], multi_score_forecast.values.T[week][i]))

