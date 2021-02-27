import discord
import os

from discord.ext import commands
from datetime import datetime

import aiohttp

client = commands.Bot(command_prefix = '?', intents = discord.Intents.all(), case_insensitive = True)

client.house_colors = {
    "griffin": 0xD92C2C,
    "raven": 0x0099E1,
    "serpent": 0x25A225,
    "honeybadger": 0xF1C40F,
}

client.main_color = 0xA62019

client.house_emojis = {
    "griffin": "<:griffin:742100884707606608>",
    "raven": "<:raven:742100700439248936>",
    "serpent": "<:serpent:742101009995661344>",
    "honeybadger": "<:honeybadger:742101128589606993>"
}

client.status_emojis = {
    "dnd": "<:dnd:763148593569333268>",
    "online": "<:online:763148147295518790>",
    "idle": "<:idle:763148634556071967>",
    "offline": "<:offline:763147752002682900>"
}

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    client.session = aiohttp.ClientSession()

@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"Successfully loaded `{extension}` cog!")

@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    await ctx.send(f"Successfully unloaded `{extension}` cog!")

@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    client.load_extension(f"cogs.{extension}")
    await ctx.send(f"Successfully reloaded `{extension}` cog!")

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f"cogs.{filename[:-3]}")


client.run('NzU3MzQwNDc1MzQ1NzMxNzY1.X2e-SA.x8Yr1lA5yHZBUngg0coX119mZd0') # MARAUDER MAP ALPHA
#client.run('NzQyMDY1MzQzOTYyNTQ2MTk4.XzAsNA.9f6VBiLuU_OuElcmoCIMW53WZbw') MARAUDER MAP