import pandas as pd
import numpy as np
from helpers.select_team import select_team
from helpers.write_player_data import write_player_data
from datetime import date

def process_player_data(players, season):

    columns = ['player_code', 'web_name', 'total_points', 'team_code', 'element_type', 'price', 'form', 'points_per_game', 'ict_rank', 'ep_next', 'ep_this', 'chance_of_playing_next_round', 'chance_of_playing_this_round', 'fixtures', 'history', 'history_past']
    df = pd.DataFrame(players, columns = columns)

    ## Replace total_points scores of 0 with NA
    df['total_points'] = df['total_points'].replace(0, np.nan)

    ## Replace new player's missing total_points score with the average of all players 
    df['total_points'] = df['total_points'].fillna(df.groupby('element_type')['total_points'].transform('mean'))
    
    ## If selecting based on last season, assign total_points to expected points
    if season == 'previous' or season is None:
        expected_scores = pd.Series([ x[0].get('total_points') for x in df['history_past']])
        print(expected_scores)
    elif season == 'current':
        expected_scores = df['form']

    ## Extract columns as series
    prices = df["price"]
    positions = df["element_type"]
    clubs = df["team_code"]
    # so we can read the results
    names = df["web_name"]
    codes = df["player_code"]
    decisions, captain_decisions, sub_decisions = select_team(expected_scores.values, prices.values, positions.values, clubs.values)
    
    # Print team
    print("\nTeam:")
    for i in range(df.shape[0]):
        if decisions[i].value() != 0:
            print("{} Points = {}, Price = {}".format(names[i], expected_scores[i], prices[i]))

    # Print Captain choice
    print("\nCaptain:")
    for i in range(df.shape[0]):
        if captain_decisions[i].value() == 1:
            print("{} Points = {}, Price = {}".format(names[i], expected_scores[i], prices[i]))

    # Print Subs
    print("\nSubs:")
    for i in range(df.shape[0]):
        if sub_decisions[i].value() == 1:
            print("{} Points = {}, Price = {}".format(names[i], expected_scores[i], prices[i]))

    ## Save team selection
    team = []
    for i in range(df.shape[0]):
        if decisions[i].value() != 0 or sub_decisions[i].value() == 1:
            
            rank = ""
            if decisions[i].value() != 0:
                rank = "player"
            elif sub_decisions[i].value() == 1:
                rank = "sub"
            else:
                rank = "none"

            ## Append data to batch list
            team.append(dict(code = int(codes[i]), 
                             name = names[i], 
                             expected_score = int(expected_scores[i]), 
                             rank = rank, 
                             club = int(clubs[i]), 
                             position = int(positions[i]), 
                             buy_price = prices[i]))
            
    write_player_data(team, f'.\data\selections\selection-{date.today()}.json')

    


    