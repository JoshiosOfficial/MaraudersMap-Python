import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if hasattr(ctx.command, 'on_error'):
            return

        if isinstance(error, commands.CommandNotFound):
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
            
        print(error)

def setup(client):
    client.add_cog(ErrorHandler(client))