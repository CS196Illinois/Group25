from django.shortcuts import render
import mlbgame, datetime

# Create your views here.

def home(request):
    now = datetime.datetime.now()

    #retrieve today's games
    games = mlbgame.day(now.year, now.month, now.day)[0:10]
    if games is []:
        #go to next season
        date = mlbgame.important_dates(now.year+1).first_date_seas.split('-')
        year = int(date[0])
        month = int(date[1])
        day = int(date[2][:2])
        mlbgame.day(year, month, day)[0:10]

    return render(request, 'home.html', {'data': games})