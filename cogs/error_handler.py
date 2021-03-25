import discord
import traceback
import sys
import asyncio

from discord.ext import commands
from copy import copy
from fuzzywuzzy import process

class ErrorHandler(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.command_list = []
        for command in self.client.commands:
            self.command_list.append(str(command))

            actual_command = self.client.get_command(str(command))
            for alias in actual_command.aliases:
                self.command_list.append(alias)


    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, 'on_error'):
            return

        if isinstance(error, commands.CommandNotFound):
            ratios = process.extract(ctx.message.content.split(' ')[0], self.command_list)

            description = [
                f"The command you tried to run does not exist. \nFor a full list of commands, type **{self.client.prefix}help**.\n"
            ]

            if ratios[0][1] > 70:
                description.append(f"Did you mean: **{ratios[0][0]}**?\n")
                description.append("React with 👍 if this was your intention.")

            embed = discord.Embed(
                description = "\n".join(description),
                color = self.client.main_color,
                title = "Unknown Command"
            )

            sent_message = await ctx.send(embed=embed)

            if ratios[0][1] > 70:
                await sent_message.add_reaction('👍')

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) == '👍'

                try:
                    reaction, user = await self.client.wait_for('reaction_add', timeout=15.0, check=check)
                except asyncio.TimeoutError:
                    await sent_message.remove_reaction('👍', self.client.user)
                else:
                    await sent_message.remove_reaction('👍', self.client.user)
                    await sent_message.remove_reaction('👍', ctx.message.author)

                    new_message = copy(ctx.message)
                    args = ''

                    if ctx.message.content.split(' ') != None and len(ctx.message.content.split(' ')) >= 2:
                        args = ctx.message.content.split(' ')[1]

                    new_message.content = f"{self.client.prefix}{ratios[0][0]} {args}"
                    await self.client.process_commands(new_message)

            return

        if isinstance(error, commands.MissingRole):
            embed = discord.Embed(
                description = (
                'You do not have permission to use this command.\n'
                f"The **{error.missing_role}** role is required to run this."
                ),
                color = self.client.main_color,
                title = "Missing Permission"
            )

            await ctx.send(embed=embed)
            return

        if ctx.command.name in ["load", "unload", "reload"]:
            embed = discord.Embed(
                description = (
                    f"An error has occured while trying to {ctx.command} this cog. Here is the error:"
                    f"```{error}```"
                ),
                color = self.client.main_color,
                title = "Error"
            )
            await ctx.send(embed=embed)
            return

        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(client):
    client.add_cog(ErrorHandler(client))
