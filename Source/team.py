import base64
import requests
import json


class Team:

    def __init__(self, name):
        """
        Team Constructor

        Parameters
        ----------
        name : string
            abbreviation of the team

        Notes
        -----
        roster_count is due to get_roster method being recursive, keeps track
        of how many players have been added to the team's roster when displayed

        """
        self.name = name
        self.positions = ['QB', 'RB', 'WR', 'TE', 'C', 'G',
                          'OT', 'LB', 'CB', 'DB', 'DE', 'SS', 'DT', 'K']
        self.roster_count = 0


    def get_name(self):
        """
        Returns the team name (abbreviation)

        """
        return self.name


    def get_schedule(self, user_name, passw):
        """
        Gets a specific team's upcoming schedule

        Parameters
        ---------
        user_name :  string
            user name for accessing API
        passw : stirng
            password for accessing API

        """
        try:
            response = requests.get(
                url='https://api.mysportsfeeds.com/v1.2/pull/nfl/2018-regular'
                    '/full_game_schedule.json?',
                params={
                    'team' : self.get_name()
                },
                headers={
                    'Authorization': 'Basic ' + base64.b64encode
                    ('{}:{}'.format(user_name,passw).encode('utf-8')).decode('ascii')
                }
            )
            data = response.json()
            print(' 2018 Schedule: \n')
            for i in range(0, 16):
                date = data['fullgameschedule']['gameentry'][i]['date']
                awayTeam = data['fullgameschedule']['gameentry'][i]['awayTeam']['City'] \
                + ' '  + data['fullgameschedule']['gameentry'][i]['awayTeam']['Name']
                homeTeam = data['fullgameschedule']['gameentry'][i]['homeTeam']['City'] \
                + ' '  + data['fullgameschedule']['gameentry'][i]['homeTeam']['Name']
                time = data['fullgameschedule']['gameentry'][i]['time']
                gameData = (' ' + date + ' ' * 10 + awayTeam + ' @ ' + homeTeam)
                dataLength = len(gameData)
                spaces = 80 - dataLength
                print( gameData + ' ' * spaces + time)
            print('\n')
        
        except requests.exceptions.RequestException:
            print('HTTP Request failed')


    def get_roster(self, user_name, passw, position='QB'):
        """
        Gets a specific teams roster for the upcoming season

        Parameters
        ----------
        user_name : string
            user name for accessing API
        passw : string
            password for accessing API
        position : string
            position of players being grabbed for that iteration of method

        """
        try:
            response = requests.get(
                url='https://api.mysportsfeeds.com/v1.2/pull/nfl/2018-regular'
                    '/roster_players.json?',
                params={ 
                    'team' : self.get_name(),
                    'position' : position 
                },
                headers={
                    'Authorization': 'Basic ' + base64.b64encode
                    ('{}:{}'.format(user_name,passw).encode('utf-8')).decode('ascii')
                }
            )
            data = response.json()
            positionPrint = position + ':' + ' ' * (4 - len(position))
            for i in range(0, len(data['rosterplayers']['playerentry'])):
                positionPrint += (data['rosterplayers']['playerentry'][i]['player']['FirstName']) + ' '  +\
                 (data['rosterplayers']['playerentry'][i]['player']['LastName'] + ' ')
            print(positionPrint)
            self.roster_count += 1
            if (self.roster_count < 14):
                try:
                    self.get_roster(user_name, passw, self.positions[self.roster_count])
                except:
                    self.roster_count = self.roster_count + 1


        except requests.exceptions.RequestException:
            print('HTTP Request failed')