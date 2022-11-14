import disnake
import asyncio

from disnake.ext import commands
from helpers import get_restricted_channels


class OnMessageEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith("@ghelp"):
            embed = disnake.Embed(
                color = disnake.Colour.random(),
                title = "Gawther's Help System",
                description = "Please [Click Here]('https://google.com') For A Full List Of All Commands and Their Details."
            ).set_thumbnail(
                url = self.bot.user.avatar
            ).set_footer(
                text = "This will open a .md (a mark-down file) in your browser window."
            )

            return await message.reply(embed=embed)
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
