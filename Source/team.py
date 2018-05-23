import base64
import requests
import json

class Team: 
    name = ""

    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def getSchedule(self, userName, passw):
        try:
            response = requests.get(
                url="https://api.mysportsfeeds.com/v1.2/pull/nfl/2018-regular/full_game_schedule.json?team=" + self.getName(),
                params={
                #"Abbreviation": "CIN"
                },
                headers={
                    "Authorization": "Basic " + base64.b64encode('{}:{}'.format(userName,passw).encode('utf-8')).decode('ascii')
                }
            )
            data = response.json()
            print(" 2018 Schedule: \n")
            for i in range(0, 16):
                date = data['fullgameschedule']['gameentry'][i]['date']
                awayTeam = data['fullgameschedule']['gameentry'][i]['awayTeam']['City'] \
                + " "  + data['fullgameschedule']['gameentry'][i]['awayTeam']['Name']
                homeTeam = data['fullgameschedule']['gameentry'][i]['homeTeam']['City'] \
                + " "  + data['fullgameschedule']['gameentry'][i]['homeTeam']['Name']
                time = data['fullgameschedule']['gameentry'][i]['time']
                gameData = (" " + date + " " * 10 + awayTeam + " @ " + homeTeam)
                dataLength = len(gameData)
                spaces = 80 - dataLength
                print( gameData + ' ' * spaces + time)
        
        except requests.exceptions.RequestException:
            print('HTTP Request failed')
    #send_request()
