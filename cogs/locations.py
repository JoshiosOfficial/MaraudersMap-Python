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

        warpkeybaglist = [item for item in player["unlockables"] if "world_warpkey" in item]
        if (len(warpkeybaglist) > 1):
            warpkeybag = warpkeybaglist[1]
        else:
            warpkeybag = warpkeybaglist[0]

        embed = discord.Embed(
            description = (
                f"**Locations Explored**: {len([match for match in player['unlockables'] if 'world_discovery_' in match] if player['unlockables'] else '0')}/21\n"
                f"**Hogsworth Fast Travel**: {len([match for match in player['unlockables'] if 'world_fasttravel_' in match] if player['unlockables'] else '0')}/19\n"
                f"**Warpkey Bag**: {warpkeybag[14:].capitalize()}\n\n"
                f"{':white_check_mark:' if 'world_discovery_hogsworth' in player['unlockables'] else ':x:'} Hogsworth\n"
                f"{':white_check_mark:' if 'world_discovery_hogsend' in player['unlockables'] else ':x:'} Hogsend\n"
                f"{':white_check_mark:' if 'world_discovery_ministry' in player['unlockables'] else ':x:'} Ministry\n"
                f"{':white_check_mark:' if 'world_discovery_london' in player['unlockables'] else ':x:'} London\n"
                f"{':white_check_mark:' if 'world_discovery_edgebrook' in player['unlockables'] else ':x:'} Edgebrook\n"
                f"{':white_check_mark:' if 'world_discovery_portstead' in player['unlockables'] else ':x:'} Portstead\n"
                f"{':white_check_mark:' if 'world_discovery_dwelling' in player['unlockables'] else ':x:'} Dwelling\n"
                f"{':white_check_mark:' if 'world_discovery_tristmoor' in player['unlockables'] else ':x:'} Hogsworth\n"
                f"{':white_check_mark:' if 'world_discovery_eldhamridge' in player['unlockables'] else ':x:'} Eldham Ridge\n"
                f"{':white_check_mark:' if 'world_discovery_squaluscove' in player['unlockables'] else ':x:'} Squalus Cove\n"
                f"{':white_check_mark:' if 'world_discovery_griffinshollow' in player['unlockables'] else ':x:'} Griffin's Hollow\n"
                f"{':white_check_mark:' if 'world_discovery_wigtown' in player['unlockables'] else ':x:'} Wigtown\n"
                f"{':white_check_mark:' if 'world_discovery_ireland' in player['unlockables'] else ':x:'} Ireland\n"
                f"{':white_check_mark:' if 'world_discovery_riddleyard' in player['unlockables'] else ':x:'} Riddleyard\n"
                f"{':white_check_mark:' if 'world_discovery_haggleton' in player['unlockables'] else ':x:'} Haggleton\n"
                f"{':white_check_mark:' if 'world_discovery_antrum' in player['unlockables'] else ':x:'} Antrum\n"
                f"{':white_check_mark:' if 'world_discovery_rushstone' in player['unlockables'] else ':x:'} Rushstone\n"
                f"{':white_check_mark:' if 'world_discovery_walden' in player['unlockables'] else ':x:'} Walden\n"
                f"{':white_check_mark:' if 'world_discovery_gnollbergport' in player['unlockables'] else ':x:'} Gnollberg Port\n"
                f"{':white_check_mark:' if 'world_discovery_greenshoreharbour' in player['unlockables'] else ':x:'} Greenshore Harbour\n"
                f"{':white_check_mark:' if 'world_discovery_azkaban' in player['unlockables'] else ':x:'} Dark Prison\n"
            ),
            color = self.client.house_colors[data["player"]["house"].lower()] if data["player"]["house"] else self.client.main_color,
        )
        embed.set_footer(text = f"Last updated: {humanize.naturaltime(datetime.datetime.now() - datetime.datetime.fromtimestamp(player['updated']))}")
        embed.set_author(name = f"{player['username'] if player['username'] else username}", icon_url = f"https://minotar.net/helm/{player['username']}.png")

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Locations(client))
