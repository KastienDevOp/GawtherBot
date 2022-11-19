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
                color=disnake.Colour.random(),
                title="Gawther's Help System",
                description="Please Download The Attached File For A Full List Of All Commands and Their Details. An Announcment Will Be Made When This File Is Updated."
            ).set_thumbnail(
                url=self.bot.user.avatar
            ).set_footer(
                text="This will open a .md (a mark-down file) in your browser window."
            )

            if message.author.top_role.name in ["Owners", "Head Administrators", "Administrators", "Moderators", "Community Helpers"]:
                file = disnake.File('./support_pages/staff_commands.md')
            elif message.author.top_role.name in ["Owners", "Developers"]:
                file = disnake.File('./support_pages/dev_commands.md')
            else:
                file = disnake.File('./support_pages/general_commands.md')

            return await message.reply(embed=embed, file=file)
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
