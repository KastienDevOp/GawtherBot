import disnake
import sqlite3 as sql
import json
import asyncio

from disnake.ext import commands
from datetime import date
from Paginator import CreatePaginator
from helpers import get_guild_id


class BankCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="bank",
        description="Allows a user to pay or request money to or from another member in the discord server.",
        guild_ids=[get_guild_id(), ]
    )
    @commands.has_any_role(
        "Owners", "Developers", "Head Admins", "Moderators", "Community Helpers",
        "Programming", "Gaming", "Artistry", "Nitro", "Member", "Python", "JavaScript",
        "Java", "Rust", "HTML-CSS", "Minecraft", "Summoners-War", "Chess"
    )
    async def bank(self, inter, cmd: str = commands.Param(choices=["Pay", "Request", "Show All Request", "Pay Open Request"])):
        if cmd == "Pay":
            pass
        elif cmd == "Request":
            pass
        elif cmd == "Show All Request":
            pass
        elif cmd == "Pay Open Request":
            pass
        else:
            pass

    async def pay(self, inter):
        await asyncio.sleep(1)
        await inter.response.send_message("Enter The ID For The Member You Want To Pay", ephemeral=True)

        user_input = int((await self.bot.wait_for('message')).content)

        if int(user_input):
            member = disnake.utils.get(inter.guild.members, id=int(user_input))
        else:
            return await inter.edit_original_message("The Member Must Be Apart Of This Guild. If This Is An Error, Contant Support")

        await inter.channel.purge(limit=1)

        await inter.edit_original_message("Enter The Amount To Pay")

        amount = int((await self.bot.wait_for('message')).content)

        if not int(amount):
            return await inter.edit_original_message("The Amount Must Be A Whole Number")

        await inter.edit_original_message("Enter The Reason For The Payment")

        reason = (await self.bot.wait_for('message')).content

        if not all(i.isprintable() for i in reason):
            return await inter.edit_original_message("The Reason Must Be A Printable Screen!")

        """INSERT DATABASE WORKING HERE"""
        """SEND NOTIFICATION TO PAYER, PAYEE, AND TEXT CHANNEL HERE"""

        await inter.edit_original_message("Your Payment Has Been Successful.")


def setup(bot):
    bot.add_cog(BankCommands(bot))
