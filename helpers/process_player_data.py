import pandas as pd
from helpers.select_team import select_team

def process_player_data(players):

    columns = ['web_name', 'total_points', 'team_code', 'element_type', 'price']
    df = pd.DataFrame(players, columns = columns)

    df["imputed_total_points"] = df.groupby("element_type")["total_points"].transform(lambda x: x.fillna(x.mean()))
    #df["imputed_total_points"] = df.groupby("element_type")["total_points"].transform(lambda x : x.mean() if x == 0 else x)
    
    expected_scores = df["imputed_total_points"]  # total points from last season
    prices = df["price"]
    positions = df["element_type"]
    clubs = df["team_code"]
    # so we can read the results
    names = df["web_name"]
    decisions, captain_decisions, sub_decisions = select_team(expected_scores.values, prices.values, positions.values, clubs.values)
    
    # print results
    for i in range(df.shape[0]):
        if decisions[i].value() != 0:
            print("{} Points = {}, Price = {}".format(names[i], expected_scores[i], prices[i]))

    print("Subs:")
    # print results
    for i in range(df.shape[0]):
        if sub_decisions[i].value() == 1:
            print("{} Points = {}, Price = {}".format(names[i], expected_scores[i], prices[i]))

    print("Captain:")
    # print results
    for i in range(df.shape[0]):
        if captain_decisions[i].value() == 1:
            print("{} Points = {}, Price = {}".format(names[i], expected_scores[i], prices[i]))