from django.shortcuts import render
import mlbgame, datetime, itertools
from mlb_app.predictor.prediction_model import get_winner as predict

# Create your views here.

def home(request):
    fullNames = {
        "Dodgers": "Los Angeles Dodgers",
        "Indians": "Cleveland Indians",
        "Rays": "Tampa Bay Rays",
        "Twins": "Minnesota Twins",
        "Athletics": "Oakland Athletics",
        "White Sox": "Chicago White Sox",
        "Reds": "Cincinnati Reds",
        "Padres": "San Diego Padres",
        "Cardinals": "St. Louis Cardinals",
        "Cubs": "Chicago Cubs",
        "Brewers": "Milwaukee Brewers",
        "Royals": "Kansas City Royals",
        "Astros": "Houston Astros",
        "Yankees": "New York Yankees",
        "Braves": "Atlanta Braves",
        "Orioles": "Baltimore Orioles",
        "Blue Jays": "Toronto Blue Jays",
        "Giants": "San Francisco Giants",
        "Pirates": "Pittsburgh Pirates",
        "Diamondbacks": "Arizona Diamondbacks",
        "Marlins": "Miami Marlins",
        "Mets": "New York Mets",
        "Mariners": "Seattle Mariners",
        "Rangers": "Texas Rangers",
        "Angels": "Los Angeles Angels",
        "Nationals": "Washington Nationals",
        "Phillies": "Philadelphia Phillies",
        "Red Sox": "Boston Red Sox",
        "Rockies": "Colorado Rockies",
        "Tigers": "Detroit Tigers"
    }

    teamNames = {v: k for k, v in fullNames.items()}

    searched = False
    now = datetime.datetime.now()
    areGamesToday = True

    #retrieve today's games
    games = mlbgame.day(now.year, now.month, now.day)[0:10]
    dayCount = 1
    #retrieve this week's games if not enough games today
    while len(games) < 10 and dayCount < 7:
        dateToCheck = datetime.date.today()
        dateToCheck += datetime.timedelta(days=dayCount)
        gamesOnDay = mlbgame.day(dateToCheck.year, dateToCheck.month, dateToCheck.day)[0:10-len(games)]
        if len(gamesOnDay) > 0:
            for game in gamesOnDay:
                games.append(game)
        dayCount += 1

    dayCount = 0
    if len(games) == 0:
        areGamesToday = False
        #go to next season
        date = mlbgame.important_dates(now.year+1).first_date_seas.split('-')
        year = int(date[0])
        month = int(date[1])
        day = int(date[2][:2])
        while len(games) < 10 and dayCount < 6:
            dateToCheck = datetime.date(year, month, day)
            dateToCheck += datetime.timedelta(days=dayCount)
            gamesOnDay = mlbgame.day(dateToCheck.year, dateToCheck.month, dateToCheck.day)[0:10]
            if len(gamesOnDay) > 0:
                for game in gamesOnDay:
                    games.append(game)
            dayCount += 1

    predictions = []
    for game in games:
        predictions.append(teamNames[predict(fullNames[game.home_team], fullNames[game.home_team])])

    zipped = list(zip(games, predictions))

    return render(request, 'home.html', {'data': zipped, 'today': areGamesToday, 'searched': searched})

def search(request, team_searched):
    fullNames = {
        "Dodgers": "Los Angeles Dodgers",
        "Indians": "Cleveland Indians",
        "Rays": "Tampa Bay Rays",
        "Twins": "Minnesota Twins",
        "Athletics": "Oakland Athletics",
        "White Sox": "Chicago White Sox",
        "Reds": "Cincinnati Reds",
        "Padres": "San Diego Padres",
        "Cardinals": "St. Louis Cardinals",
        "Cubs": "Chicago Cubs",
        "Brewers": "Milwaukee Brewers",
        "Royals": "Kansas City Royals",
        "Astros": "Houston Astros",
        "Yankees": "New York Yankees",
        "Braves": "Atlanta Braves",
        "Orioles": "Baltimore Orioles",
        "Blue Jays": "Toronto Blue Jays",
        "Giants": "San Francisco Giants",
        "Pirates": "Pittsburgh Pirates",
        "Diamondbacks": "Arizona Diamondbacks",
        "Marlins": "Miami Marlins",
        "Mets": "New York Mets",
        "Mariners": "Seattle Mariners",
        "Rangers": "Texas Rangers",
        "Angels": "Los Angeles Angels",
        "Nationals": "Washington Nationals",
        "Phillies": "Philadelphia Phillies",
        "Red Sox": "Boston Red Sox",
        "Rockies": "Colorado Rockies",
        "Tigers": "Detroit Tigers"
    }

    teamNames = {v: k for k, v in fullNames.items()}

    searched = True
    now = datetime.datetime.now()
    areGamesToday = True

    #retrieve today's games
    games = mlbgame.day(now.year, now.month, now.day, home=team_searched, away=team_searched)[0:10]
    dayCount = 1
    #retrieve this week's games if not enough games today
    while len(games) < 10 and dayCount < 7:
        dateToCheck = datetime.date.today()
        dateToCheck += datetime.timedelta(days=dayCount)
        gamesOnDay = mlbgame.day(dateToCheck.year, dateToCheck.month, dateToCheck.day, home=team_searched, away=team_searched)[0:10-len(games)]
        if len(gamesOnDay) > 0:
            games.append(gamesOnDay[0])
        dayCount += 1

    dayCount = 0
    if len(games) == 0:
        areGamesToday = False
        #go to next season
        date = mlbgame.important_dates(now.year+1).first_date_seas.split('-')
        year = int(date[0])
        month = int(date[1])
        day = int(date[2][:2])
        while len(games) < 10 and dayCount < 6:
            dateToCheck = datetime.date(year, month, day)
            dateToCheck += datetime.timedelta(days=dayCount)
            gamesOnDay = mlbgame.day(dateToCheck.year, dateToCheck.month, dateToCheck.day, home=team_searched, away=team_searched)[0:10]
            if len(gamesOnDay) > 0:
                for game in gamesOnDay:
                    games.append(game)
            dayCount += 1

    predictions = []
    for game in games:
        predictions.append(teamNames[predict(fullNames[game.home_team], fullNames[game.home_team])])

    zipped = list(zip(games, predictions))

    return render(request, 'home.html', {'data': zipped, 'today': areGamesToday, 'team': team_searched, 'searched': searched})