import disnake
import sqlite3 as sql
import json
import asyncio

from disnake.ext import commands
from datetime import date

with open('config.json','r',encoding='utf-8-sig') as f:
    data = json.load(f)

guild_ids = [data["guild_id"],]


class BankCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name = "bank",
        description = "Allows a user to pay or request money to or from another member in the discord server.",
        guild_ids = guild_ids
    )
    @commands.has_any_role(
        "Owners", "Developers", "Head Admins", "Moderators", "Community Helpers",
        "Programming", "Gaming", "Artistry", "Nitro", "Member", "Python", "JavaScript",
        "Java", "Rust", "HTML-CSS", "Minecraft", "Summoners-War", "Chess"
    )
    async def bank(self, inter, operations: str = commands.Param(choices=["pay","request","adjust_balance"])):
        if operations == "pay":
            await self.pay_to_member(inter)
        elif operations == "request":
            await self.request_from_member(inter)
        elif operations == "adjust_balance":
            await self.adjust_user_balance(inter)
        else:
            return await inter.response.send_message("Error With Params")

    async def pay_to_member(self,inter):
        await asyncio.sleep(0.5)

        await inter.response.send_message("Enter The ID Of The Member You Wish To Pay.",ephemeral=True)
        member_id = await self.bot.wait_for('message')
        member_to_pay = disnake.utils.get(inter.guild.members, id=int(member_id.content))

        await asyncio.sleep(0.7)

        await inter.edit_original_message("Enter The Amount To Pay.")
        amount_to_pay = await self.bot.wait_for('message')

        await asyncio.sleep(0.7)

        await inter.edit_original_message("Enter The Reason.")
        reason = await self.bot.wait_for('message')

        await asyncio.sleep(0.7)

        payer = inter.author.id
        payee = member_to_pay.id if member_to_pay.id else member_id.content
        amount = int(amount_to_pay.content)
        la_reason = reason.content

        await member_id.delete()
        await amount_to_pay.delete()
        await reason.delete()

        if payee:
            now = date.today()

            with sql.connect('main.db') as mdb:
                cur = mdb.cursor()

                srch = 'SELECT bank FROM members WHERE id=?'
                srch2 = 'SELECT bank FROM members WHERE id=?'

                val = (payer,)
                val2 = (payee,)

                payer_balance = cur.execute(srch, val).fetchone()[0]
                payee_balance = cur.execute(srch2, val2).fetchone()[0]

                if payer_balance >= amount: 
                    payer_new_balance = payer_balance - amount
                    payee_new_balance = payee_balance + amount

                    srch3 = 'UPDATE members SET bank=? WHERE id=?'
                    srch4 = 'UPDATE members SET bank=? WHERE id=?'

                    val3 = (payer_new_balance,payer)
                    val4 = (payee_new_balance,payee)

                    cur.execute(srch3, val3)
                    cur.execute(srch4, val4)

                    all_transactions = cur.execute('SELECT * FROM bank_transactions').fetchall()
                    new_number = len(all_transactions) + 1

                    srch5 = 'INSERT INTO bank_transactions(id,payer,payee,date,amount,reason) VALUES (?,?,?,?,?,?,?,?)'
                    val5 = (new_number,payer,payee,amount,la_reason,now,payer_new_balance,payee_new_balance)

                    cur.execute(srch, val)

                    await self.send_notification(inter, payer, payee, amount, la_reason, payer_balance, payee_balance, payer_new_balance, payee_new_balance)
                else:
                    return await inter.edit_original_message(f"{inter.author.mention} You Do Not Have Enough Money For This Transaction! Your Balance Is Currently **${payer_balance}**.")
        else:
            return await inter.edit_original_message(f"{inter.author.mention} the member's id must be made up of numbers 0-9")

    async def request_from_member(self, inter):
        await asyncio.sleep(0.5)

        await inter.response.send_message("Enter The ID Of The Member You Wish To Pay.",ephemeral=True)
        member_id = await self.bot.wait_for('message')
        member_to_receive_from = disnake.utils.get(inter.guild.members, id=int(member_id.content))

        await asyncio.sleep(0.7)

        await inter.edit_original_message("Enter The Amount To Pay.")
        amount_to_pay = await self.bot.wait_for('message')

        await asyncio.sleep(0.7)

        await inter.edit_original_message("Enter The Reason.")
        reason = await self.bot.wait_for('message')

        await asyncio.sleep(0.7)
        
        payer = member_to_receive_from.id if member_to_receive_from.id else member_id.content
        payee = inter.author.id 
        amount = int(amount_to_pay.content)
        la_reason = reason.content

        await member_id.delete()
        await amount_to_pay.delete()
        await reason.delete()

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = "Gawther's Bank Notification System",
            description = f"{inter.author.name} Has Requested ${amount} From You. Please Accept or Deny By Entering Accept or Deny."
        ).add_field(
            name = "Other Information",
            value = "You Have 20 Minutes To Respond To This Request. If You Do Not Respond, The Command Will Need To Be Ran Again.",
            inline = False 
        ).set_thumbnail(
            url = self.bot.user.avatar
        ).set_footer(
            text = "If you feel this is an error, please contact support!"
        )

        await inter.edit_original_message("Your Request Has Been Sent.")
        await payer.send(embed=embed)
        confirmation = await self.bot.wait_for('message', timeout=1200)

        if confirmation.content.lower() == "accept":
            with sql.connect('main.db') as mdb:
                cur = mdb.cursor()

                srch = 'SELECT bank FROM members WHERE id=?'
                srch2 = 'SELECT bank FROM members WHERE id=?'

                val = (payer, )
                val2 = (payee, )

                payer_balance = cur.execute(srch, val).fetchone()[0]
                payee_balance = cur.execute(srch2, val2).fetchone()[0]

                new_payer_bal = payer_balance - amount
                new_payee_bal = payee_balance + amount

                srch3 = 'UPDATE members SET bank=? WHERE id=?'
                srch4 = 'UPDATE members SET bank=? WHERE id=?'

                val3 = (new_payer_bal, payer, )
                val4 = (new_payee_bal, payee, )

                cur.execute(srch3, val3)
                cur.execute(srch4, val4)

                await self.send_notification(inter, payer, payee, amount, la_reason, payer_balance, payee_balance, new_payer_bal, new_payee_bal)
        else:
            pass

    async def adjust_user_balance(self,inter):
        checks = ["Owners","Developers","Head Administrators","Administrators","Moderators"]

        if inter.author.top_role.name in checks:
            await inter.response.send_message("Enter The Members ID",ephemeral=True)
            member_to_adjust = await self.bot.wait_for('message')
            member_object = disnake.utils.get(inter.guild.members, id=int(member_to_adjust.content))

            await inter.edit_original_message("Enter Amount To Fix.")
            amount_to_adjust = await self.bot.wait_for('message')
            amount = int(amount_to_adjust.content)

            await inter.edit_original_message("Is This A Withdrawl (taking away) or Deposit (giving to)? Enter Withdrawl or Deposit")
            adjustment_method = await self.bot.wait_for('message')
            method = adjustment_method.content.lower()

            await inter.edit_original_message("Enter The Reason For The Adjustment")
            reason = await self.bot.wait_for('message')
            la_reason = reason.content

            await member_to_adjust.delete()
            await amount_to_adjust.delete()
            await adjustment_method.delete()
            await reason.delete()

            if member_object:
                with sql.connect('main.db') as mdb:
                    cur = mdb.cursor()

                    srch = 'SELECT bank FROM members WHERE id=?'
                    val = (member_object.id, )

                    curr_mem_bal = cur.execute(srch, val).fetchone()[0]

                    staff_member = inter.author.id

                    if method == "withdrawl":
                        new_mem_bal = curr_mem_bal - amount
                    else:
                        new_mem_bal = curr_mem_bal + amount

                    srch2 = 'UPDATE members SET bank=? WHERE id=?'
                    val2 = (new_mem_bal, member_object.id, )

                    try:
                        cur.execute(srch2, val2)
                        await self.send_notification(inter, staff_member, member_object.id, amount, la_reason, 0, curr_mem_bal, 0, new_mem_bal)
                    except:
                        return await inter.edit_original_message("There was a problem with adjusting the members balance. Please report to the Owners and Developers. Thanks -Gawther")
            else:
                return await inter.edit_original_message("That ID Is Not A Member Of This Discord. Please Enter A Valid Member ID. If You Find This As An Error, Please Report To The Owners and Developers. Thanks - Gawther")

    async def send_notification(self, inter, payer, payee, amount, reason, payer_bal, payee_bal, payer_new_bal, payee_new_bal):
        embed = disnake.Embed(
            color = disnake.Colour.green(),
            title = "Gawther's Bank Notification System",
            description = f"{payer.name} Has Paid {payee.name} The Amount Of ${amount}."
        ).add_field(
            name = "Reason",
            value = f"{reason}",
            inline = False
        ).set_thumbnail(
            url = self.bot.user.avatar
        ).set_footer(
            text = "If you did not execute this command, please contact support!"
        )

        payer_embed = embed
        payee_embed = embed

        payer_embed.add_field(
            name = "Receipt",
            value = f"Previous Balance: ${payer_bal}\nWithdrawn: ${amount}\nNew Balance: ${payer_new_bal}",
            inline = False
        )

        payee_embed.add_field(
            name = "Receipt",
            value = f"Previous Balance: ${payee_bal}\nWithdrawn: ${amount}\nNew Balance: ${payee_new_bal}",
            inline = False
        )

        await inter.edit_original_message("Please See Your DM's For Your Receipt.")

        payee_object = disnake.utils.get(inter.guild.members, id=payee)
        payer_object = disnake.utils.get(inter.guild.members, id=payer)

        await payee_object.send(embed=payee_embed)
        await payer_object.send(embed=payer_embed)

        noti_chan = disnake.utils.get(inter.guild.text_channels, name="bank_notifications")
        await noti_chan.send(embed=embed)


def setup(bot):
    bot.add_cog(BankCommands(bot))