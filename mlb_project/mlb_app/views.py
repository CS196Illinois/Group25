from django.shortcuts import render
import mlbgame, datetime

# Create your views here.

def home(request):
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
            games.append(gamesOnDay)
        dayCount += 1
    if games is []:
        areGamesToday = False
        #go to next season
        date = mlbgame.important_dates(now.year+1).first_date_seas.split('-')
        year = int(date[0])
        month = int(date[1])
        day = int(date[2][:2])
        mlbgame.day(year, month, day)[0:10]

    return render(request, 'home.html', {'data': games, 'today': areGamesToday})