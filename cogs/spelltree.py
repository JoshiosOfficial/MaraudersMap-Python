import discord
from discord.ext import commands

import aiohttp
import datetime
import humanize

class Spelltree(commands.Cog):

    def __init__(self, client):
        self.client = client

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

        embed = discord.Embed(
            description = (
                f"Charms\n {nl.join(charms) if len(charms) != 0 else 'None'}\n\n"
                f"Jinxes\n {nl.join(jinxes) if len(jinxes) != 0 else 'None'}\n\n"
                f"Curses\n {nl.join(curses) if len(curses) != 0 else 'None'}\n\n"
                f"Transfiguration\n {nl.join(transfiguration) if len(transfiguration) != 0 else 'None'}\n\n"
                f"Defensive\n {nl.join(defensive) if len(defensive) != 0 else 'None'}\n\n"
            ),
            color = self.client.house_colors[data["player"]["house"].lower()] if data["player"]["house"] else self.client.main_color,
        )
        embed.set_footer(text = f"Last updated: {humanize.naturaltime(datetime.datetime.now() - datetime.datetime.fromtimestamp(player['updated']))}")
        embed.set_author(name = f"{player['username'] if player['username'] else username}", icon_url = f"https://minotar.net/helm/{player['uuid']}.png")

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Spelltree(client))
