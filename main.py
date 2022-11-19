#imports

import discord
from discord.ext import commands
import functions
import os


#variables

bot = commands.Bot(intents=discord.Intents.all(), command_prefix='TM ')
bot.remove_command('help')
botToken = os.environ.get("BOT_TOKEN")


#slash commands

@bot.slash_command(
    name="create",
    description="create your account, possible regions: NA, SA, EU, AF, AS, OC"
)
async def create(ctx: discord.ApplicationContext):
    await functions.create(ctx)


@bot.slash_command(name="play", description="start a game of l4d2 versus")
async def play(ctx: discord.ApplicationContext, when: str, players: int):
    await functions.play(ctx, when, players)

@bot.slash_command(
    name="link",
    description="Link your steam account"
)
async def link(ctx: discord.ApplicationContext, steamid: str):
    await functions.link(ctx, steamid)


#regular commmands

@bot.command()
async def info(ctx, person):
    await functions.TMinfo(ctx, person)


@bot.command()
async def delete(ctx, p1):
    await functions.delete(ctx, p1)


@bot.command()
async def dislikes(ctx, arg1, arg2):
    await functions.dislikes(ctx, arg1, arg2)


@bot.command()
async def like(ctx, p1, p2):
    await functions.like(ctx, p1, p2)


@bot.command()
async def ban(ctx, person1, person2):
    await functions.ban(ctx, person1, person2)


@bot.command()
async def unban(ctx, person1, person2):
    await functions.unban(ctx, person1, person2)


@bot.command()
async def skill(ctx, person, level):
    await functions.skill(ctx, person, level)


@bot.command()
async def create(ctx, id, name, skill):
    await functions.TMcreate(ctx, id, name, skill)


@bot.command()
async def trust(ctx, p):
    await functions.trust(ctx,p)


@bot.command()
async def untrust(ctx, p):
    await functions.untrust(ctx, p)


#run the bot

bot.run(str(botToken))