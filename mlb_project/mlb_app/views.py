from django.shortcuts import render
import mlbgame, datetime, statsapi, pandas as pd

# Create your views here.

def home(request):
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

    return render(request, 'home.html', {'data': games, 'today': areGamesToday, 'searched': searched})

def search(request, team_searched):
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

    return render(request, 'home.html', {'data': games, 'today': areGamesToday, 'team': team_searched, 'searched': searched})

def standings(request):
    standings_dict = statsapi.standings_data(leagueId="103,104", division="all", include_wildcard=True)
    al_west = standings_dict.get(200).get('teams')
    al_east = standings_dict.get(201).get('teams')
    al_central = standings_dict.get(202).get('teams')
    nl_central = standings_dict.get(205).get('teams')
    nl_east = standings_dict.get(203).get('teams')
    nl_west = standings_dict.get(204).get('teams')
    return render(request, 'standings.html', {'al_west':al_west, 'al_east':al_east, 'al_central':al_central, 'nl_central':nl_central, 'nl_east':nl_east, 'nl_west':nl_west})