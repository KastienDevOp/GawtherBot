import disnake
import json
import asyncio

from disnake.ext import commands

with open('config.json','r',encoding='utf-8-sig') as f:
    data = json.load(f)

guild_ids = [data["guild_id"],]


class StaffCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name = "purge",
        description = "Remove _N_ Number Of Messages From The Channel The Command Is Executed In.",
        guild_ids = guild_ids
    )
    async def purge(self, inter, num: int):
        x = num
        await inter.response.send_message(f"Removing {x} Messages From {inter.channel.name}. . . Please Wait . . .", ephemeral=True)

        channel_history = await inter.channel.history(limit=num).flatten()

        """
        While deleting messages, if channel runs out of messagse to delete, stop loop and print num_deleted/total -> reason
        otherwise, regular deleting of messages, when counter reaches zero -> completion message
        """

        for i in range(num):
            await inter.channel.purge(limit=5)

            if num > 0:
                num -= 5
                await inter.edit_original_message(f"Purging {num} Messages . . . Please Wait . . . ")
                await asyncio.sleep(0.3)
            else:
                break

        await inter.edit_original_message(f"Successfully Removed {x} Message From {inter.channel.name}.")

    

def setup(bot):
    bot.add_cog(StaffCommands(bot))