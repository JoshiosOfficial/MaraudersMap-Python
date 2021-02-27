import discord
from discord.ext import commands

import aiohttp
import datetime
import humanize

class Player(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def player(self, ctx, username=None):

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
 
        player = data["player"]

        embed = discord.Embed(
            description = (
                f"**Basic Information test**:\n"
                f"<:username:742141709068271727> Username: {player['username'] if player['nickname'] else username}\n"
                f"💬 Nickname: {player['nickname'] if player['nickname'] else 'None'}\n"
                f"{self.client.house_emojis[player['house'].lower()] if player['house'] else '🏠'} House: {player['house'].lower().capitalize() if player['house'] else 'Unsorted'}\n"
                f"<:potterworld:742140640464470077> Join Date: {datetime.datetime.fromtimestamp(player['joined']).strftime('%B %d, %Y') if player['joined'] > 0 else 'Unknown'}\n\n"
                f"**Progression**:\n"
                f"🕒 Year: {player['year'] if player['year'] else 'Year 1'} (Level {player['stats']['experience']['level'] if (player['stats']) and ('experience' in player['stats']) else '1'})\n"
                f"<:spell:742140166138757199> Spells: {len(player['spells']) if player['spells'] else '0'}\n"
                f"📖 Classes Attended: {player['stats']['classes_attended']['balance'] if (player['stats']) and ('classes_attended' in player['stats']) else '0'}\n"
                f"🗺️ Locations Explored: {len([match for match in player['unlockables'] if 'world_discovery_' in match] if player['unlockables'] else '0')}\n\n"
                f"{'This player is a **staff member**.' if 'staff' in player else ''}"
            ),
            color = self.client.house_colors[data["player"]["house"].lower()] if data["player"]["house"] else self.client.main_color,
        )
        embed.set_footer(text = f"Last updated: {humanize.naturaltime(datetime.datetime.now() - datetime.datetime.fromtimestamp(player['updated']))}")
        embed.set_author(name = f"{player['username'] if player['username'] else username}", icon_url = f"https://minotar.net/helm/{player['username']}.png")

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Player(client))