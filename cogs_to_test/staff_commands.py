import disnake
import json
import io
import sqlite3 as sql

from disnake.ext import commands
from disnake.ext.commands.errors import MemberNotFound
from datetime import datetime, timedelta
from typing import List
from helpers.helper_methods import get_guild_id


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
            await inter.response.send_message("Please Enter The Number Of Messages To Purge", ephemeral=True)
            num = await self.bot.wait_for('message')

            await inter.edit_original_message("Please Enter The Reason For The Purge")
            reason = await self.bot.wait_for('message')

            if int(num.content):
                await self.purge(inter, num.content, reason.content)
            else:
                return inter.edit_original_message("The Member's ID Must Be A Whole Number (no decimal), and Has To Be All Numbers 0-9")
        elif operation == "manage_member":
            await inter.response.send_message("Enter The Target Members ID",ephemeral=True)
            member_id = (await self.bot.wait_for('message')).content

            if int(member_id):
                member = disnake.utils.get(inter.guild.members, id=int(member_id))
            else:
                await inter.channel.purge(limit=1)
                return await inter.edit_original_message("The Member ID Must Be Of Numeric 0-9 Values")

            await inter.edit_original_message("Enter The Type Of Action. Ban, Kick, Mute, Warn")
            action = (await self.bot.wait_for('message')).content.lower()

            if action in ["ban","kick","mute","warn"]:
                action_type = action
            else:
                return await inter.edit_original_message("You Must Enter Ban, Kick, Mute, or Warn For The Action")

            await inter.edit_original_message(f"Enter The Length Of Time For The {action_type} ***__IN SECONDS!!!__***")
            length_of_time = (await self.bot.wait_for('message')).content

            if int(length_of_time):
                now = datetime.now()
                end = now + timedelta(seconds=int(length_of_time))
            else:
                return await inter.edit_original_message("The Length Of Time Must Be In Seconds. Days Divided By 24 Hours Divided By 60 Minutes Per Hour Divided By 60 Seconds Per Hour = Total Seconds")
            
            await inter.edit_original_message(f"Enter The Reason For The {action_type}")
            reason_content = (await self.bot.wait_for('message')).content

            if reason_content:
                reason = reason_content
            else:
                return await inter.edit_original_message("The Reason Must Be A Printable String")

            confirmation = self.update_db(member,action_type,now,end,reason)

            if confirmation:
                self.send_notification()
            else:
                return await inter.edit_original_message("The Database Failed To Update. Please Contact Developers")
        else:
            return await inter.response.send_message("Error On Param Selection")

    async def purge(self, inter, num, reason):
        """
        CREDITS TO THE ASSISTANCE IN MAKING THIS COMMAND GOES TO DLCHAMP#6450 ON DISCORD
        """
        num = int(num)

        await inter.edit_original_message(f"Removing {num} Messages From {inter.channel.name}. . .Please Wait. . .")

        purged = await inter.channel.purge(limit=num)

        _file = self.delete_messages_log(purged, reason)

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

    def delete_messages_log(self, messages: List[disnake.Message], reason) -> disnake.File:
        '''Converts the list of deleted messages to a log.txt and returns the File object ready to be sent'''
        _file = io.StringIO()

        for i, message in enumerate(messages):
            line = {
                str(i): {
                    'author': message.author.name,
                    'timestamp': str(message.created_at),
                    'content': message.content
                }
            }
            _file.write("="*30 + '\n')
            _file.write("Reason: " + reason + '\n')
            _file.write(f'{json.dumps(line, indent=2)}\n')

        _file.seek(0)
        return disnake.File(_file, filename=f"Deleted_{datetime.now()}.txt")

    async def update_db(self,member,action_type,now,end,reason):
        with sql.connect('bank.db') as mdb:
            cur = mdb.cursor()

def setup(bot):
    bot.add_cog(StaffCommands(bot))
