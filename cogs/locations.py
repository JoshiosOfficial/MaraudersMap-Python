import discord
from discord.ext import commands

import aiohttp
import datetime
import humanize

class Locations(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def locations(self, ctx, username=None):

        if not username:
            embed = discord.Embed(
                description = f"The player `{username}` was not found. This means that this player never joined Potterworld before, or you incorrectly spelled their username. Please try again.",
                title = "Player Not Found",
                color = self.client.main_color
            )
            await ctx.send(embed=self.embed)
            return

        response = await self.client.session.get(f"https://api.potterworldmc.com/player/{username}")
        data = await response.json()

        if data['status'] == False:
            embed = discord.Embed(
                description = f"The player `{username}` was not found. This means that this player never joined Potterworld before, or you incorrectly spelled their username. Please try again.",
                title = "Player Not Found",
                color = self.client.main_color
            )
            await ctx.send(embed=self.embed)
            return

        player = data["player"]

        locations = [match for match in player['unlockables'] if 'world_discovery_' in match]
        warpkey_bag_list = [item for item in player["unlockables"] if "world_warpkey" in item]
        warpkey_bag = self.client.locations[warpkey_bag_list[0][14:]] if len(warpkey_bag_list) > 0 else "Unknown"

        warpkey_bag_list2 = [item for item in player["unlockables"] if "world_warpkey2" in item and item != "world_warpkey2_unlock"]
        warpkey_bag2 = self.client.locations[warpkey_bag_list2[0][15:]] if len(warpkey_bag_list2) > 0 else "Unknown"

        description = [
            f"**Locations Explored**: {len(locations) if player['unlockables'] else '0'}/21\n"
            f"**Hogsworth Fast Travel**: {len([match for match in player['unlockables'] if 'world_fasttravel_' in match] if player['unlockables'] else '0')}/19\n"
            f"**Warp Point**: {warpkey_bag}\n"
            f"**Warp Point #2**: {warpkey_bag2}\n"
        ]

        yes = self.client.emotes["YES"]
        no = self.client.emotes["NO"]

        for location in self.client.locations:
            id = "world_discovery_" + location
            description.append(f"{yes if id in locations else no} {self.client.locations[location]}")

        embed = discord.Embed(
            description = "\n".join(description),
            color = self.client.house_colors[player["house"].lower()] if player["house"] else self.client.main_color,
        )
        embed.set_footer(text = f"Last updated: {humanize.naturaltime(datetime.datetime.now() - datetime.datetime.fromtimestamp(player['updated']))}")
        embed.set_author(name = f"{player['username'] if player['username'] else username}", icon_url = f"https://minotar.net/helm/{player['uuid']}.png")

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Locations(client))
