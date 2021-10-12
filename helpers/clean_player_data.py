from datetime import date
from helpers.write_player_data import write_player_data

def clean_player_data(data):
    
    players = []
    
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

        ## Chance of playing next round
        if player['chance_of_playing_next_round'] is not None:
            chance_of_playing_next_round = player['chance_of_playing_next_round']
        else:
            chance_of_playing_next_round = 0

        ## Chance of playing this round
        if player['chance_of_playing_this_round'] is not None:
            chance_of_playing_this_round = player['chance_of_playing_this_round']
        else:
            chance_of_playing_this_round = 0

        ## Expected Points next round
        if player['ep_next'] is not None:
            ep_next = player['ep_next']
        else:
            ep_next = 0

        ## Expected points this round
        if player['ep_this'] is not None:
            ep_this = player['ep_this']
        else:
            ep_this = 0

        ## Player form
        if player['form'] is not None:
            form = player['form']
        else:
            form = 0

        ## Points per game (across all games with minutes)
        if player['points_per_game'] is not None:
            points_per_game = player['points_per_game']
        else:
            points_per_game = 0

        ## ICT (Influence, Creativity, Threat) Index Rank (lower is better)
        if player['ict_index_rank'] is not None:
            ict_rank = player['ict_index_rank']
        else:
            ict_rank = 500

        ## Fixtures array
        if player['fixtures'] is not None:
            fixtures = []
            player_fixtures = player['fixtures']
            for game in player_fixtures:
                match = {}
                match = {"event_name": game['event_name'], "is_home": game['is_home'], "difficulty": game['difficulty']}
                fixtures.append(match.copy())

        ## Historical matches this season
        if player['history'] is not None:
            history = player['history']
        else: 
            history = []

        ## Historical matches in past seasons
        if player['history_past'] and any(d['season_name'] == '2020/21' for d in player['history_past']):
            history_past = [d for d in player['history_past'] if d['season_name'] == '2020/21']
        else:
            history_past = [dict(season_name = '2020/21', total_points = 0)]
        
        ## Append data to batch list
        players.append(dict(player_code = player_code, 
                            web_name = web_name, 
                            total_points = total_points, 
                            team_code = team_code, 
                            element_type = element_type, 
                            price = price, 
                            form = float(form), 
                            points_per_game = float(points_per_game), 
                            ict_rank = ict_rank, 
                            ep_next = float(ep_next), 
                            ep_this = float(ep_this), 
                            chance_of_playing_next_round = chance_of_playing_next_round, 
                            chance_of_playing_this_round = chance_of_playing_this_round,
                            fixtures = fixtures,
                            history = history,
                            history_past = history_past))

    write_player_data(players, f'./data/cleaned/players-{date.today()}.json')

    return players
