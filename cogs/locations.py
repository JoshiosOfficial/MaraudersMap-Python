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

        if not username or len(username) > 24:
            embed = self.client.NOT_FOUND_EMBED.copy()
            embed.description = embed.description.format(username=(username if len(username) <= 24 else None))
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

        locs = {
            'locations': [],
            'warpkey_bag_list': [],
            'warpkey_bag_list2': [],
            'world_fasttravel': [],
        }

        if 'unlockables' in player:
            for unlockable in player['unlockables']:
                if 'world_discovery_' in unlockable:
                    locs["locations"].append(unlockable)

                elif 'world_warpkey2' in unlockable and unlockable != 'world_warpkey2_unlock':
                    locs["warpkey_bag_list2"].append(unlockable)

                elif 'world_warpkey' in unlockable:
                    locs["warpkey_bag_list"].append(unlockable)

                elif 'world_fasttravel_' in unlockable:
                    locs["world_fasttravel"].append(unlockable)

        warpkey_bag = self.client.locations[locs['warpkey_bag_list'][0][14:]] if len(locs['warpkey_bag_list']) > 0 else "Unknown"
        warpkey_bag2 = self.client.locations[locs['warpkey_bag_list2'][0][15:]] if len(locs['warpkey_bag_list2']) > 0 else "Unknown"

        description = [
            f"**Locations Explored**: {len(locs['locations'])}/21\n"
            f"**Hogsworth Fast Travel**: {len(locs['world_fasttravel'])}/19\n"
            f"**Warp Point**: {warpkey_bag}\n"
            f"**Warp Point #2**: {warpkey_bag2}\n"
        ]

        for location in self.client.locations:
            id = "world_discovery_" + location

            emote = self.client.emotes["YES" if id in locs['locations'] else "NO"]
            description.append(f"{emote} {self.client.locations[location]}")

        embed = discord.Embed(
            description = "\n".join(description),
            color = self.client.house_colors[player["house"].lower()] if player["house"] else self.client.main_color,
        )
        embed.set_footer(text = f"Last updated: {humanize.naturaltime(datetime.datetime.now() - datetime.datetime.fromtimestamp(player['updated']))}")
        embed.set_author(name = f"{player['username'] if player['username'] else username}", icon_url = f"https://minotar.net/helm/{player['uuid']}.png")

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Locations(client))
