import disnake
import sqlite3 as sql
import json

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
        await inter.response.send_message("Enter The Members ID.",ephemeral=True)
        
        member_to_pay = disnake.utils.get(inter.guild.members, id=int((await self.bot.wait_for('message')).content))

        if member_to_pay:
            await inter.channel.purge(limit=1)

            await inter.edit_original_message("Enter The Amount To Pay.")
            amount_to_pay = int((await self.bot.wait_for('message')).content)

            await inter.edit_original_message("Enter The Reason For The Payment.")
            reason = (await self.bot.wait_for('message')).content

            if all(i.isprintable() for i in reason):
                await inter.channel.purge(limit=2)

                today = date.today()

                if await self.increase_db(inter.author, member_to_pay, amount_to_pay, reason, today) == True:
                    payer_bal, payee_bal, payer_new_bal, payee_new_bal = [] # pull from database, or return as separate list from update command Ex: return True, list

                    if await self.send_successful_notification(inter, inter.author, member_to_pay, amount_to_pay, reason, payer_bal, payee_bal, payer_new_bal, payee_new_bal) == True:
                        return await inter.edit_original_message("Your Payment Has Been Successful. See DM's For Receipt.")
                    else:
                        return await inter.edit_original_message("The Notification Has Failed To Send. Contact Developers and Owners")
                else:
                    return await inter.edit_original_message("The Database Failed To Update. Contact Developers and Owners")
            else:
                return await inter.edit_original_message("The Reason Must Be A Printable String! Please use the 26-Letter English Alphabet, Numeric Values 0-9, and Normal Special Characters.")
        else:
            return await inter.edit_original_message("The Member's ID Must Be That Of A Member Currently In This Discord! Try Again!")

    async def request_from_member(self, inter):
        await inter.response.send_message("Enter The Members ID.",ephemeral=True)
        member_to_request_from = disnake.utils.get(inter.guild.members, id=int((await self.bot.wait_for('message')).content))

        if member_to_request_from:
            await inter.channel.purge(limit=1)

            await inter.edit_original_message("Enter The Amount To Request.")
            amount_to_pay = int((await self.bot.wait_for('message')).content)

            await inter.edit_original_message("Enter The Reason For The Request.")
            reason = (await self.bot.wait_for('message')).content

            if all(i.isprintable() for i in reason):
                await inter.channel.purge(limit=2)
                
                if await self.send_request_notification(inter, member_to_request_from, amount_to_pay, reason) == True:
                    today = date.today()

                    if await self.increase_db(inter.author, member_to_request_from, amount_to_pay, reason, today) == True:
                        payer_bal, payee_bal, payer_new_bal, payee_new_bal = [] # pull from database, or return as separate list from update command. Ex: return True, list

                        if await self.send_success_notification(inter, inter.author, member_to_request_from, amount_to_pay, reason, payer_bal, payee_bal, payer_new_bal, payee_new_bal) == True:
                            return await inter.edit_original_message("Your Payment Has Been Successful. See DM's For Receipt.")
                        else:
                            return await inter.edit_original_message("The Notification Has Failed To Send. Contact Developers and Owners")
                    else:
                        return await inter.edit_original_message("The Database Failed To Update. Contact Developers and Owners")
                else:
                    return await inter.edit_original_message("The Request Notification Has Failed To Send. Contact Developers and Owners")
            else:
                return await inter.edit_original_message("The Reason Must Be A Printable String! Please use the 26-Letter English Alphabet, Numeric Values 0-9, and Normal Special Characters.")
        else:
            return await inter.edit_original_message("The Member's ID Must Be That Of A Member Currently In This Discord! Try Again!")

    async def adjust_user_balance(self,inter):
        await inter.response.send_message("Enter The Members ID:",ephemeral=True)
        member_to_adjust = disnake.utils.get(inter.guild.members, id=int((await self.bot.wait_for('message')).content))

        if member_to_adjust:
            await inter.channel.purge(limit=1)

            await inter.edit_original_message("Enter The Amount To Adjust By.")
            amount_to_adjust_by = int((await self.bot.wait_for('message')).content)

            await inter.edit_original_message("Enter If Withdrawl or Deposit")
            method = (await self.bot.wait_for('message')).content.lower()

            await inter.edit_original_message("Enter The Reason For The Adjustment.")
            reason = (await self.bot.wait_for('message')).content

            if method == "withdrawl":
                await inter.channel.purge(limit=3)

                staff_member = inter.author

                if all(i.isprintable() for i in reason):
                    today = date.today()

                    if await self.decrease_db(staff_member,member_to_adjust, amount_to_adjust_by, reason, today) == True:
                        member_bal, member_new_bal = [] # pull from database, or return as separate list from update command.Ex: return True, list

                        if await self.send_adjustment_notification(inter, inter.author, member_to_adjust, amount_to_adjust_by, reason) == True:
                            return await inter.edit_original_message("The Adjustment Has Been Made. Please See The Bank Logs Channel For The Receipt. The Member Has Also Received A Notification As Well.")
                        else:
                            return await inter.edit_original_message("The Notification Failed To Send. Contact Developers and Owners")
                    else:
                        return await inter.edit_original_message("The Database Failed To Update. Contact Developers and Owners")
                else:
                    return await inter.edit_original_message("The Reason Must Be A Printable String! Please use the 26-Letter English Alphabet, Numeric Values 0-9, and Normal Special Characters.")

            elif method == "deposit":
                await inter.channel.purge(limit=3)

                staff_member = inter.author

                if all(i.isprintable() for i in reason):
                    today = date.today()

                    if await self.increase_db(member_to_adjust, amount_to_adjust_by, reason, date) == True:
                        member_bal, member_new_bal = [] # pull from database, or return as separate list from update command. Ex: return True, list

                        if await self.send_adjustment_notification(inter, inter.author, member_to_adjust, amount_to_adjust_by, reason) == True:
                            return await inter.edit_original_message("The Adjustment Has Been Made. Please See The Bank Logs Channel For The Receipt. The Member Has Also Received A Notification As Well.")
                        else:
                            return await inter.edit_original_message("The Notification Failed To Send. Contact Developers and Owners.")
                    else:
                        return await inter.edit_original_message("The Database Failed To Update. Contact Developers and Owners")
                else:
                    return await inter.edit_original_message("The Reason Must Be A Printable String! Please use the 26-Letter English Alphabet, Numeric Values 0-9, and Normal Special Characters.")
            
            else:
                await inter.channel.purge(limit=3)

                return await inter.edit_original_message("The Method Must Be Either A Withdrawl or Deposit. Try Again!")

    async def send_request_notification(self, inter, member, amount, reason):
        embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = "Gawther's Bank Notification System",
            description = f"{inter.author.name} Has Requested ${amount}GB From You. Please Enter Accept or Deny."
        ).add_field(
            name = "Reason",
            value = f"{reason}",
            inline = False
        ).set_thumbnail(
            url = self.bot.user.avatar
        )

        await member.send(embed=embed)
        
        if (await self.bot.wait_for('message')).content.lower() == "accept":
            return True
        else:
            return False

    async def send_success_notification(self, inter, payer, payee, amount, reason, payer_bal, payee_bal, payer_new_bal, payee_new_bal):
        color = disnake.Colour.random()
        title = "Gawther's Bank Notification System"

        payer_embed = disnake.Embed(
            color = color,
            title = title,
            description = f"You Paid {payee.name} ${amount}GB"
        ).add_field(
            name = "Reason",
            value = f"{reason}",
            inline = False
        ).add_field(
            name = "Receipt",
            value = f"Previous Balance: ${payer_bal}GB\nAdjusted By: $({amount})GB\nNew Balance: ${payer_new_bal}GB",
            inline = False
        ).set_thumbnail(
            url = self.bot.user.avatar
        )

        payee_embed = disnake.Embed(
            color = color,
            title = title,
            description = f"{payer.name} Paid You ${amount}GB"
        ).add_field(
            name = "Reason",
            value = f"{reason}",
            inline = False
        ).add_field(
            name = "Receipt",
            value = f"Previous Balance: ${payee_bal}GB\nAdjusted By: ${amount}GB\nNew Balance: ${payee_new_bal}GB",
            inline = False
        ).set_thumbnail(
            url = self.bot.user.avatar
        )
 
        noti_embed = disnake.Embed(
            color = color,
            title = title,
            description = f"{payer.name} Paid {payee.name} The Amount Of ${amount}GB"
        ).add_field(
            name = "Reason",
            value = f"{reason}",
            inline = False
        ).set_thumbnail(
            url = self.bot.user.avatar
        )

        try:
            await payer.send(embed=payer_embed)
            await payee.send(embed=payee_embed)
            await (disnake.utils.get(inter.guild.text_channels, name="bank_notifications")).send(embed=noti_embed)

            return True
        except:
            return False

    async def increase_db(self, payer, payee, amount, reason, date):
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT bank FROM members WHERE id=?'
            srch2 = 'SELECT bank FROM members WHERE id=?'

            val = (payer, )
            val2 = (payee, )

            payer_bal = cur.execute(srch, val).fetchone()[0]
            payee_bal = cur.execute(srch2, val2).fetchone()[0]

            if payer_bal >= amount:
                payer_new_bal = payer_bal - amount
                payee_new_bal = payee_bal + amount

                srch3 = 'UPDATE members SET bank=? WHERE id=?'
                srch4 = 'UPDATE members SET bank=? WHERE id=?'

                val3 = (payer_new_bal, payer, )
                val4 = (payee_new_bal, payee, )

                try:
                    cur.execute(srch3, val3)
                    cur.execute(srch4, val4)

                    all_transactions = cur.execute('SELECT * FROM bank_transactions').fetchall()

                    srch5 = 'INSERT INTO bank_transactions(id, payer, payee, date, amount, reason) VALUES (?,?,?,?,?,?)'
                    val5 = (len(all_transactions)+1,payer, payee, date, amount, reason)

                    try:
                        cur.execute(srch5, val5)

                        list = [payer_bal, payee_bal, payer_new_bal, payee_new_bal]

                        return True, list
                    except:
                        return False
                except:
                    return False
    
    async def decrease_db(self, staff, member, amount, reason, date):
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT bank FROM members WHERE id=?'
            val = (member.id, )

            member_bal = cur.execute(srch, val).fetchone()[0]

            new_member_bal = member_bal - amount

            srch2 = 'UPDATE members SET bank=? WHERE id=?'
            val2 = (new_member_bal, member.id, )

            try: 
                cur.execute(srch2, val2)

                all_transactions = cur.execute('SELECT * FROM bank_transactions').fetchall()

                srch3 = 'INSERT INTO bank_transactions(id, payer, payee, date, amount, reason) VALUES (?,?,?,?,?,?)'
                val3 = (len(all_transactions)+1, staff, member.id, date, amount, reason)

                try:
                    cur.execute(srch3, val3)

                    list = [member_bal, new_member_bal]

                    return True, list
                except: 
                    return False
            except:
                return False

def setup(bot):
    bot.add_cog(BankCommands(bot))