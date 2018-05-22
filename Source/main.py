#Project goals: 
# - User can input a team name -> access the API and return the team's schedule with the result of each game (2017)
#    - #Get schedule for upcoming 2018 season 
# - If the user asks to get all team names, print the city with name for all teams - make them then select one 

#Future: 
# - User can select a team and then get a variety of data about the team including roster etc, not just the schedule (for a variety of years)
# - Eventually the ability to search for a specific player to get their stats 
# - :)


import team as team
import base64
import requests

def printWelcome():
    print("############ Welcome to the NFL Statistic Book ############ \n\n")
    print("(1) Search for a specific team")
    print("(2) Get a list of teams to choose from")
    return getFirstSelection()

def getFirstSelection():

    selection = input("\nSelection: ")
    return selection

def execInput(selection):
    if (selection == '1'):
        teamName = input("\nPlease enter team name or city: ")
        t = team.Team(teamName)
        api_test()
        #Search the api for the team, determine if it is real, if it is not real, make the user enter another team name 

    elif (selection == '2'):
        print("Team names are:")
        #get team names 
    else:
        execInput(getFirstSelection())

def api_test():
    apiUrl = "https://api.mysportsfeeds.com/v1.2/pull/nfl/2018-regular/full_game_schedule.json"
    response = requests.get(apiUrl)
    print(response.status_code)




####### Main #######

selection = printWelcome()  
execInput(selection)  