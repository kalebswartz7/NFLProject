import base64
import requests
import json

class Team: 
    name = ""
    positions = []
    count = 0

    """ Team Constructor """ 

    def __init__(self, name):
        self.name = name
        self.positions = ['QB', 'RB', 'WR', 'TE', 'C', 'G', 'OT', 'LB', 'CB', 'DB', 'DE', 'SS', 'DT', 'K']


    """ Returns the team name (abbreviation) """

    def getName(self):
        return self.name


    """ Gets a specific team's schedule """

    def getSchedule(self, userName, passw):
        try:
            response = requests.get(
                url="https://api.mysportsfeeds.com/v1.2/pull/nfl/2018-regular/full_game_schedule.json?",
                params={
                    'team' : self.getName()
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
            print("\n")
        
        except requests.exceptions.RequestException:
            print('HTTP Request failed')


    """ Gets a specific team's roster """

    def getRoster(self, userName, passw, position = 'QB'):
        try:
            response = requests.get(
                url="https://api.mysportsfeeds.com/v1.2/pull/nfl/2018-regular/roster_players.json?",
                params={ 
                    'team' : self.getName(),
                    'position' : position 
                },
                headers={
                    "Authorization": "Basic " + base64.b64encode('{}:{}'.format(userName,passw).encode('utf-8')).decode('ascii')
                }
            )
            data = response.json()
            positionPrint = position + ":" + " " * (4 - len(position))
            for i in range(0, len(data['rosterplayers']['playerentry'])):
                positionPrint += (data['rosterplayers']['playerentry'][i]['player']['FirstName']) + ' '  +\
                 (data['rosterplayers']['playerentry'][i]['player']['LastName'] + ' ')
            print(positionPrint)
            self.count = self.count + 1
            if (self.count < 14):
                try:
                    self.getRoster(userName, passw, self.positions[self.count])
                except:
                    self.count = self.count + 1


        except requests.exceptions.RequestException:
            print('HTTP Request failed')