import discord
from discord.ext import commands

import aiohttp

class Housepoints(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def housepoints(self, ctx):

        response = await self.client.session.get("https://api.potterworldmc.com/housepoints")
        data = await response.json()

        housepoints = sorted(data['housepoints'].items(), key=lambda x: x[1], reverse=True)

        embed = discord.Embed(
            description = (
                f"{self.client.emotes[housepoints[0][0].upper()]} {housepoints[0][0].capitalize()} - **{housepoints[0][1]}**\n"
                f"{self.client.emotes[housepoints[1][0].upper()]} {housepoints[1][0].capitalize()} - **{housepoints[1][1]}**\n"
                f"{self.client.emotes[housepoints[2][0].upper()]} {housepoints[2][0].capitalize()} - **{housepoints[2][1]}**\n"
                f"{self.client.emotes[housepoints[3][0].upper()]} {housepoints[3][0].capitalize()} - **{housepoints[3][1]}**\n\n"
                f"{self.client.emotes[housepoints[0][0].upper()]} {housepoints[0][0].capitalize()} is **{housepoints[0][1] - housepoints[1][1]}** points ahead of {self.client.emotes[housepoints[1][0].upper()]} {housepoints[1][0].capitalize()}!"
            ),
            color = self.client.house_colors[housepoints[0][0]],
            title = "Current House Points"
        )

        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Housepoints(client))
