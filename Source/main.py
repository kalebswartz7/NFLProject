#Next Steps: 
# - Get roster in a formatted kind of way 
# - View players stats 


from team import Team
import base64
import requests
import os
import sys

""" Gets username and password as credentials to acccess the API - Hidden ;) """

def getCredentials():
    with open('secret.txt') as f:
        lines = f.readlines()
        return lines


userName = getCredentials()[0].strip()
passw = getCredentials()[1].strip()
allTeams = {}
createdTeam = "Bengals"


""" Accesses the API to get a team (City + Name) and pairs that with the team's abbreviation in a dictionary as the JSON URL's use the 
    team's abbreviations """

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


"""" This is what is first printed / asked when the program starts. This function gets called repeatedly however to give the user
     more options after the data they want is already found. """ 

def printWelcome(opening = True, currentTeam = False):
    if (opening):
        print("############ Welcome to the NFL Statistic Book ############ \n\n")
    if (currentTeam == True):
        print("(0) Stay with current team")

    print("(1) Search for a specific team")
    print("(2) Get a list of teams to choose from")
    print("(3) Quit")
    return getFirstSelection()


""" This method just gets the input from the user in printWelcome() """

def getFirstSelection():
    selection = input("\nSelection: ")
    return selection


""" This method takes the input from the user recieved in getFirstSelection() and decides what to do with that input depending on 
    what the user entered """

def execInput(selection, toClear = True, currentTeam = False):
    if (selection == '1'):
        if (toClear):
           clear()
           teamName = input("Please enter team name: ")
        else:
            teamName = input("\nPlease enter team name: ")
        if isTeam(teamName):
            global createdTeam
            createdTeam = teamName
            createTeam(getAbbreviation(teamName))
            
        else:
            execInput('1', False)

    elif (selection == '0' and currentTeam == True):
        print(createdTeam)
        if isTeam(createdTeam):
            createTeam(getAbbreviation(createdTeam))

    elif (selection == '2'):
        clear()
        print("Available teams: \n")
        printTeams()
        execInput('1', False)
    
    elif (selection == '3'):
        clear()
        sys.exit("Have a great day")


    else:
        execInput(getFirstSelection())


""" Creates a Team with a team's corresponding abbreviation for easy access in the API """

def createTeam(teamAbbreviation):
    t = Team(teamAbbreviation)
    getTeamOptions(t)


""" Clears window """

def clear():
    os.system( 'clear' )


""" Prints all Teams from the dictionary available to choose in the program """

def printTeams():
    count = 0
    teamString = ""
    for key in allTeams:
        count = count + 1
        teamString += key + " " * (25 - len(key))
        if (count % 5 == 0):
            teamString += "\n"
    print(teamString)


""" Determines whether or not the user input a real team name / city """  

def isTeam(teamName):
    for key in allTeams:
        if teamName.lower() in key.lower() and len(teamName) >= 4:
            return True
    return False


""" Gets the abbreviation of a correspnding team name """ 

def getAbbreviation(teamName):
    for key in allTeams:
        if teamName.lower() in key.lower() and len(teamName) >= 4:
            return allTeams[key]


""" Once a user successfully selects a team, these new options are displayed """

def getTeamOptions(t):
    clear()
    print("TEAM SELECTED: " + t.getName() + "\n\n" + "(1) Get 2018-2019 Schedule\n(2) Get Roster\n(3) Choose another team ")
    selection = input("\n Selection: ")
    if (selection is '3'):
        clear()
        execInput(printWelcome(False))
    elif (selection is '1'):
        clear()
        t.getSchedule(userName, passw)
        execInput(printWelcome(False, True), True, True)
    elif (selection is '2'):
        clear()
        t.getRoster(userName, passw)
        print("\n")
        execInput(printWelcome(False, True), True, True)
    



""" Main """
generateTeams()
selection = printWelcome()  
execInput(selection)  

