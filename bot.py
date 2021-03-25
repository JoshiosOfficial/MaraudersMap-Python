import discord
import os

from discord.ext import commands
from datetime import datetime
from dotenv import load_dotenv,find_dotenv

import aiohttp
import json

load_dotenv(find_dotenv())

prefix = os.getenv('PREFIX')
client = commands.Bot(command_prefix = prefix, intents = discord.Intents.all(), case_insensitive = True)

with open('locations.json') as f:
  client.locations = json.load(f)

with open('emotes.json', encoding="utf8") as f:
  client.emotes = json.load(f)

client.house_colors = {
    "griffin": 0xD92C2C,
    "raven": 0x0099E1,
    "serpent": 0x25A225,
    "honeybadger": 0xF1C40F,
}

client.main_color = 0xA62019

client.NOT_FOUND_EMBED = discord.Embed(
    description = "The player `{username}` was not found. This means that this player never joined Potterworld before, or you incorrectly spelled their username. Please try again.",
    title = "Player Not Found",
    color = client.main_color
)

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

token = os.getenv('DISCORD_TOKEN')
client.run(token) # MARAUDER MAP ALPHA
