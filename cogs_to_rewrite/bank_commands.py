import disnake
import sqlite3 as sql
import json
import asyncio

from disnake.ext import commands
from datetime import date
from Paginator import CreatePaginator
from helpers.helper_methods import get_guild_id

class BankCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name = "bank",
        description = "Allows a user to pay or request money to or from another member in the discord server.",
        guild_ids = [get_guild_id(),]
    )
    @commands.has_any_role(
        "Owners", "Developers", "Head Admins", "Moderators", "Community Helpers",
        "Programming", "Gaming", "Artistry", "Nitro", "Member", "Python", "JavaScript",
        "Java", "Rust", "HTML-CSS", "Minecraft", "Summoners-War", "Chess"
    )
    async def bank(self, inter, operations: str = commands.Param(choices=["list_requests","pay","pay_request","request","adjust_balance"])):
        if operations == "list_requests":
            await self.get_all_requests(inter)
        elif operations == "pay":
            await self.pay_to_member(inter)
        elif operations == "pay_request":
            await self.pay_requests(inter)
        elif operations == "request":
            await self.request_from_member(inter)
        elif operations == "adjust_balance":
            await self.adjust_user_balance(inter)
        else:
            return await inter.response.send_message("Error With Params")

    async def get_all_requests(self,inter):
        with sql.connect('bank.db') as bankdb:
            cur = bankdb.cursor()

            srch = 'SELECT * FROM requests WHERE payer=?'
            val = (inter.author.id,)

            all_requests = cur.execute(srch, val).fetchall()

            lead_embed = disnake.Embed(
                color = disnake.Colour.random(),
                title = "Gawther's Bank Notification System",
                description = "You Requested A Copy Of All Your Unpaid Payment Requests. Please See The Following Pages"
            ).set_thumbnail(
                url = self.bot.user.avatar
            )

            embeds = []

            for request in all_requests:
                num = request[0]
                payee = disnake.utils.get(inter.guild.members, id=requests[2])
                date = request[3]
                amount = request[4]
                reason = request[5]

                embeds.append(
                    embed = disnake.Embed(
                        color = disnake.Colour.random(),
                        title = f"Request #{num}",
                        description = f"You Owe {payee.name} ${amount} GB From {date}"
                    ).add_field(
                        name = "Reason",
                        value = f"{reason}",
                        inline = False
                    )
                )

            if len(embeds) > 1:
                embeds.insert(0, lead_embed)
                return await inter.response.send_message(embed = embeds[0],view = CreatePaginator(embeds, inter.author.id, 0),ephemeral=True)
            else:
                lead_embed.add_field(
                    name = "No Un-Paid Request",
                    value = "You Have No Open Request. Have A Great Day!",
                    inline = False
                )
                return await inter.response.send_message(embed=lead_embed,ephemeral=True)

    async def pay_to_member(self,inter):
        await inter.response.send_message("Enter Member's ID. To get the ID, right-click the members profile, and select Copy ID")
        member_id = int((await self.bot.wait_for('message')).content)

        if not member_id:
            return await inter.edit_original_message("The Member's ID Must Be A Whole Number! Ex: 0123456789")
        
        await inter.edit_original_message("Enter The Amount To Pay")
        amount = int((await self.bot.wait_for('message')).content)

        if not amount:
            return await inter.edit_original_message("The Amount Must Be A Whole Number! Ex: 150, 26, 1882")
        
        await inter.edit_original_message("Enter The Reason For The Payment")
        reason = (await self.bot.wait_for('messaaage')).content

        payer = inter.author
        payee = disnake.utils.get(inter.guild.members, id=member_id)

        with sql.connect('members.db') as members:
            cur = members.cursor()

            srch = 'SELECT bank FROM profiles WHERE id=?'
            srch2 = 'SELECT bank FROM profiles WHERE id=?'

            val = (payer.id, )
            val2 = (payee.id, )

            payer_current_balance = cur.execute(srch, val).fetchone()[0]
            payee_current_balance = cur.execute(srch2, val2).fetchone()[0]

            if payer_current_balance >= amount:
                payer_new_bal = payer_current_balance - amount
                payee_new_bal = payee_current_balance + amount

                srch3 = 'UPDATE profiles SET bank=? WHERE id=?'
                srch4 = 'UPDATE profiles SET bank=? WHERE id=?'

                val3 = (payer_new_bal, payer.id, )
                val4 = (payee_new_bal, payee.id, )

                cur.execute(srch3, val3)
                cur.execute(srch4, val4)

                with sql.connect('bank.db') as bank:
                    cur = bank.cursor()

                    today = datetime.now()

                    all_transactions = cur.execute('SELECT * FROM transactions').fetchall()
                    new_trans_id = len(all_transactions) + 1

                    srch5 = 'INSERT INTO transations(transaction_number, payer, payee, date, amount, reason) VALUES (?,?,?,?,?,?)'
                    val5 = (new_trans_id, payer.id, payee.id, today, amount, reason)

                    cur.execute(srch5, val5)

        payer_embed = disnake.Embed(
            color = disnake.Colour.green(),
            title = "Gawther's Bank Notification System",
            description = f"You Paid {payee.name} ${amount} GB on {today}"
        ).add_field(
            name = "Reason",
            value = f"{reason}",
            inline = False
        ).add_field(
            name = "Updated Bank Information",
            value = f"Previous Balance: ${payee_current_balance} GB\nAmount Withdrawn: ${amount} GB\nNew Balance: ${payer_new_bal} GB",
            inline = False
        ).set_thumbnail(
            url = self.bot.user.avatar
        ).set_footer(
            text = "If you find this to be in error, please contact support!"
        )

        payee_embed = disnake.Embed(
            color = disnake.Colour.green(),
            title = "Gawther's Bank Notification System",
            description = f"You Were Paid ${amount} GB By {payer.name} on {today}"
        ).add_field(
            name = "Reason",
            value = f"{reason}",
            inline = False
        ).add_field(
            name = "Updated Bank Information",
            value = f"Previous Balance: ${payee_current_balance} GB\nAmount Deposited: ${amount} GB\nNew Balance: ${payee_new_bal} GB",
            inline = False
        ).set_thumbnail(
            url = self.bot.user.avatar
        ).set_footer(
            text = "If you find this to be in error, please contact support!"
        )

        confirmation_embed = disnake.Embed(
            color = disnake.Colour.green(),
            title = "Gawther Bank Notifcation System",
            value = f"{payer.name} Has Paid {payee.name} The Amount Of ${amount} GB on {today}"
        ).add_field(
            name = "Reason",
            value = f"{reason}",
            inline = False
        ).set_thumbnail(
            url = self.bot.user.avatar
        )

        await payer.send(embed=payer_embed)
        await payee.send(embed=payee_embed)
        await disnake.utils.get(inter.guild.text_channels, name="bank_notifications").send(embed=confirmation_embed)
        await inter.channel.purge(limit=3)
        await inter.edit_original_message("Your Payment Has Been Process and Sent Successfully. Please See Your DM's For Your Receipt.")
 

def setup(bot):
    bot.add_cog(BankCommands(bot))