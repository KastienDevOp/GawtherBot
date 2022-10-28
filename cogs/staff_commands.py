import disnake
import json
import io
import sqlite3 as sql

from disnake.ui import View, Button
from disnake.ext import commands
from datetime import datetime
from typing import List

from disnake.ext.commands.errors import MissingAnyRole

with open('config.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

guild_ids = [data["guild_id"], ]


class StaffCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="staff",
        description="Displays a list of sub-commands executable by staff members",
        guild_ids=guild_ids
    )
    @commands.has_any_role("Owners", "Developers", "Head Administrators", "Administrators", "Moderators", "Community Helpers")
    async def staff(self, inter, operation: str = commands.Param(choices=["purge"])):
        if operation == "purge":
            await inter.response.send_message("Please Enter The Number Of Messages To Purge", ephemeral=True)
            num = await self.bot.wait_for('message')

            await inter.edit_original_message("Please Enter The Reason For The Purge")
            reason = await self.bot.wait_for('message')

            if int(num.content):
                await self.purge(inter, num.content, reason.content)
            else:
                return inter.edit_original_message("The Member's ID Must Be A Whole Number (no decimal), and Has To Be All Numbers 0-9")
        else:
            await inter.response.send_message("Error On Param Selection")

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


# view = disnake.ui.View()
# item = disnake.ui.Button(style=disnake.ButtonStyle.blurple, label="Click Me", url="https://googlge.com")
# view.add_item(item=item)
# await ctx.send("This message has a button!",view=view)

# class ViewWithButton(disnake.ui.View):
#   @disnake.ui.button(style="", label="ClickMe")
#   async def click_me_button(self, button: disnake.ui.Button, interaction: disnake.Interaction):
#       print("Button was clicked!")
#   await ctx.send("This message has a button!", view=ViewWithButton())

def setup(bot):
    bot.add_cog(StaffCommands(bot))
