import pickle
import numpy as np
from sklearn.linear_model import LogisticRegression

import urllib
import requests
from bs4 import BeautifulSoup


# sets up functions to acquire team pitching stats
url_pitching = "https://www.espn.com/mlb/stats/team/_/view/pitching"
page = requests.get(url_pitching)
soup = BeautifulSoup(page.text, 'html.parser')
tablePRows = soup.find_all(
    'tr', attrs={'class': "Table__TR Table__TR--sm Table__even"})

# sets up functions to acquire team batting stats
url_batting = "https://www.espn.com/mlb/stats/team"
page = requests.get(url_batting)
soup = BeautifulSoup(page.text, 'html.parser')
tableBRows = soup.find_all(
    'tr', attrs={'class': "Table__TR Table__TR--sm Table__even"})

# Setting tokens for team batting stats on ESPN database
teamBatting = {
    "New York Mets": 0,
    "Atlanta Braves": 1,
    "Boston Red Sox": 2,
    "Washington Nationals": 3,
    "San Francisco Giants": 4,
    "Chicago White Sox": 5,
    "Baltimore Orioles": 6,
    "Colorado Rockies": 7,
    "Philadelphia Phillies": 8,
    "San Diego Padres": 9,
    "Los Angeles Dodgers": 10,
    "Toronto Blue Jays": 11,
    "Los Angeles Angels": 12,
    "New York Yankees": 13,
    "Detroit Tigers": 14,
    "Kansas City Royals": 15,
    "Miami Marlins": 16,
    "Minnesota Twins": 17,
    "Arizona Diamondbacks": 18,
    "Houston Astros": 19,
    "Tampa Bay Rays": 20,
    "St. Louis Cardinals": 21,
    "Cleveland Indians": 22,
    "Seattle Mariners": 23,
    "Oakland Athletics": 24,
    "Milwaukee Brewers": 25,
    "Chicago Cubs": 26,
    "Pittsburgh Pirates": 27,
    "Texas Rangers": 28,
    "Cincinnati Reds": 29,
}
# Setting tokens for team pitching stats on ESPN database
teamPitching = {
    "Los Angeles Dodgers": 0,
    "Cleveland Indians": 1,
    "Tampa Bay Rays": 2,
    "Minnesota Twins": 3,
    "Oakland Athletics": 4,
    "Chicago White Sox": 5,
    "Cincinnati Reds": 6,
    "San Diego Padres": 7,
    "St. Louis Cardinals": 8,
    "Chicago Cubs": 9,
    "Milwaukee Brewers": 10,
    "Kansas City Royals": 11,
    "Houston Astros": 12,
    "New York Yankees": 13,
    "Atlanta Braves": 14,
    "Baltimore Orioles": 15,
    "Toronto Blue Jays": 16,
    "San Francisco Giants": 17,
    "Pittsburgh Pirates": 18,
    "Arizona Diamondbacks": 19,
    "Miami Marlins": 20,
    "New York Mets": 21,
    "Seattle Mariners": 22,
    "Texas Rangers": 23,
    "Los Angeles Angels": 24,
    "Washington Nationals": 25,
    "Philadelphia Phillies": 26,
    "Boston Red Sox": 27,
    "Colorado Rockies": 28,
    "Detroit Tigers": 29,
}

# call the API to get stats for both teams needed to predict game
def get_winner(home_team_name, away_team_name):
    # Stores the team stats in a numpy array and predicts the outcome of the game
    inputStats = gatherStats(home_team_name, away_team_name)
    stats = np.array([inputStats[0], inputStats[1],
                      inputStats[2], inputStats[3]]).reshape(1, 4)

    prediction = predict_game(stats)

    if (prediction == 1):
        return home_team_name
    else:
        return away_team_name


def predict_game(stats):
    # Creates path to models

    # Loads logistic regression model from pickle file
    with open('mlb_app/predictor/models.p', 'rb') as pickled:
        data = pickle.load(pickled)
    logreg = data['regression']

    prediction = logreg.predict(stats)

    return prediction[0]

# main function to gather stats of the inputted teams


def gatherStats(homeTeam, awayTeam):
    output = []
    output.append(gatherPitchingStats(homeTeam, awayTeam)[0])
    output.append(gatherBattingStats(homeTeam, awayTeam)[0])
    output.append(gatherBattingStats(homeTeam, awayTeam)[1])
    output.append(gatherBattingStats(homeTeam, awayTeam)[2])
    return output


def findPStats(index):
    count = 0
    teams = []
    stats = []
    output = []
    for row in tablePRows:
        if count == (index + 30):
            teams.append(row)
            for team in teams:
                stats.append(team.find_all('td'))
                for stat in stats:
                    output.append(float(stat[3].text))
                    return output
        count = count + 1
    count = 0


def gatherPitchingStats(homeTeam, awayTeam):
    homeIndex = teamPitching.get(homeTeam)
    awayIndex = teamPitching.get(awayTeam)
    finalStats = []
    finalStats.append(findPStats(homeIndex)[0] - findPStats(awayIndex)[0])
    return (finalStats)


def findBStats(index):
    count = 0
    teams = []
    stats = []
    batting = []
    for row in tableBRows:
        if count == (index + 30):
            teams.append(row)
            for team in teams:
                stats.append(team.find_all('td'))
                for stat in stats:
                    batting.append(float(stat[7].text))
                    batting.append(float(stat[14].text))
                    batting.append(float(stat[12].text))
                    return batting
        count = count + 1
    count = 0


def gatherBattingStats(homeTeam, awayTeam):
    homeIndex = teamBatting.get(homeTeam)
    awayIndex = teamBatting.get(awayTeam)
    finalStats = []
    finalStats.append(findBStats(homeIndex)[0] - findBStats(awayIndex)[0])
    finalStats.append(findBStats(homeIndex)[1] - findBStats(awayIndex)[1])
    finalStats.append(findBStats(homeIndex)[2] - findBStats(awayIndex)[2])
    return (finalStats)