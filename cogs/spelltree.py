import discord
from discord.ext import commands

import aiohttp
import datetime
import humanize

class Spelltree(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.data = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.spells_response = await self.client.session.get(f"https://api.potterworldmc.com/spells")
        self.spells = await self.spells_response.json()

    def spell_to_readable(self, spell):
        if (spell == "protegototalum"): 
            return 'Protellum'

        if (spell == "antiapparate"):
            return 'Anti-Appareo'

        for x in self.spells['spells']:
          if x['key'] == spell:
              return x['name']

    @commands.command()
    async def spelltree(self, ctx, username=None):

        if not username:
            embed = discord.Embed(
                description = f"The player `{username}` was not found. This means that this player never joined Potterworld before, or you incorrectly spelled their username. Please try again.",
                title = "Player Not Found",
                color = self.client.main_color
            )
            await ctx.send(embed=embed)
            return

        response = await self.client.session.get(f"https://api.potterworldmc.com/player/{username}")
        data = await response.json()

        if data['status'] == False:
            embed = discord.Embed(
                description = f"The player `{username}` was not found. This means that this player never joined Potterworld before, or you incorrectly spelled their username. Please try again.",
                title = "Player Not Found",
                color = self.client.main_color
            )
            await ctx.send(embed=embed)
            return

        nl = "\n"
        player = data["player"]

        charms = [item for item in player["unlockables"] if "spelltrees_charms" in item]
        curses = [item for item in player["unlockables"] if "spelltrees_curses" in item]
        jinxes = [item for item in player["unlockables"] if "spelltrees_jinxes" in item]
        defensive = [item for item in player["unlockables"] if "spelltrees_defensive" in item]
        transfiguration = [item for item in player["unlockables"] if "spelltrees_transfiguration" in item]

        charms = [self.spell_to_readable(e[18:]) for e in charms]
        curses = [self.spell_to_readable(e[18:]) for e in curses]
        jinxes = [self.spell_to_readable(e[18:]) for e in jinxes]
        defensive = [self.spell_to_readable(e[21:]) for e in defensive]
        transfiguration = [self.spell_to_readable(e[27:]) for e in transfiguration]

        embed = discord.Embed(
            description = (
                f"<:charms:742480444855025775> **Charms**:\n {nl.join(charms) if len(charms) != 0 else 'None'}\n\n"
                f"<:jinxes:742481106711871619> **Jinxes**:\n {nl.join(jinxes) if len(jinxes) != 0 else 'None'}\n\n"
                f"<:curses:742481337784598608> **Curses**:\n {nl.join(curses) if len(curses) != 0 else 'None'}\n\n"
                f"<:transfiguration:742481688080416870> **Transfiguration**:\n {nl.join(transfiguration) if len(transfiguration) != 0 else 'None'}\n\n"
                f"<:defensive:742481924387242004> **Defensive**:\n {nl.join(defensive) if len(defensive) != 0 else 'None'}\n\n"
            ),
            color = self.client.house_colors[data["player"]["house"].lower()] if data["player"]["house"] else self.client.main_color,
        )
        embed.set_footer(text = f"Last updated: {humanize.naturaltime(datetime.datetime.now() - datetime.datetime.fromtimestamp(player['updated']))}")
        embed.set_author(name = f"{player['username'] if player['username'] else username}", icon_url = f"https://minotar.net/helm/{player['uuid']}.png")

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Spelltree(client))
