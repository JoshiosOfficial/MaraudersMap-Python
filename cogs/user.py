import discord
from discord.ext import commands


class User(commands.Cog):
    
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def user(self, ctx, user: discord.Member=None):
        
        if not user:
            user = ctx.author

        status_emojis = self.client.status_emojis

        username = (
            f"**Username**\n" 
            f"{user.mention} (`{user.id}`)\n\n"
        )

        nickname = ""
        if user.nick:
            nickname = (
                f"**Nickname** \n"
                f"{user.display_name} \n\n"
            )
    
        create_date = (
            f"**Account Creation**\n" 
            f"{user.created_at.strftime('%B %d, %Y')}\n\n"
        )

        join_date = (
            f"**Joined Discord Server**\n" 
            f"{user.joined_at.strftime('%B %d, %Y')}\n\n"
        )

        status = (
            f"**Status**\n"
            f"{status_emojis[user.desktop_status.value]} Desktop\n"
            f"{status_emojis[user.web_status.value]} Web\n"
            f"{status_emojis[user.mobile_status.value]} Mobile\n\n"
        )


        member_roles = [r.mention for r in user.roles][::-1]
        member_roles.pop()

        roles = (
            f"**Roles**\n"
            f"{' '.join(member_roles)}\n\n" if member_roles else "**Roles**\nNone\n\n"
        )

        embed = discord.Embed(
            description = username + nickname + create_date + join_date + status + roles,
            color = user.color if str(user.color) != "#000000" else self.client.main_color
        )

        embed.set_thumbnail(url = user.avatar_url)
        await ctx.send(embed=embed)

    @user.error
    async def user_error(self, ctx, error):

        if isinstance(error, commands.BadArgument):
            await self.user(ctx, ctx.author)
        else:
            print(error)


def setup(client):
    client.add_cog(User(client))