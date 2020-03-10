import requests
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep
from random import randint

one_seed = 1933
two_seed = 1967
four_seed = 1970
five_seed = 1978
six_seed = 1991

# Empty dataframe
df = pd.DataFrame(columns = ["Year", "Game", "Winning Team", "Losing Team", "Winner's Score", "Loser's Score"])

headers = {"user-agent": "Mozilla/5.0"}

num_cells = 3
year = 1970
request = 0

# Scrape and store data into df
while True:
    if year > 2018:
        break
    playoffs_url = "https://www.footballdb.com/seasons/nfl/" + str(year)
    p = requests.get(playoffs_url, headers = headers)
    request += 1
    print(request)
    soup_playoffs = BeautifulSoup(p.text, "lxml")
    matches = soup_playoffs.find_all("table", class_ = "scrollable")
    matches = matches[0]
    playoff_info = []
    for cell in matches.find_all("td"):
        playoff_info.append(cell.text)
    num_games = len(playoff_info) // num_cells
    games = []
    for i in range(num_games):
        game = playoff_info[:num_cells]
        series = game[1]
        teams = game[2].split("@")
        team_1 = teams[0].strip()
        team_2 = teams[1].strip()
        team_1_info = team_1.split()
        team_2_info = team_2.split()
        score_1 = team_1_info[-1]
        score_2 = team_2_info[-1]
        while True:
            team_1 = team_1[:-1]
            if team_1[-1].isupper() and team_1[-2].islower():
                team_1 = team_1[:-1]
                break
        while True:
            team_2 = team_2[:-1]
            if team_2[-1].isupper() and team_2[-2].islower():
                team_2 = team_2[:-1]
                break
        if score_1 > score_2:
            w_team = team_1
            w_score = score_1
            l_team = team_2
            l_score = score_2
        else:
            w_team = team_2
            w_score = score_2
            l_team = team_1
            l_score = score_1
        game = [year, series, w_team, l_team, w_score, l_score]
        games.append(game)
        del playoff_info[:num_cells]
    df_current = pd.DataFrame(games, columns = ["Year", "Game", "Winning Team", "Losing Team", "Winner's Score", "Loser's Score"])
    df = df.append(df_current)
    print(df)
    year += 1
    sleep(randint(1,4))

# Output to csv file    
df.to_csv("nfl playoffs.csv", index=False, encoding="utf-8")