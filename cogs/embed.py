import discord
import asyncio

from discord.ext import commands
from discord import Webhook, AsyncWebhookAdapter

class Embed(commands.Cog):

    def __init__(self, client):
        self.client = client

        self.embeds = {}

        self.ERROR_EMBED = discord.Embed(
            description = f"You have not created an embed! To create one, type `{self.client.prefix}embed create` to start the process.",
            color = self.client.main_color
        )

        self.NO_ARGUMENT_EMBED = discord.Embed(
            description = 'You are missing an {command} argument for this command.',
            color = self.client.main_color
        )

        self.color_list = {
            "griffin": 0xD92C2C,
            "raven": 0x0099E1,
            "serpent": 0x25A225,
            "honeybadger": 0xF1C40F,
            "main": 0xA62019
        }

    async def handle_checks(self, ctx, message):
        if ctx.author not in self.embeds:
            error_embed = self.ERROR_EMBED.copy()
            await ctx.send(embed = error_embed)
            return False

        if not message:
            no_argument_embed = self.NO_ARGUMENT_EMBED.copy()
            no_argument_embed.description = no_argument_embed.description.format(command=ctx.command)
            await ctx.send(embed = no_argument_embed)
            return False

        if len(message) > 256 and ctx.command.name in ['author', 'title', 'footer']:
            error_embed = discord.Embed(
                description = f"The {ctx.command.name} field can only be 256 characters, and so your input did not work.",
                color = self.client.main_color
            )
            await ctx.send(embed = error_embed)
            return False

        return True

    @commands.group(
        name = 'embed',
        aliases = ['e']
    )
    async def embed(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Will be an embed help command")

    @embed.group(
        name = 'create',
        aliases = ['start']
    )
    async def create(self, ctx):
        if ctx.invoked_subcommand is None:
            if ctx.author in self.embeds:
                error_embed = discord.Embed(
                    description = f"You have already created an embed! To remove it, type `{self.client.prefix}embed cancel` to restart the process.",
                    color = self.client.main_color
                )
                await ctx.send(embed = error_embed)
                return

            embed = {
                'embed': discord.Embed(),
                'emojis': [],
                'content': ''
            }
            self.embeds[ctx.author] = embed

            await ctx.message.add_reaction('✅')

    @embed.group(
        name = 'description',
        aliases = ['desc']
    )
    async def description(self, ctx, *, message=None):

        if ctx.invoked_subcommand is None:

            result = await self.handle_checks(ctx, message)
            if not result:
                return

            embed = self.embeds[ctx.author]['embed']
            embed.description = message

            await ctx.message.add_reaction('✅')

    @embed.group(
        name = 'view'
    )
    async def view(self, ctx):

        if ctx.invoked_subcommand is None:

            if ctx.author not in self.embeds:
                error_embed = self.ERROR_EMBED.copy()
                await ctx.send(embed = error_embed)
                return

            embed = self.embeds[ctx.author]['embed']
            content = self.embeds[ctx.author]['content']

            if type(embed.description) is not str:
                missing_desc_embed = discord.Embed(
                    description = 'You do not have a description in the embed. This is required to view it.',
                    color = self.client.main_color
                )
                await ctx.send(embed=missing_desc_embed)
                return

            await ctx.send(embed=embed, content=content)

    @embed.group(
        name = 'send'
    )
    async def send(self, ctx, channel: discord.TextChannel = None, *, user: discord.Member = None):

        if ctx.invoked_subcommand is None:

            if ctx.author not in self.embeds:
                error_embed = self.ERROR_EMBED.copy()
                await ctx.send(embed = error_embed)
                return

            embed = self.embeds[ctx.author]

            if type(embed['embed'].description) is not str:
                missing_desc_embed = discord.Embed(
                    description = 'You do not have a description in the embed. This is required to send it.',
                    color = self.client.main_color
                )
                await ctx.send(embed=missing_desc_embed)
                return

            user = user or ctx.author
            channel = channel or ctx.channel

            webhooks_list = []
            for w in await channel.webhooks():
                webhooks_list.append(f"{w.name} - `{w.id}`")
            webhooks = "\n".join(webhooks_list)

            choose_embed = discord.Embed(
                description = (
                    'Since you are sending out an embed, it will use a webhook. Below I have listed all webhooks currently on this server. '
                    'Pick the webhook that is your name or the name of the person you are trying to send as. Send the id of that webhook, or `new` to create a new one.'
                    f"\n\n**Webhooks:**\n{webhooks}"
                ),
                color = self.client.main_color
            )
            await ctx.send(embed=choose_embed)

            def check(message):
                return message.author == ctx.message.author

            try:
                message = await self.client.wait_for('message', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                fail_embed = discord.Embed(
                    description = "You did not specify the webhook ID that you wish to use in time. Please use the command again if you want to send your embed.",
                    color = self.client.main_color
                )
                await ctx.send(embed=fail_embed)
            else:
                if message.content == "new":
                    created_webhook = await channel.create_webhook(name=user.name)
                    sent_message = await created_webhook.send(embed = embed['embed'], content = embed['content'], username = user.display_name, avatar_url=user.avatar_url, wait=True)

                    for emoji in embed['emojis']:
                        await sent_message.add_reaction(emoji)

                    await message.add_reaction('✅')
                    return
                else:
                    for webhook in await channel.webhooks():
                        if message.content == str(webhook.id):
                            sent_message = await webhook.send(embed = embed['embed'], content = embed['content'], username = user.display_name, avatar_url = user.avatar_url)

                            for emoji in embed['emojis']:
                                await sent_message.add_reaction(emoji)

                            await message.add_reaction('✅')
                            return

                    fail_embed = discord.Embed(
                        description = "You did not specify a correct webhook ID that you wish to use. Please use the command again if you want to send your embed.",
                        color = self.client.main_color
                    )
                    await ctx.send(embed=fail_embed)

    @embed.group(
        name = 'copy'
    )
    async def copy(self, ctx, message: discord.Message):

        if ctx.invoked_subcommand is None:

            if ctx.author in self.embeds:
                error_embed = discord.Embed(
                    description = f"You have already created an embed! To remove it, type `{self.client.prefix}embed cancel` to restart the process.",
                    color = self.client.main_color
                )
                await ctx.send(embed = error_embed)
                return

            if len(message.embeds) == 0:
                error_embed = discord.Embed(
                    description = "This message does not have an embed, and so I am unable to copy it.",
                    color = self.client.main_color
                )
                await ctx.send(embed = error_embed)
                return

            embed = {
                'embed': message.embeds[0],
                'emojis': [],
                'content': message.content
            }
            self.embeds[ctx.author] = embed

            await ctx.message.add_reaction('✅')

    @embed.group(
        name = 'edit'
    )
    async def edit(self, ctx, message: discord.Message):

        if ctx.invoked_subcommand is None:

            if ctx.author not in self.embeds:
                error_embed = self.ERROR_EMBED.copy()
                await ctx.send(embed = error_embed)
                return

            if len(message.embeds) == 0:
                error_embed = discord.Embed(
                    description = "This message does not have an embed, and so I am unable to edit it.",
                    color = self.client.main_color
                )
                await ctx.send(embed = error_embed)
                return

            embed = self.embeds[ctx.author]['embed']
            content = self.embeds[ctx.author]['content']

            await message.edit(content=content, embed=embed)
            await ctx.message.add_reaction('✅')

    @embed.group(
        name = 'botsend'
    )
    async def botsend(self, ctx, channel: discord.TextChannel = None):

        if ctx.invoked_subcommand is None:

            if ctx.author not in self.embeds:
                error_embed = self.ERROR_EMBED.copy()
                await ctx.send(embed = error_embed)
                return

            channel = channel or ctx.channel
            embed = self.embeds[ctx.author]

            if type(embed['embed'].description) is not str:
                missing_desc_embed = discord.Embed(
                    description = 'You do not have a description in the embed. This is required to send it.',
                    color = self.client.main_color
                )
                await ctx.send(embed=missing_desc_embed)
                return

            sent_message = await channel.send(embed = embed['embed'], content = embed['content'])

            for emoji in embed['emojis']:
                await sent_message.add_reaction(emoji)

            await ctx.message.add_reaction('✅')

    @embed.group(
        name = 'cancel'
    )
    async def cancel(self, ctx):

        if ctx.invoked_subcommand is None:

            if ctx.author not in self.embeds:
                error_embed = self.ERROR_EMBED.copy()
                await ctx.send(embed = error_embed)
                return

            del self.embeds[ctx.author]

            await ctx.message.add_reaction('✅')

    @embed.group(
        name = 'author'
    )
    async def author(self, ctx, *, message=None):

        if ctx.invoked_subcommand is None:

            result = await self.handle_checks(ctx, message)
            if not result:
                return

            embed = self.embeds[ctx.author]['embed']
            embed.set_author(name = message, icon_url = "https://i.imgur.com/T1Vcy1p.png")

            await ctx.message.add_reaction('✅')

    @embed.group(
        name = 'color',
        aliases = ['colour']
    )
    async def color(self, ctx, *, message=None):

        if ctx.invoked_subcommand is None:

            result = await self.handle_checks(ctx, message)
            if not result:
                return

            embed = self.embeds[ctx.author]['embed']

            if message.lower() in self.color_list:
                embed.color = self.color_list[message.lower()]
                await ctx.message.add_reaction('✅')
            else:
                try:
                    embed.color = discord.Color(value = int(message, 16))
                    await ctx.message.add_reaction('✅')
                except ValueError:
                    invalid_value_embed = discord.Embed(
                        description = 'This color does not exist in my system or is not a hex color code.',
                        color = self.client.main_color
                    )
                    await ctx.send(embed = invalid_value_embed)
                    return

    @embed.group(
        name = 'image'
    )
    async def image(self, ctx, *, message=None):

        if ctx.invoked_subcommand is None:

            result = await self.handle_checks(ctx, message)
            if not result:
                return

            embed = self.embeds[ctx.author]['embed']
            embed.set_image(url=message)

            await ctx.message.add_reaction('✅')

    @embed.group(
        name = 'title'
    )
    async def title(self, ctx, *, message=None):

        if ctx.invoked_subcommand is None:

            result = await self.handle_checks(ctx, message)
            if not result:
                return

            embed = self.embeds[ctx.author]['embed']
            embed.title = message

            await ctx.message.add_reaction('✅')

    @embed.group(
        name = 'thumbnail'
    )
    async def thumbnail(self, ctx, *, message=None):

        if ctx.invoked_subcommand is None:

            result = await self.handle_checks(ctx, message)
            if not result:
                return

            embed = self.embeds[ctx.author]['embed']
            embed.set_thumbnail(url=message)

            await ctx.message.add_reaction('✅')

    @embed.group(
        name = 'footer'
    )
    async def footer(self, ctx, *, message=None):

        if ctx.invoked_subcommand is None:

            result = await self.handle_checks(ctx, message)
            if not result:
                return

            embed = self.embeds[ctx.author]['embed']
            embed.set_footer(text=message)

            await ctx.message.add_reaction('✅')

    @embed.group(
        name = 'content'
    )
    async def content(self, ctx, *, message=None):

        if ctx.invoked_subcommand is None:

            result = await self.handle_checks(ctx, message)
            if not result:
                return

            self.embeds[ctx.author]['content'] = message
            await ctx.message.add_reaction('✅')

    @embed.group(
        name = 'emojis'
    )
    async def emojis(self, ctx, *, message=None):

        if ctx.invoked_subcommand is None:

            result = await self.handle_checks(ctx, message)
            if not result:
                return

            emojis = []
            for emoji in message.split(' '):
                emojis.append(emoji)

            self.embeds[ctx.author]['emojis'] = emojis
            await ctx.message.add_reaction('✅')

    @embed.group(
        name = 'footer_image'
    )
    async def footer_image(self, ctx, *, message=None):

        if ctx.invoked_subcommand is None:

            result = await self.handle_checks(ctx, message)
            if not result:
                return

            embed = self.embeds[ctx.author]['embed']

            if not embed.footer.text:
                no_footer_embed = discord.Embed(
                    description = 'You need a footer use this command.',
                    color = self.client.main_color
                )
                await ctx.send(embed = no_footer_embed)
                return

            embed.set_footer(text = str(embed.footer.text), icon_url=message)
            await ctx.message.add_reaction('✅')

    @embed.group(
        name = 'allcolors',
        aliases = ['allcolor']
    )
    async def allcolors(self, ctx,):

        if ctx.invoked_subcommand is None:

            for color in self.color_list:
                embed = discord.Embed(
                    description = f"**{color.capitalize()}**: #{self.color_list[color]}",
                    color = self.color_list[color]
                )
                await ctx.send(embed=embed)


    @copy.error
    @edit.error
    @send.error
    @botsend.error
    async def embed_error(self, ctx, error):

        if isinstance(error, commands.MessageNotFound):

            if ctx.command.name in ['copy', 'edit']:
                error_embed = discord.Embed(
                    description= f"You must provided a message link in order to {ctx.command.name} an embed.",
                    color = self.client.main_color
                )
                await ctx.send(embed = error_embed)

        elif isinstance(error, commands.ChannelNotFound):

            if ctx.command.name in ['botsend', 'send']:
                error_embed = discord.Embed(
                    description= "An invalid channel was provided. Make sure this channel exists.",
                    color = self.client.main_color
                )
                await ctx.send(embed = error_embed)

        else:
            print(error)

def setup(client):
    client.add_cog(Embed(client))
