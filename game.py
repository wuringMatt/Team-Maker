#imports

import discord
import json
import asyncio


#variables

message = ""

embed = discord.Embed(title="L4D2 Game", color = 0x0000FF)

#load and save data

with open("data.json", "r") as f:
    data = json.load(f)


def save(data):
    with open("data.json", "w") as f:
        data = json.dump(data, f, indent=2)


#function for /play (when, players) command

async def play(ctx, when, players):
    global message
    global embed

    message = await ctx.respond(embed = embed)

async def edit(ctx):
    global message

    newembed = discord.Embed(title="L4D2 Game", color = 0xFF0000)
    await message.followup.edit_message(message.id, embed=newembed)
