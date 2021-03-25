import discord
from discord.ext import commands

import aiohttp
import datetime
import humanize

class Player(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(
        name = 'player',
        aliases = ['whois', 'p', 'profile'],
        brief = 'Provides Potterworld statistics about a player.'
    )
    @commands.has_role('Bug Tester')
    async def player(self, ctx, username=None):

        if not username or len(username) > 24:
            embed = self.client.NOT_FOUND_EMBED.copy()
            embed.description = embed.description.format(username=(username if username and len(username) <= 24 else None))
            await ctx.send(embed=embed)
            return

        response = await self.client.session.get(f"https://api.potterworldmc.com/player/{username.replace('/', '')}")
        data = await response.json()

        if data['status'] == False:
            embed = self.client.NOT_FOUND_EMBED.copy()
            embed.description = embed.description.format(username=username)
            await ctx.send(embed=embed)
            return

        player = data["player"]

        embed = discord.Embed(
            description = (
                f"**Basic Information**:\n"
                f"{self.client.emotes['USERNAME']} Username: {player['username'] if player['username'] else username}\n"
                f"{self.client.emotes['NICKNAME']} Nickname: {player['nickname'] if player['nickname'] else 'None'}\n"
                f"{self.client.emotes[player['house'].upper()] if player['house'] else '🏠'} House: {player['house'].lower().capitalize() if player['house'] else 'Unsorted'}\n"
                f"{self.client.emotes['JOIN_DATE']} Join Date: {datetime.datetime.fromtimestamp(player['joined']).strftime('%B %d, %Y') if 'joined' in player and player['joined'] > 0 else 'Unknown'}\n\n"
                f"**Progression**:\n"
                f"{self.client.emotes['YEAR']} Year: {player['year'] if player['year'] else 'Year 1'} (Level {player['stats']['experience']['level'] if (player['stats']) and ('experience' in player['stats']) else '1'})\n"
                f"{self.client.emotes['SPELLS']} Spells: {len(player['spells']) if player['spells'] else '0'}\n"
                f"{self.client.emotes['CLASSES_ATTENDED']} Classes Attended: {player['stats']['classes_attended']['balance'] if (player['stats']) and ('classes_attended' in player['stats']) else '0'}\n"
                f"{self.client.emotes['LOCATIONS_EXPLORED']} Locations Explored: {len([match for match in player['unlockables'] if 'world_discovery_' in match] if 'unlockables' in player else '0')}\n\n"
                f"{'This player is a **staff member**.' if 'staff' in player else ''}"
            ),
            color = self.client.house_colors[player["house"].lower()] if player["house"] else self.client.main_color,
        )

        player_link = f"https://potterworldmc.com/player/{player['username'] if player['username'] else username}"

        embed.set_footer(text = f"Last updated: {humanize.naturaltime(datetime.datetime.now() - datetime.datetime.fromtimestamp(player['updated']))}")
        embed.set_author(name = f"{player['username'] if player['username'] else username}", icon_url = f"https://minotar.net/helm/{player['uuid']}.png", url = player_link)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Player(client))
