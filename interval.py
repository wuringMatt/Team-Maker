#Imports

import sched, time
import requests
import json
import os


#varaibles

SIlist = []
s = sched.scheduler(time.time, time.sleep)
steamApiKey = os.environ.get("STEAM_API_KEY")


#load data of users

with open("data.json") as f:
    data = json.load(f)


#save function for the data

def save(data):
    with open("data.json", "w") as f:
        data = json.dump(data, f, indent=2)


#function for updating the Steam Id list (gets called in loop)

def steamListUpdate():
    global SIlist
    SIlist = []
    for u in data["users"]:
        if u["steamId"] != None:
            SIlist.append(u["steamId"])


#fucntion for getting the stats from the collected steam data (returns dict)

def getStats(data):
    stats = {
        "Lost": 0,
        "Won": 0,
        "Played": 0
    }

    for s in data["playerstats"]["stats"]:
        if s["name"] == "Stat.GamesLost.Versus":
            stats["Lost"] = s["value"]
        elif s["name"] == "Stat.GamesWon.Versus":
            stats["Won"] = s["value"]
        elif s["name"] == "Stat.GamesPlayed.Versus":
            stats["Played"] = s["value"]

    return stats


#gets the data from steam (returns list with data)

def getSteamData():
    global SIlist
    playerList = []

    for Id in SIlist:
        try:
            playerData = requests.get(f"http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v2/?appid=550&key={steamApiKey}&steamid={Id}")
            playerList.append([Id, getStats(playerData.json())])
        except:
            playerList.append([Id, "error"])

    return playerList


# saves player data in the data.json file

def savePlayerData(playerList):
    global data
    for u in data["users"]:
        for s in playerList:
            if u["steamId"] == s[0]:
                if s[1] != 'error':
                    u["gameStats"]["gamesLost"] = s[1]["Lost"]
                    u["gameStats"]["gamesWon"] = s[1]["Won"]
                    u["gameStats"]["gamesTotal"] = s[1]["Played"]
                else:
                    print(s)            
    save(data)
    return


#Interval loop for keeping player stats up to date

def do_something(sc): 
    steamListUpdate()
    playerList = getSteamData()
    savePlayerData(playerList)

    sc.enter(10, 1, do_something, (sc,))


#start the loop

s.enter(10, 1, do_something, (s,))
s.run()