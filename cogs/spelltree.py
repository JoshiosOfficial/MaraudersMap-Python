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
            embed = self.client.NOT_FOUND_EMBED.copy()
            embed.description = embed.description.format(username=username)
            await ctx.send(embed=embed)
            return

        response = await self.client.session.get(f"https://api.potterworldmc.com/player/{username}")
        data = await response.json()

        if data['status'] == False:
            embed = self.client.NOT_FOUND_EMBED.copy()
            embed.description = embed.description.format(username=username)
            await ctx.send(embed=embed)
            return

        player = data["player"]

        spelltrees = {
            'charms': [],
            'jinxes': [],
            'curses': [],
            'transfiguration': [],
            'defensive': [],
        }

        for unlockable in player['unlockables']:
            if "spelltrees_charms" in unlockable:
                spell = self.spell_to_readable(unlockable[18:])
                spelltrees['charms'].append(spell)

            elif "spelltrees_jinxes" in unlockable:
                spell = self.spell_to_readable(unlockable[18:])
                spelltrees['jinxes'].append(spell)

            elif "spelltrees_curses" in unlockable:
                spell = self.spell_to_readable(unlockable[18:])
                spelltrees['curses'].append(spell)

            elif "spelltrees_transfiguration" in unlockable:
                spell = self.spell_to_readable(unlockable[27:])
                spelltrees['transfiguration'].append(spell)

            elif "spelltrees_defensive" in unlockable:
                spell = self.spell_to_readable(unlockable[21:])
                spelltrees['defensive'].append(spell)

        description = []
        for spelltree in spelltrees:
            emote = self.client.emotes[spelltree.upper()]
            spells = "\n".join(spelltrees[spelltree]) if len(spelltrees[spelltree]) != 0 else 'None'
            description.append(f"{emote} **{spelltree.capitalize()}**:\n {spells}\n")

        embed = discord.Embed(
            description = "\n".join(description),
            color = self.client.house_colors[player["house"].lower()] if player["house"] else self.client.main_color,
        )
        embed.set_footer(text = f"Last updated: {humanize.naturaltime(datetime.datetime.now() - datetime.datetime.fromtimestamp(player['updated']))}")
        embed.set_author(name = f"{player['username'] if player['username'] else username}", icon_url = f"https://minotar.net/helm/{player['uuid']}.png")

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Spelltree(client))
