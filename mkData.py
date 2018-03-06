import requests
import json
import base64
import numpy
import datetime
import pandas

#function to return all games played in a string list
#in the correct game identifier format
#YYYYMMDD-away team(acc)-home team(acc)
globalcount = 0;

def gamesHappeningon(datestr): #date is a string in the format YYYYMMDD
    global globalcount
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
    globalcount = globalcount + 1;
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

def getPlayerStats(API):
    "given a player's json file, will output a row vector with their chosen stats"
    tempStats = numpy.zeros(31)
    #one hot encoding
    if API["player"]["Position"]== "PG":
        tempStats[0] = 1
    if API["player"]["Position"]== "SG":
        tempStats[1] = 1
    if API["player"]["Position"]== "C":
        tempStats[2] = 1
    if API["player"]["Position"]== "SF":
        tempStats[3] = 1
    if API["player"]["Position"]== "PF":
        tempStats[4] = 1

    #acutal stats
    tempStats[5] = API["stats"]["Fg2PtAtt"]["#text"]
    tempStats[6] = API["stats"]["Fg2PtMade"]["#text"]
    tempStats[7] = API["stats"]["Fg3PtAtt"]["#text"]
    tempStats[8] = API["stats"]["Fg3PtMade"]["#text"]
    tempStats[9] = API["stats"]["FtAtt"]["#text"]
    tempStats[10] = API["stats"]["FtMade"]["#text"]
    tempStats[11] = API["stats"]["OffReb"]["#text"]
    tempStats[12] = API["stats"]["DefReb"]["#text"]
    tempStats[13] = API["stats"]["Ast"]["#text"]
    tempStats[14] = API["stats"]["Pts"]["#text"]
    tempStats[15] = API["stats"]["Tov"]["#text"]
    tempStats[16] = API["stats"]["Stl"]["#text"]
    tempStats[17] = API["stats"]["Blk"]["#text"]
    tempStats[18] = API["stats"]["BlkAgainst"]["#text"]
    tempStats[19] = API["stats"]["Fouls"]["#text"]
    tempStats[20] = API["stats"]["FoulsDrawn"]["#text"]
    tempStats[21] = API["stats"]["FoulPers"]["#text"]
    tempStats[22] = API["stats"]["FoulPersDrawn"]["#text"]
    tempStats[23] = API["stats"]["FoulTech"]["#text"]
    tempStats[24] = API["stats"]["FoulTechDrawn"]["#text"]
    tempStats[25] = API["stats"]["FoulFlag1"]["#text"]
    tempStats[26] = API["stats"]["FoulFlag1Drawn"]["#text"]
    tempStats[27] = API["stats"]["FoulFlag2"]["#text"]
    tempStats[28] = API["stats"]["FoulFlag2Drawn"]["#text"]
    tempStats[29] = API["stats"]["PlusMinus"]["#text"]
    tempStats[30] = API["stats"]["MinSeconds"]["#text"]

    return tempStats

def gameStats(gameidentifier, away):
    "creates row of stats for one team"
    global globalcount
    gameSet = numpy.zeros(1) #includes the x0 term = 1
    gameSet[0] = 1
    #print(i)
    #print("hdf")
    #print(gameidentifier)
    #print(away)
    tempGame = requests.get(
        url = "https://api.mysportsfeeds.com/v1.1/pull/nba/2016-2017-regular/game_boxscore.json?gameid=" + gameidentifier,
        params = {

        },
        headers = {
            "Authorization": "Basic " + base64.b64encode('{}:{}'.format("matthewc","change112").encode('utf-8')).decode('ascii')
        })

    globalcount = globalcount + 1;
    #print(globalcount)
    #print(tempGame.status_code)
    loaded = json.loads(tempGame.content.decode('latin1'))

    #print(loaded)

    if away:
        playerTemp = loaded["gameboxscore"]["awayTeam"]["awayPlayers"]["playerEntry"]
    else:
        playerTemp = loaded["gameboxscore"]["homeTeam"]["homePlayers"]["playerEntry"]
    PG = numpy.zeros(31) #31 stats we are looking at
    SG = numpy.zeros(31)
    C = numpy.zeros(31)
    SF = numpy.zeros(31)
    PF = numpy.zeros(31)
    count = numpy.zeros(5) #numbezr of players on each team in each role
    # 0-PG 1-SG 2-C 3-PF 4-SF

    for j in range(0,len(playerTemp)): #scans through all players
        position = playerTemp[j]["player"]["Position"]
        player = playerTemp[j]
        #print(position)
        if position == "PG":
            count[0]+=1
            PG = PG + getPlayerStats(player)
        if position == "SG":
            count[1]+=1
            SG = SG + getPlayerStats(player)
        if position == "C":
            count[2]+=1
            C = C + getPlayerStats(player)
        if position == "SF":
            count[3]+=1
            SF = SF + getPlayerStats(player)
        if position == "PF":
            count[4]+=1
            PF = PF + getPlayerStats(player)
        if position == "G":
            count[0]+=1
            count[1]+=1
            PG = PG + 0.5*getPlayerStats(player)
            SG = SG + 0.5*getPlayerStats(player)
        if position == "F":
            count[3]+=1
            count[4]+=1
            SF = SF + 0.5*getPlayerStats(player)
            PF = PF + 0.5*getPlayerStats(player)
    if count[0] != 0:
        PG = PG/count[0]
    if count[1] != 0:
        SG = SG/count[1]
    if count[2] != 0:
        C = C/count[2]
    if count[3] != 0:
        SF = SF/count[3]
    if count[4] != 0:
        PF = PF/count[4]

    gameSet = numpy.concatenate([gameSet,PG,SG,C,SF,PF])

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

    #formatted is a list of days between the two dates specified
    gamesHappening = []
    gamesForTheDay = gamesHappeningon(strFormatted)
    print(gamesForTheDay)
    for idx, j in enumerate(gamesForTheDay):
        gamesHappening.append(gamesForTheDay[idx])
    print(gamesHappening)
    #parese individual games
    #concatentates each game's stats (home and away)
    training = numpy.empty((0,312))
    #print(gamesHappening[0])
    #print (gamesHappening)
    for idx, i in enumerate(gamesHappening):
        temprow = []
        #print(gamesHappening[idx])
        temprow = numpy.concatenate([temprow,gameStats(gamesHappening[idx],'true'),gameStats(gamesHappening[idx],'false')])
        training = numpy.vstack((training,temprow))

    #print(training)
    #print(type(training))

    print(training)
    #numpy.savetxt("DataSets - Copy/" + str(startDateInt) + ".csv",training,delimiter=",")
    #df = pandas.DataFrame(training)
    #df.to_csv("DataSets/Playoffs/" + str(startDateInt) + ".csv")
    print("done")

for i in range (0,1):
    trainingSet(20161112+i)
