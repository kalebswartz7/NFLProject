#Project goals: 
# - User can input a team name -> access the API and return the team's schedule with the result of each game (2017)
#    - #Get schedule for upcoming 2018 season 
# - If the user asks to get all team names, print the city with name for all teams - make them then select one 

#Future: 
# - User can select a team and then get a variety of data about the team including roster etc, not just the schedule (for a variety of years)
# - Eventually the ability to search for a specific player to get their stats 
# - :)


from team import Team
import base64
import requests
import os

def getCredentials():
    with open('secret.txt') as f:
        lines = f.readlines()
        return lines


userName = getCredentials()[0].strip()
passw = getCredentials()[1].strip()
allTeams = {}

def generateTeams():
    try:
        response = requests.get(
            url="https://api.mysportsfeeds.com/v1.2/pull/nfl/2018-regular/conference_team_standings.json?teamstats=W,L,T,PF,PA",
            params={
            },
            headers={
                "Authorization": "Basic " + base64.b64encode('{}:{}'.format(userName,passw).encode('utf-8')).decode('ascii')
            }
        )
        data = response.json()
        for j in range(0, 2):
            for i in range(0, 16):
                team = (data['conferenceteamstandings']['conference'][j]['teamentry'][i]['team']['City']) + " "
                team += (data['conferenceteamstandings']['conference'][j]['teamentry'][i]['team']['Name'])
                abbreviation = (data['conferenceteamstandings']['conference'][j]['teamentry'][i]['team']['Abbreviation'])
                allTeams[team] = abbreviation
        
    except requests.exceptions.RequestException:
        print('HTTP Request failed')


def printWelcome(opening = True):
    if (opening):
        print("############ Welcome to the NFL Statistic Book ############ \n\n")
    if (opening == False):
        clear()
    print("(1) Search for a specific team")
    print("(2) Get a list of teams to choose from")
    return getFirstSelection()

def getFirstSelection():
    selection = input("\nSelection: ")
    return selection


def execInput(selection, toClear = True):
    if (selection == '1'):
        if (toClear):
           clear()
           teamName = input("Please enter team name: ")
        else:
            teamName = input("\nPlease enter team name: ")
        if isTeam(teamName):
            createTeam(getAbbreviation(teamName))
        else:
            execInput('1', False)
        #Search the api for the team, determine if it is real, if it is not real, make the user enter another team name 

    elif (selection == '2'):
        clear()
        print("Available teams: \n")
        printTeams()
        execInput('1', False)

        #get team names 
    else:
        execInput(getFirstSelection())

def createTeam(teamAbbreviation):
    t = Team(teamAbbreviation)
    getTeamOptions(t)

def clear():
    os.system( 'clear' )

def printTeams():
    count = 0
    teamString = ""
    for key in allTeams:
        count = count + 1
        teamString += key + " " * (25 - len(key))
        if (count % 5 == 0):
            teamString += "\n"
    print(teamString)

def isTeam(teamName):
    for key in allTeams:
        if teamName.lower() in key.lower() and len(teamName) >= 4:
            return True
    return False

def getAbbreviation(teamName):
    for key in allTeams:
        if teamName.lower() in key.lower() and len(teamName) >= 4:
            return allTeams[key]

def getTeamOptions(t):
    clear()
    print("TEAM SELECTED: " + t.getName() + "\n\n" + "(1) Get 2018-2019 Schedule \n(2) Choose another team")
    selection = input("\nSelection: ")
    if (selection is '2'):
        execInput(printWelcome(False))
    elif (selection is '1'):
        clear()
        t.getSchedule(userName, passw)




####### Main #######
generateTeams()
selection = printWelcome()  
execInput(selection)  

