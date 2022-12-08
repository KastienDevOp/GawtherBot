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
            self.pay(inter)
        elif cmd == "Request":
            self.request(inter)
        elif cmd == "Show All Request":
            self.show_all(inter)
        elif cmd == "Pay Open Request":
            self.pay_open(inter)
        else:
            return await inter.response.send_message("Invalid Operation: Contact Developers")

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

        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT balance FROM members WHERE id=?'
            val = (inter.author.id, )

            srch2 = 'SELECT balance FROM members WHERE id=?'
            val2 = (member.id, )

            payer_bal = cur.execute(srch, val).fetchone()[0]
            payee_bal = cur.execute(srch2, val2).fetchone()[0]

            if payer_bal >= amount:
                payer_new_bal = payer_bal - amount
                payee_new_bal = payee_bal + amount

                srch3 = 'UPDATE members SET balance=? WHERE id=?'
                val3 = (payer_new_bal, inter.author.id, )
                val4 = (payee_new_bal, member.id, )

                cur.execute(srch3, val3)
                cur.execute(srch3, val4)
            else:
                return await inter.edit_original_message("You do not have enough in your bank balance to cover this transaction. Please try again later.")

        payer = inter.author
        payee = member

        await payer.send(await self.send_confirmation(payer, payee, amount, reason))
        await payee.send(await self.send_confirmation(payer, payee, amount, reason))

        await inter.edit_original_message("You Have Successfully Sent The Payment. Please See Your DM's For Your Receipt")

    async def send_confirmation(self, payer, payee, amount, reason):
        embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = "Gawther's Bank Notification System",
            description = "Please find your details below"
        ).add_field(
            name = 'Your Account Has Been Updated!',
            value = f"{payer.name} has paid {payee.name} ${amount} GB",
            inline = False
        ).add_field(
            name = "Reason",
            value = reason,
            inline = False
        ).set_thumbnail(
            url = self.bot.user.avatar
        ).set_footer(
            text = "If you find this to be in error, please contact support."
        )

        return embed

    async def request(self, inter):
        pass

    async def show_all(self, inter):
        pass

    async def pay_open(self, inter):
        pass

def setup(bot):
    bot.add_cog(BankCommands(bot))
