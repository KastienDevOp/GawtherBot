import disnake
import json
import sqlite3 as sql

from disnake.ext import commands
from helpers import get_guild_id, delete_messages_log


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
        elif operation == "announcement":
            await self.make_announcement(inter)
        else:
            return await inter.response.send_message("Error On Param Selection")

    async def purge(self, inter):
        """
        CREDITS TO THE ASSISTANCE IN MAKING THIS COMMAND GOES TO DLCHAMP#6450 ON DISCORD
        """
        await inter.response.send_message("Please Enter The Number Of Messages To Purge", ephemeral=True)
        num = int((await self.bot.wait_for('message')).content)

        await inter.edit_original_message("Please Enter The Reason For The Purge")
        reason = (await self.bot.wait_for('message')).content

        await inter.edit_original_message(f"Removing {num} Messages From {inter.channel.name}. . .Please Wait. . .")

        if num >= 500:
            await inter.edit_original_message("That Is Too Many Messages! Insert Pass Phrase To Override. . .")
            pass_phrase = (await self.bot.wait_for('message',timeout=30)).content

            # create a pass phrase
            if pass_phrase == "admin":
                purged = await inter.channel.purge(limit=num)

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
        cmd = (await self.bot.wait_for('message')).content.lower()

        await inter.channel.purge(limit=1)
        await inter.edit_original_message("Enter The Members ID")
        user_input = (await self.bot.wait_for('message')).content
        
        await inter.channel.purge(limit=1)
        await inter.edit_original_message("Enter The Reason For The Warning")
        reason = (await self.bot.wait_for('message')).content
        await inter.channel.purge(limit=1)

        if cmd not in ["warn","mute","kick","ban"]:
            return await inter.edit_original_message("The Command Must Be Either Warn, Mute, Kick or Ban!")

        if not int(user_input):
            return await inter.edit_original_message("The Member's ID Must Be Of Numeric Value or Apart Of This Guild!")

        if not all(i.isprintable() for i in reason):
            return await inter.edit_original_message("The Reason Must Be A Printable String!")

        member = disnake.utils.get(inter.guild.members, id=int(user_input))

        if cmd == "warn":
            await self.warn_member(inter,member,cmd,reason)
        elif cmd == "mute":
            await self.mute_member(inter,member,cmd,reason)
        elif cmd == "kick":
            await self.kick_member(inter,member,cmd,reason)
        elif cmd == "ban":
            await self.ban_member(inter,member,cmd,reason)
        else:
            return await inter.edit_original_message("Something Went Wrong. Please Contact The Developers!")

    async def warn_member(self,inter,member,cmd,reason):
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT warnings FROM members WHERE id=?'
            val = (member.id,)

            current_warnings = cur.execute(srch, val).fetchone()[0]
            new_count = current_warnings + 1

            srch2 = 'UPDATE members SET warnings=? WHERE id=?'
            val2 = (new_count, member.id,)

            cur.execute(srch2, val2)

        embed = disnake.Embed(
            color = disnake.Colour.orange(),
            title = "Gawther's Moderation System Notification",
            description = f"{inter.author.name} Has Warned {member.name}."
        ).add_field(
            name = "Reason",
            value = reason,
            inline = False
        ).add_field(
            name = "Counts",
            value = f"Previous Warnings: {current_warnings}\nNew Warnings: {new_count}",
            inline = False
        ).set_thumbnail(
            url = self.bot.user.avatar
        )

        noti_chan = disnake.utils.get(inter.guild.text_channels, name="moderation_notifications")

        await member.send(embed=embed)
        await noti_chan.send(embed=embed)

        return await inter.edit_original_message(f"You Have Successfully Warned, {member.name}")

    async def mute_member(self,inter,member,cmd,reason):
        pass

    async def kick_member(self,inter,member,cmd,reason):
        pass

    async def ban_member(self,inter,member,cmd,reason):
        pass

    async def make_announcement(self,inter):
        pass

        
def setup(bot):
    bot.add_cog(StaffCommands(bot))
