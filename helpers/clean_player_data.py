import json
from datetime import date
from helpers.write_player_data import write_player_data

def clean_player_data(data_file):
    
    players = []
    
    with open(data_file) as json_file:
        data = json.load(json_file)

        for player in data:

            ## Extract player code
            if player['code'] is not None:
                player_code = player['code']
            else:
                player_code = None

            ## Extract last name
            if player['web_name'] is not None:
                web_name = player['web_name']
            else:
                web_name = None

            ## Extract last year's points
            if player['total_points'] is not None:
                total_points = player['total_points']
            else:
                total_points = 0

            ## Extract team_code
            if player['team_code'] is not None:
                team_code = player['team_code']
            else:
                team_code = 100

            ## Extract element_type
            if player['element_type'] is not None:
                element_type = player['element_type']
            else:
                element_type = 3

            ## Extract player's price
            if player['now_cost'] is not None:
                price = player['now_cost'] / 10
            else:
                price = 100
            
            ## Append data to batch list
            players.append([player_code, web_name, total_points, team_code, element_type, price])

    write_player_data(players, f'.\data\cleaned\players-{date.today()}.json')

    return players
