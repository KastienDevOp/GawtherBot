import disnake

from disnake.ext import commands
from API.helpers import get_guild_id


class DeveloperCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="empty",description="Empty",guild_ids=[get_guild_id(),])
    async def empty(self, inter):
        pass


def setup(bot):
    bot.add_cog(DeveloperCommands(bot))