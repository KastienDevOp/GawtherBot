import disnake
import asyncio

from disnake.ext import commands
from helpers import get_restricted_channels
from cogs.general_commands import GeneralCommands


class OnMessageEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("@ghelp"):
            await GeneralCommands.gawther_help(self,message)
        else:
            if message.channel.id in [int(channel) for channel in get_restricted_channels()]:
                if message.author.id != self.bot.user.id:
                    if not message.webhook_id:
                        await message.reply(
                            content="This is a notification ONLY channel! Do NOT post messages here! -Gawther"
                        )
                        await message.delete()
                        await asyncio.sleep(10)
                        return await message.channel.purge(limit=1)


def setup(bot):
    bot.add_cog(OnMessageEvents(bot))
