from datetime import date
from helpers.write_player_data import write_player_data

def save_team_selection(path, data, decisions, sub_decisions, codes, names, expected_scores, clubs, positions, prices):
    team = []

    if hasattr(data, 'shape'):
        data_length = data.shape[0]
    else:
        data_length = len(data)

    for i in range(data_length):
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
            
    write_player_data(team, f'./data/{path}/selection-{date.today()}.json')