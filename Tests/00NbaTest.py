import requests
import json
import base64

#stat = requests.get("https://api.mysportsfeeds.com/v1.1/pull/nba/2016-playoff/bos/cumulative_player_stats.json")

response = requests.get(
            url="https://api.mysportsfeeds.com/v1.1/pull/nba/2016-2017-regular/game_boxscore.json?gameid={game-identifier}",
            params={
                "fordate": "20161121" ,
                "player" : "stephen-curry"
            },
            headers={
                "Authorization": "Basic " + base64.b64encode('{}:{}'.format("matthewc","change112").encode('utf-8')).decode('ascii')
            })

#responsejson = json.loads(response)
#print(response.status_code)
#print(type(response.content))

#decoded = json.loads(response.content.decode('latin1'))
#print(type(decoded))
#print(decoded)

games = requests.get(
        url="https://api.mysportsfeeds.com/v1.1/pull/nba/2016-2017-regular/full_game_schedule.json",
        params={
            #"date": "from-20161101-to-20161102"
            "date": "20161101"
        },
        headers={
            "Authorization": "Basic " + base64.b64encode('{}:{}'.format("matthewc","change112").encode('utf-8')).decode('ascii')
        })

loaded = json.loads(games.content.decode('latin1'))
played = loaded['fullgameschedule']['gameentry']
firstGame = played[0]

print (firstGame['date'])
awayTeam = firstGame['awayTeam']['Abbreviation']
homeTeam = firstGame['homeTeam']['Abbreviation']

print(awayTeam)
print(homeTeam)

test = loaded['fullgameschedule']['gameentry'][0]['date']
print(test)

#print (loaded)
#print(games.content)
