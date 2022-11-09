import disnake
import asyncio

from disnake.ext import commands


class OnMessageEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        notification_channels = [
            1035682116429680682,
            1033855023618203698,
            1033877482987864124,
            1033878532062990507,
            1033879108230336542,
            1033889553930518610,
            1035398905392803890,
            1035713979353399336,
            1036871164838039624,
            1033922944600129567,
            1033355878562283582
        ]

        if message.channel.id in notification_channels:
            if message.author.id == 925933044932702228:
                pass
            else:
                await message.delete()
                return await message.channel.send("This is a notification ONLY channel! Do NOT post messages here! -Gawther")

def setup(bot):
    bot.add_cog(OnMessageEvents(bot))