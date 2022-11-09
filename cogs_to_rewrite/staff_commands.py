import disnake
import json
import sqlite3 as sql

from disnake.ext import commands
from helpers.helper_methods import get_guild_id, delete_messages_log


class StaffCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="staff",
        description="Displays a list of sub-commands executable by staff members",
        guild_ids=[get_guild_id(), ]
    )
    @commands.has_any_role("Owners", "Developers", "Head Administrators", "Administrators", "Moderators", "Community Helpers")
    async def staff(self, inter, operation: str = commands.Param(choices=["manage_member","purge"])):
        if operation == "purge":
            await self.purge(inter)
        elif operation == "manage_member":
            await self.manage_member(inter)
        else:
            return await inter.response.send_message("Error On Param Selection")

    async def purge(self, inter):
        """
        CREDITS TO THE ASSISTANCE IN MAKING THIS COMMAND GOES TO DLCHAMP#6450 ON DISCORD
        """
        await inter.response.send_message("Please Enter The Number Of Messages To Purge", ephemeral=True)
        num = (await self.bot.wait_for('message')).content

        await inter.edit_original_message("Please Enter The Reason For The Purge")
        reason = (await self.bot.wait_for('message')).content

        await inter.edit_original_message(f"Removing {num} Messages From {inter.channel.name}. . .Please Wait. . .")

        purged = await inter.channel.purge(limit=int(num))

        _file = delete_messages_log(purged, reason)

        await inter.edit_original_message(f"Removed {len(purged)}/{num} Messages From {inter.channel.name}.")

        file_channel = disnake.utils.get(
            inter.guild.text_channels, name="purge_file_logs")

        embed = disnake.Embed(
            color=disnake.Colour.red(),
            title="Gawther Purge System Notification",
            description=f"{inter.author.name} Executed The Purge Command In #{inter.channel.name}"
        ).add_field(
            name="Reason",
            value=reason,
            inline=False
        ).set_thumbnail(
            url=self.bot.user.avatar
        )

        await file_channel.send(embed=embed, file=_file)

    async def manage_member(self,inter):
        await inter.response.send_message("Please Enter Warn, Mute, Kick, or Ban")
        

def setup(bot):
    bot.add_cog(StaffCommands(bot))
