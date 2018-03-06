import requests
import json
import base64
import numpy
import datetime
import pandas

#function to return all games played in a string list
#in the correct game identifier format
#YYYYMMDD-away team(acc)-home team(acc)
#globalcount = 0;

def gamesHappeningon(datestr): #date is a string in the format YYYYMMDD
    #global globalcount
    "returns a list of strings with all the games"
    #70 is the server limit for requests
    response = requests.get(
        url = "https://api.mysportsfeeds.com/v1.1/pull/nba/2016-2017-regular/full_game_schedule.json",
        params = {
            "date" : datestr
        },
        headers = {
            "Authorization": "Basic " + base64.b64encode('{}:{}'.format("matthewc","change112").encode('utf-8')).decode('ascii')
        })
    #globalcount = globalcount + 1;
    #print(globalcount)
    #print(response.status_code)
    loaded = json.loads(response.content.decode('latin1'))
    #loaded = response
    gamelist = []

    #print(loaded['fullgameschedule'])#['gameentry'])
    if 'gameentry' in loaded['fullgameschedule']:
        for i in range (0,len(loaded['fullgameschedule']['gameentry'])): #how many games in the day
            date = loaded['fullgameschedule']['gameentry'][i]['date']
            awayTeam = loaded['fullgameschedule']['gameentry'][i]['awayTeam']['Abbreviation']
            homeTeam = loaded['fullgameschedule']['gameentry'][i]['homeTeam']['Abbreviation']

            retstr = date[0:4]+date[5:7]+date[8:10]  +  "-"  +  awayTeam  +  "-"  +  homeTeam
            #print (retstr)
            gamelist.append(retstr)

    return gamelist

def gameStats(gameidentifier):
    "creates row of stats for one team"
    #global globalcount

    gameSet = numpy.zeros(1)
    tempGame = requests.get(
        url = "https://api.mysportsfeeds.com/v1.2/pull/nba/2016-2017-regular/scoreboard.json?fordate=" + gameidentifier,
        params = {
        },
        headers = {
            "Authorization": "Basic " + base64.b64encode('{}:{}'.format("matthewc","change112").encode('utf-8')).decode('ascii')
        })

    loaded = json.loads(tempGame.content.decode('latin1'))
    ans = []
    for i in range(0,len(loaded['scoreboard']['gameScore'])):
        if(loaded['scoreboard']['gameScore'][i]['homeScore']>loaded['scoreboard']['gameScore'][i]['awayScore']):
            ans.append(1)
        else:
            ans.append(0)
    return ans


    return gameSet

def trainingSet(startDateInt): #startDateInt is in the form  YYYYMMDD
    "combines the home and away team's stats into one row [away home]"
    print(startDateInt)
    #parse dates
    startday = startDateInt%100
    startmonth = (startDateInt%10000) // 100
    startyear = startDateInt//10000

    #assume year is the same
    start = datetime.date(startyear,startmonth,startday)
    #scan through all dates
    strDate = (start).isoformat()
    strFormatted = strDate.replace('-', '')

    #parese individual games
    #concatentates each game's stats (home and away)
    training = []
    training = numpy.append(training,gameStats(strFormatted))
    print(training)
    print(type(training[0]))

    numpy.savetxt("Labels/" + str(startDateInt) + ".csv",training,delimiter=",")

    print("done")

for i in range (0,50):
    try:
        date = 20170401+i
        trainingSet(date)
    except KeyError:
        filler = []
        numpy.savetxt("Labels/" + str(date) + ".csv",filler,delimiter=",")
