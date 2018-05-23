import base64
import requests
import json

class Team: 
    name = ""

    def __init__(self, name):
        self.name = name

    def getName(self):
        return self.name

    def get_team_info(self, userName, passw):
        try:
            response = requests.get(
                url="https://api.mysportsfeeds.com/v1.2/pull/nfl/2018-regular/full_game_schedule.json?team=CIN",
                params={
                #"Abbreviation": "CIN"
                },
                headers={
                    "Authorization": "Basic " + base64.b64encode('{}:{}'.format(userName,passw).encode('utf-8')).decode('ascii')
                }
            )
            data = response.json()
            print(data['fullgameschedule']['gameentry'][0]['awayTeam'])
        
        except requests.exceptions.RequestException:
            print('HTTP Request failed')
    #send_request()
