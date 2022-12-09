#imports

import discord
import json


#variables



#load and save data

with open("data.json", "r") as f:
    data = json.load(f)


def save(data):
    with open("data.json", "w") as f:
        data = json.dump(data, f, indent=2)


#get user from data.json using user input

def getUser(p):
    global data

    for u in data["users"]:
        if u["id"] == str(p):
            return u
        elif u["name"] == p:
            return u
    else:
        return False


#check for 2 players to see if they exist

def player_check(p1, p2):
    if p1 == False and p2 == False:
        embed = discord.Embed(title="Both players don't exist", color=0xFF0000)        
        return embed
    elif p1 == False:
        embed = discord.Embed(title="Player 1 doesn't exist", color=0xFF0000) 
        return embed
    elif p2 == False:
        embed = discord.Embed(title="Player 2 doesn't exist", color=0xFF0000) 
        return embed
    elif p1 == p2:
        embed = discord.Embed(title="That aint working like that", color=0xFF0000)
        return embed


#function for checking trusted commands

def trusted(ctx):
    for u in data["users"]:
        if u["id"] == ctx.author.id and u["trusted"] == True:
            return True
    else:
        return False


#function for /create command
#saves new player to data.json

def create(ctx):
    global data

    for u in data["users"]:
        if u["id"] == f"{ctx.author.id}":
            embed = discord.Embed(title="You already have an account",
                                  description="",
                                  color=0xFF0000)

            return ctx.respond(embed=embed)

    data["users"].append({
        "id": f"{ctx.author.id}",
        "steamId": None,
        "name": f'{ctx.author}',
        "skill": 5,
        "dislikes": [],
        "banned": [],
        "trusted": False,
        "gameStats": {
            "gamesWon": 0,
            "gamesLost": 0,
            "gamesTotal": 0
        }
    })

    save(data)
    print("player has been made: " + data["users"][id])

    embed = discord.Embed(
        title="Thanks for making an account, you can join the games now",
        description="",
        color=0x00FF00)

    return ctx.respond(embed=embed)


#Function for TM info (p) command
#gives information about player

def TMinfo(ctx, p):
    global data

    if trusted(ctx) == False:
            embed = discord.Embed(title="You aren't authorized to use this command",
                                  description="",
                                  color=0xFF0000)
            return ctx.send(embed=embed)

    person = getUser(p)
    nl = '\n'

    if person == False:
        embed = discord.Embed(title="This person doesn't exist",
                              description="",
                              color=0xFF0000)
        return ctx.send(embed=embed)

    embed = discord.Embed(title=f'{person["name"]}',
                          description="",
                          color=0x0000FF)

    embed.add_field(name="Skill Level:",
                    value=f'{person["skill"]}',
                    inline=False)

    if person["trusted"] == True:
        trust = "Yes"
    else:
        trust = "No"

    embed.add_field(name="Trusted?",
                    value=trust,
                    inline=False)

    embed.add_field(name="Dislikes:",
                    value=f'{nl.join(person["dislikes"])}' or "none",
                    inline=True)

    embed.add_field(name="Banned:",
                    value=f'{nl.join(person["banned"])}' or "none",
                    inline=True)

    return ctx.send(embed=embed)


#function for TM dislike (p1, p2) command
#adds p2 to p1's dislike list in data.json

def dislikes(ctx, p1, p2):
    global data

    if trusted(ctx) == False:
            embed = discord.Embed(title="You aren't authorized to use this command",
                                  description="",
                                  color=0xFF0000)
            return ctx.send(embed=embed)    

    p1 = getUser(p1)
    p2 = getUser(p2)

    embed = player_check(p1, p2)
    if embed != None:
        return ctx.send(embed=embed)

    for p in p1["dislikes"]:
        if p == p2["name"]:
            embed = discord.Embed(title="Player 1 already dislikes Player 2", color=0xFF0000) 
            return ctx.send(embed = embed)
    else:
        p1["dislikes"].append(p2["name"])
        save(data)
        embed = discord.Embed(title="Player 1 dislikes Player 2", color=0x00FF00) 
        return ctx.send(embed = embed)


#function for TM like (p1, p2) command
#removes p2 from p1's dislike list in data.json

def like(ctx, p1, p2):
    global data

    if trusted(ctx) == False:
            embed = discord.Embed(title="You aren't authorized to use this command",
                                  description="",
                                  color=0xFF0000)
            return ctx.send(embed=embed)

    p1 = getUser(p1)
    p2 = getUser(p2)

    embed = player_check(p1, p2)

    if embed != None:
        return ctx.send(embed=embed)

    for p in p1["dislikes"]:
        if p == p2["name"]:
            p1["dislikes"].remove(p2["name"])
            save(data)
            embed = discord.Embed(title="Player 1 likes Player 2 again", color=0x00FF00) 
            return ctx.send(embed = embed)

    for u in data["users"]:
        if u == p2:
            embed = discord.Embed(title="Player 1 doesn't dislike Player 2", color=0xFF0000) 
            return ctx.send(embed=embed)


#function for TM skill (p, l) command
#set the skill of p in data.json

def skill(ctx, p, l):
    global data

    if trusted(ctx) == False:
            embed = discord.Embed(title="You aren't authorized to use this command",
                                  description="",
                                  color=0xFF0000)
            return ctx.send(embed=embed)

    p = getUser(p)

    l = int(l)

    if l < 1 or l > 10:
        return ctx.send(
            "you cant assign a skill level lower than 1 or higher than 10")

    for u in data["users"]:
        if u == p:
            p["skill"] = l
            save(data)
            return ctx.send(f"player skill set to {l}")
    else:
        return ctx.send("that person doesn't exist")


#function for TM ban (p1, p2) command
#adds p1 to p2's banned list and p2 to p1's banned list in data.json

def ban(ctx, p1, p2):
    global data

    if trusted(ctx) == False:
            embed = discord.Embed(title="You aren't authorized to use this command",
                                  description="",
                                  color=0xFF0000)
            return ctx.send(embed=embed)

    p1 = getUser(p1)
    p2 = getUser(p2)

    embed = player_check(p1, p2)
    if embed != None:
        return ctx.send(embed=embed)
        
    for p in p1["banned"]:
        if p == p2["name"]:
            embed = discord.Embed(title="Player 1 and Player 2 are already banned", color=0xFF0000)
            return ctx.send(embed=embed)

    p1["banned"].append(p2["name"])
    p2["banned"].append(p1["name"])
    save(data)

    embed = discord.Embed(title="person1 and person2 wont be able to play together anymore", color=0x00FF00)
    return ctx.send(embed = embed)


#function for TM unban (p1, p2) command
#removes p1 from p2's banned list and p2 from p1's banned list in data.json

def unban(ctx, p1, p2):
    global data

    if trusted(ctx) == False:
            embed = discord.Embed(title="You aren't authorized to use this command",
                                  description="",
                                  color=0xFF0000)
            return ctx.send(embed=embed)

    p1 = getUser(p1)
    p2 = getUser(p2)

    embed = player_check(p1, p2)
    if embed != None:
        return ctx.send(embed=embed)

    for p in p1["banned"]:
        if p == p2["name"]:
            p1["banned"].remove(p2["name"])
            p2["banned"].remove(p1["name"])
            save(data)
            embed = discord.Embed(title="person1 and person2 will be able to play with each other again", color=0x00FF00)
            return ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="these people arent banned from each other", color=0xFF0000)
        return ctx.send(embed=embed)


#function for delete (p) command
#deletes p1's data from data.json

def delete(ctx, p1):

    if trusted(ctx) == False:
            embed = discord.Embed(title="You aren't authorized to use this command",
                                  description="",
                                  color=0xFF0000)
            return ctx.send(embed=embed)

    p1 = getUser(p1)

    if p1 == False:
        return ctx.send("this player doesnt exist")

    for u in data["users"]:
        if u == p1:
            data["users"].remove(p1)
            save(data)
            print("player has been deleted: " + str(u))
            return ctx.send("player has been deleted")


#function for TM create (id, name, skill) command
#creates an account in data.json 

def TMcreate(ctx, id, name, skill):
    global data

    if trusted(ctx) == False:
            embed = discord.Embed(title="You aren't authorized to use this command",
                                  description="",
                                  color=0xFF0000)
            return ctx.send(embed=embed)

    try: 
        skill = int(skill)
    except:
        ctx.send("skill needs to be a number between 1 and 10")

    if skill < 1 or skill > 10:
        return ctx.send("player cant have skill level lower than 1 or higher than 10")

    for u in data["users"]:
        if u["id"] == id:
            return ctx.send("id already exists")
        elif u["name"] == name:
            return ctx.send("name already exists") 
    else:
        data["users"].append({
            "id": id,
            "steamId": None,
            "name": name,
            "skill": skill,
            "dislikes": [],
            "banned": [],
            "trusted": False,
            "gameStats": {
                "gamesWon": 0,
                "gamesLost": 0,
                "gamesTotal": 0
            }
        })

        save(data)
        print("player has been made: " + str(data["users"][int(id)]))

        return ctx.send("player has been made")


#function for TM trust (p) command
#Trusts p in data.json

def trust(ctx, p):
    global data

    if ctx.author.id != "342979399252967424":
            embed = discord.Embed(title="You aren't authorized to use this command",
                                  description="",
                                  color=0xFF0000)
            return ctx.send(embed=embed)

    p = getUser(p)

    if p == False:
        embed = discord.Embed(title="Player doesn't exist", color=0xFF0000)
        return ctx.send(embed=embed)
    
    if p["trusted"] == False:
        p["trusted"] = True
        save(data)
        embed = discord.Embed(title="Player is now trusted", color=0x00FF00)
        return ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Player is already trusted", color=0xFF0000)
        return ctx.send(embed=embed)


#function for TM untrust (p) command
#untrusts p in data.json 
 
def untrust(ctx, p):
    global data

    if ctx.author.id != "342979399252967424":
            embed = discord.Embed(title="You aren't authorized to use this command",
                                  description="",
                                  color=0xFF0000)
            return ctx.send(embed=embed)

    p = getUser(p)

    if p == False:
        embed = discord.Embed(title="Player doesn't exist", color=0xFF0000)
        return ctx.send(embed=embed)

    if p["trusted"] == True:
        p["trusted"] = False
        save(data)
        embed = discord.Embed(title="Player isn't trusted anymore", color=0x00FF00)
        return ctx.send(embed=embed)
    else:
        embed = discord.Embed(title="Player isn't trusted", color=0xFF0000)
        return ctx.send(embed=embed)


#function for /play (when, players) command UNFINISHED

def play(ctx, when, players):
    return ctx.respond("sup")


#function for /link (steamId) command UNFINISHED
#links steam id to author of command in data.json

def link(ctx, steamId):
    global data
    p = getUser(ctx.author.id)

    if p == False:
        return ctx.respond("please use /create first")
    
    if len(steamId) != 17:
        return ctx.respond("this is not a valid steam id")
    elif p["steamId"] == steamId:
        return ctx.respond("You've already linked this steam account")
    
    p["steamId"] = steamId
    save(data)
    return ctx.respond("steam account has been linked")
