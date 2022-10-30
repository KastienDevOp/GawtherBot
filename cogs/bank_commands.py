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

    async def pay_to_member(self,inter):
        await inter.response.send_message("Enter The Member ID or Discord Tag", ephemeral=True)

        user_entry = (await self.bot.wait_for('message')).content

        payer = inter.author

        try:
            payee = disnake.utils.get(inter.guild.members, id=int(user_entry))
        except:
            payee = disnake.utils.get(inter.guild.members, name=user_entry)

        if payee:
            await inter.edit_original_message("Enter The Amount To Pay")
            amount = int((await self.bot.wait_for('message')).content)

            if amount:
                await inter.edit_original_message("Enter The Reason For The Payment")
                reason = (await self.bot.wait_for('message')).content

                if reason:
                    await inter.edit_original_message(f"Sending Payment Of ${amount} To {payee.name}. . .Please Wait. . .")
                    await asyncio.sleep(1.5)

                    today = date.today()

                    payer_old_bal, payee_old_bal, payer_new_bal, payee_new_bal = await self.update_database(payer, payee, amount, reason, today)

                    try:
                        notification_check = await self.send_notification(inter, payer, payee, payer_old_bal, payee_old_bal, payer_new_bal, payee_new_bal, amount, today, reason)

                        if notification_check == True:
                            await inter.channel.purge(limit=3)

                            return await inter.edit_original_message("Your Transaction Has Processed Successfully. Please See Your DM's For Your Receipt.")
                        else:
                            return await inter.edit_original_message("Your Transaction Has Failed. Please Contact Support For Assistance, If Needed.")
                    except:
                        print("Failed To Send Notification")
                        return False
                else:
                    return await inter.edit_original_message("The Reason Must Be A Printable String! Please Use The Following:\n26-Letter English Alphabet\n0-9 Numeric Values\nNormal Special Characters\n\nIf This Is An Error, Contact Developers")
            else:
                return await inter.edit_original_message("The Amount Must Be A Whole Number! If This Is An Error, Contact Developers")
        else:
            return await inter.edit_original_message("The Member Must Be Apart Of This Guild! If This Is An Error, Contact Developers")

    async def request_from_member(self, inter):
        await inter.response.send_message("Enter The Member ID or Discord Tag", ephemeral=True)

        user_entry = (await self.bot.wait_for('message')).content

        """
        THIS FUNCTION IS WRITTEN EXTREMELY SIMILAR TO THE PAY_TO_MEMBER FUNCTION!
        BE SURE TO PAY ATTENTION TO THE SWAP BETWEEN PAYER AND PAYEE SINCE WE'RE
        REQUESTING AND NOT PAYING!
        """

        payee = inter.author
        
        try:
            payer = disnake.utils.get(inter.guild.members, id=int(user_entry))
        except:
            payer = disnake.utils.get(inter.guild.members, name=user_entry)

        if payer:
            await inter.edit_original_message("Enter The Amount To Request")
            amount = int((await self.bot.wait_for('message')).content)

            if amount:
                await inter.edit_original_message("Enter The Reason For The Request")
                reason = (await self.bot.wait_for('message')).content

                if reason:
                    await inter.edit_original_message(f"Sending Your Request Of ${amount} GB To {payer.name}. . .Please Wait. . .")
                    await asyncio.sleep(1.5)

                    request_check = await self.send_request(payer,payee,amount,reason)

                    if request_check == True:
                        today = date.today()

                        request_written_check = await self.write_request(payer, payee, amount, today, reason)

                        if request_written_check == True:
                            request_sent_check = await self.send_request(payer, payee, amount, reason)

                            if request_sent_check == True:
                                await inter.channel.purge(limit=3)

                                return await inter.edit_original_message("Your Request Has Been Successfully Sent. You Will Be Notified Once A Decision Has Been Made.")
                            else:
                                return await inter.edit_original_message(f"The Request Notification Failed To Send. Contact Developers\n[BOT][ERROR]: [LINE: 128]: Failed To Send Notificaiton To Target Member.")
                        else:
                            return await inter.edit_original_message(f"The Request Failed To Send. Contact Developers\n[DATABASE][ERROR]: [LINE: 130]: Failed To Writed To bank_requests.")
                    else:
                        return await inter.edit_original_message(f"{payer.name} Has Denied Your Request For ${amount} GB.")
                else:
                    return await inter.edit_original_message("The Reason Must Be A Printable String! Please Use The Following:\n26-Letter English Alphabet\n0-9 Numeric Values\nNormal Special Characters\n\nIf This Is An Error, Contact Developers")
            else:
                return await inter.edit_original_message("The Amount Must Be A Whole Number! If This Is An Error, Contact Developers")
        else:
            return await inter.edit_original_message("The Member Must Be Apart Of This Guild! If This Is An Error, Contact Developers")

    async def write_request(self,payer,payee,amount,today,reason):
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            new_num = len(cur.execute('SELECT * FROM bank_requests').fetchall()) + 1

            srch = 'INSERT INTO bank_requests(id, payer, payee, amount, date, reason, paid) VALUES (?,?,?,?,?,?,?)'
            val = (new_num, payer.id, payee.id, amount, today, reason, "False")

            try:
                cur.execute(srch, val)
                return True
            except:
                return False

    async def send_request(self,payer,payee,amount,reason):
        embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = "Gawther's Bank Notification System",
            description = f"{payee.name} Has Request ${amount} GB From You."
        ).add_field(
            name = "Reason",
            value = f"{reason}",
            inline = False
        ).add_field(
            name = "How Do I Pay?",
            value = "Use the command `/bank pay_request`",
            inline = False
        ).set_thumbnail(
            url = self.bot.user.avatar
        )

        try:
            await payer.send(embed=embed)
            return True
        except:
            print("Failed To Send Request Notification")
            return False

    async def get_all_requests(self,inter):
        await inter.response.send_message("Looking Up Your Requests. . .Just A Moment. . .", ephemeral=True)

        payer = inter.author
        request_check, all_request_embeds = await self.get_active_payment_requests(inter,payer)

        if request_check == True:
            await inter.edit_original_message(
                f"You Have {len(all_request_embeds)} Requests Open.\n \
                    Please Enter The Number Of The Report You Wish To Pay",
                embed=all_request_embeds[0],
                view=CreatePaginator(all_request_embeds,inter.author.id, 700)
            )
        else:
            return await inter.edit_original_message("There Are No Active Requests At This Time!")

    async def get_active_payment_requests(self,inter,payer):
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT * FROM bank_requests WHERE payer=? AND paid=?'
            val = (payer.id, "False", )

            all_results = cur.execute(srch, val).fetchall()

            if all_results:

                all_embeds = []

                for request in all_results:
                    num, payer, payee, amount, date, reason, paid = request
                    
                    all_embeds.append(await self.create_embed(inter, num, payee, amount, date, reason, paid))

                return True, all_embeds
            else:
                print("Failed To Pull Requests From Database")
                await inter.edit_original_message("[DATABASE][ERROR]: Either You Have No Open Requests, or The Requests Failed To Pull. Contact Support.")
                return False, None

    async def create_embed(self,inter,num,payee,amount,date,reason,paid):
        payee_object = disnake.utils.get(inter.guild.members, id=payee)

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = "Gawther's Bank Notificaiton System",
            description = "Here Are The Reqeusts You Asked For :smile:"
        ).add_field(
            name = f"Request #{num}",
            value = f"Requester: {payee_object.name}\nAmount Requested: ${amount} GB\nDate: {date}",
            inline = False
        ).add_field(
            name = f"Reason",
            value = f"{reason}",
            inline = False
        ).add_field(
            name = "Paid?",
            value = f"{paid}",
            inline = False
        ).add_field(
            name = "How Do I Pay?",
            value = "To Pay Off A Request, Use The `/bank pay_request` command"
        ).set_thumbnail(
            url = self.bot.user.avatar
        ).set_footer(
            text = "If you find any active requests to be an error, contact developers"
        )

        try:
            return embed
        except:
            print("Failed To Create Embed {} {}".format(date, amount))

    async def pay_requests(self, inter):
        await inter.response.send_message("Enter The Number Of The Request To Pay",ephemeral=True)
        num_of_request = int((await self.bot.wait_for('message')).content)
        await asyncio.sleep(0.5)

        payer = inter.author

        if num_of_request:
            await inter.channel.purge(limit=1)
            pay_check, request = await self.get_request(payer, num_of_request)

            if pay_check == True:
                pay_num, la_payer, la_payee, amount, la_date, reason, paid = request
                payee = disnake.utils.get(inter.guild.members, id=int(la_payee))

                today = date.today()

                la_check, payer_old_bal, payee_old_bal, payer_new_bal, payee_new_bal = await self.update_database(payer, payee, amount, reason, today)

                if la_check == True:
                    notification_check = await self.send_notification(inter, payer, payee, payer_old_bal, payee_old_bal, payer_new_bal, payee_new_bal, amount, today, reason)

                    if notification_check == True:
                        paid = "True"
                        updated_table = await self.update_request_table(pay_num, paid)

                        if updated_table == True:
                            await inter.channel.purge(limit=3)

                            return await inter.edit_original_message("Your Transaction Has Processed Successfully. Please See Your DM's For Your Receipt.")
                        else:
                            return await inter.edit_original_message("[DATABASE][ERROR]: The Request Table Failed To Update Payment Status. Contact Developers.")
                    else:
                        return await inter.edit_original_message("Your Transaction Has Failed. Please Contact Support For Assistance, If Needed.")
                else:
                    print("Failed To Send Notification")
                    return False              
        else:
            return await inter.edit_original_message("That Number Request Does Not Exist/Belong To You! Try Again!")

    async def update_request_table(self,num,status):
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'UPDATE bank_requests SET paid=? WHERE id=?'
            val = (status, num, )

            try:
                cur.execute(srch, val)
                return True
            except:
                print("Failed To Update Request Table.")
                return False

    async def get_request(self, payer, num):
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT * FROM bank_requests WHERE id=? AND payer=?'
            val = (num, payer.id,)

            request_information = cur.execute(srch, val).fetchone()

            if request_information:
                return True, request_information
            else:
                return False, None

    async def update_database(self, payer, payee, amount, reason, date):
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT bank FROM members WHERE id=?'
            srch2 = 'SELECT bank FROM members WHERE id=?'

            val = (payer.id, )
            val2 = (payee.id, )

            payer_curr_bal = cur.execute(srch, val).fetchone()[0]
            payee_curr_bal = cur.execute(srch2, val2).fetchone()[0]

            if payer_curr_bal >= amount:
                payer_new_bal = payer_curr_bal - amount
                payee_new_bal = payee_curr_bal + amount

                srch3 = 'UPDATE members SET bank=? WHERE id=?'
                srch4 = 'UPDATE members SET bank=? WHERE id=?'

                val3 = (payer_new_bal, payer.id, )
                val4 = (payee_new_bal, payee.id, )

                try:
                    cur.execute(srch3, val3)
                    cur.execute(srch4, val4)

                    new_trans_id = len(cur.execute('SELECT * FROM bank_transactions').fetchall()) + 1

                    srch5 = 'INSERT INTO bank_transactions(id, payer, payee, date, amount, reason) VALUES (?,?,?,?,?,?)'
                    val5 = (new_trans_id, payer.id, payee.id, date, amount, reason)

                    try:
                        cur.execute(srch5, val5)

                        return True, payer_curr_bal, payee_curr_bal, payer_new_bal, payee_new_bal
                        
                    except:
                        print("Failed To Write New Transaction")
                        return False, None, None, None, None

                except:
                    print("Failed To Update Balances")
                    return False, None, None, None, None
            else:
                await payer.send("You Do Not Have Enough In Your Account To Cover This Transaction. Current Balance: ${}".format(payer_curr_bal))
                return False, None, None, None, None

    async def adjust_user_balance(self,inter):
        await asyncio.sleep(0.5)
        await inter.response.send_message("Enter Member ID or Name",ephemeral=True)
        user_input = (await self.bot.wait_for('message')).content

        try:
            payee = disnake.utils.get(inter.guild.members, id=int(user_input))
        except:
            payee = disnake.utils.get(inter.guild.members, name=user_input)

        payer = inter.guild

        if payee:
            await inter.channel.purge(limit=1)
            await inter.edit_original_message("Enter Amount To Adjust By")
            amount = int((await self.bot.wait_for('message')).content)

            if amount:
                await inter.channel.purge(limit=1)
                await inter.edit_original_message("Enter The Reason For The Adjustment")
                reason = (await self.bot.wait_for('message')).content

                if reason:
                    await inter.channel.purge(limit=1)
                    await inter.edit_original_message("Enter Method Of Adjustment: Withdrawl or Deposit")
                    method = (await self.bot.wait_for('message')).content.lower()
                    today = date.today()

                    if method == "withdrawl":
                        await inter.channel.purge(limit=1)
                        confirmation, payer_old_bal, payee_old_bal, payer_new_bal, payee_new_bal = await self.decrease_member_bank(inter, payer, payee, amount, method, reason, today)

                        if confirmation == True:
                            notification_check = await self.send_adjustment_notification(inter, method, payer, payee, payer_old_bal, payee_old_bal, payer_new_bal, payee_new_bal, amount, reason)

                            if notification_check == True:
                                return await inter.edit_original_message("You've Adjusted The Members Balance Accordingly. Please See Your DM's For A Receipt.")
                            else:
                                return await inter.edit_original_message("Your Adjustment Failed. Contact Developers.")
                        else:
                            return await inter.edit_original_message("[DATABASE][ERROR]: Failed To Decrease Member's Bank, Contact Developers")
                    elif method == "deposit":
                        await inter.channel.purge(limit=1)
                        confirmation, payer_old_bal, payee_old_bal, payer_new_bal, payee_new_bal = await self.increase_member_bank(inter, payer, payee, amount, method, reason, today)

                        if confirmation == True:
                            notification_check = await self.send_adjustment_notification(inter, method, payer, payee, payer_old_bal, payee_old_bal, payer_new_bal, payee_new_bal, amount, reason)

                            if notification_check == True:
                                return await inter.edit_original_message("You've Adjusted The Members Balance Accordingly. Please See Your DM's For A Receipt.")
                            else:
                                return await inter.edit_original_message("Your Adjustment Failed. Contact Developers.")
                        else:
                            return await inter.edit_original_message("[DATABASE][ERROR]: Failed To Decrease Member's Bank, Contact Developers")
                    else:
                        return await inter.edit_original_message("The Method Must Be Withdrawl or Deposit! If This Is An Error, Contact Developers")
                else:
                    return await inter.edit_original_message("The Reason Must Be A Printable String! Please Use The Following:\n26-Letter English Alphabet\n0-9 Numeric Values\nNormal Special Characters\n\nIf This Is An Error, Contact Developers")
            else:
                return await inter.edit_original_message("The Amount Must Be A Whole Number! If This Is An Error, Contact Developers")
        else:
            return await inter.edit_original_message("The Member Must Be Apart Of This Guild! If This Is An Error, Contact Developers")

    async def increase_member_bank(self, inter, payer, payee, amount, method, reason, today):
        async def update_guild_bank_balance(inter, amount):
            with open('setup.json','r',encoding='utf-8-sig') as stuff:
                data = json.load(stuff)

                curr_bank_bal = data["guild_bank"]
                bank_gone_empty_count = data["bank_gone_empty_count"]

                new_bank_bal = curr_bank_bal - amount
                time = bank_gone_empty_count + 1

                if new_bank_bal == 0:
                    role_to_mention = disnake.utils.get(inter.guild.roles, name = "Owners")
                    channel_to_mention_in = disnake.utils.get(inter.guild.text_channels, name="staff-announcements")

                    msg = await channel_to_mention_in.send(f"{role_to_mention.mention}, The Guild Bank Has Reached $0 GB. This has happened {time} time(s).")
                    await msg.pin()

                    data["guild_bank"] = new_bank_bal
                    data["bank_gone_empty_count"] = time

                    with open('setup.json','w+',encoding='utf-8-sig') as new:
                        data = json.dump(data, new, indent=4)

                        try:
                            return True, curr_bank_bal, new_bank_bal
                        except:
                            print("Failed To Update Guild Bank #1")
                            return False, None, None, None
                else:
                    data["guild_bank"] = new_bank_bal

                    try:
                        with open('setup.json','w+',encoding='utf-8-sig') as new:
                            data = json.dump(data, new, indent=4)

                            return True, curr_bank_bal, new_bank_bal
                    except:
                        print("Failed To Update Guild Bank #2")
                        return False, None, None, None

        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT bank FROM members WHERE id=?'
            val = (payee.id, )

            curr_payee_bal = cur.execute(srch, val).fetchone()[0]

            if curr_payee_bal:
                new_payee_bal = curr_payee_bal + amount

                srch2 = 'UPDATE members SET bank=? WHERE id=?'
                val2 = (new_payee_bal, payee.id, )

                try:
                    cur.execute(srch2, val2)

                    new_num = len(cur.execute('SELECT * FROM bank_adjustment_logs').fetchall()) + 1

                    srch3 = 'INSERT INTO bank_adjustment_logs(id,staff,member,amount,method,reason,date) VALUES (?,?,?,?,?,?,?)'
                    val3 = (new_num, payer.id, payee.id, amount, method, reason, today)

                    try:
                        cur.execute(srch3, val3)

                        json_check, curr_bank_bal, new_bank_bal = await update_guild_bank_balance(inter, amount)

                        if json_check == True:
                            return True, curr_bank_bal, curr_payee_bal, new_bank_bal, new_payee_bal
                        else:
                            return await inter.edit_original_message("[JSON][ERROR]: Failed To Update Guild Bank. Contact Developers")
                    except:
                        print("Failed To Updated Logs")
                        return False, None, None, None, None
                except:
                    print("Failed To Update Members Balance")
                    return False, None, None, None, None
            else:
                print("Failed To Pull Member Balance From Database")
                return False, None, None, None

    async def decrease_member_bank(self, inter, payer, payee, amount, method, reason, today):
        async def update_guild_bank_balance(inter, amount):
            with open('setup.json','r',encoding='utf-8-sig') as stuff:
                data = json.load(stuff)

                curr_bank_bal = data["guild_bank"]
                bank_gone_empty_count = data["bank_gone_empty_count"]

                new_bank_bal = curr_bank_bal + amount
                time = bank_gone_empty_count + 1

                if new_bank_bal == 0:
                    role_to_mention = disnake.utils.get(inter.guild.roles, name = "Owners")
                    channel_to_mention_in = disnake.utils.get(inter.guild.text_channels, name="staff-announcements")

                    msg = await channel_to_mention_in.send(f"{role_to_mention.mention}, The Guild Bank Has Reached $0 GB. This has happened {time} time(s).")
                    await msg.pin()

                    data["guild_bank"] = new_bank_bal
                    data["bank_gone_empty_count"] = time

                    with open('setup.json','w+',encoding='utf-8-sig') as new:
                        data = json.dump(data, new, indent=4)

                        try:
                            return True, curr_bank_bal, new_bank_bal
                        except:
                            print("Failed To Update Guild Bank #1")
                            return False, None, None, None
                else:
                    data["guild_bank"] = new_bank_bal

                    try:
                        with open('setup.json','w+',encoding='utf-8-sig') as new:
                            data = json.dump(data, new, indent=4)

                            return True, curr_bank_bal, new_bank_bal
                    except:
                        print("Failed To Update Guild Bank #2")
                        return False, None, None, None

        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            srch = 'SELECT bank FROM members WHERE id=?'
            val = (payee.id, )

            curr_payee_bal = cur.execute(srch, val).fetchone()[0]

            if curr_payee_bal:
                new_payee_bal = curr_payee_bal - amount

                srch2 = 'UPDATE members SET bank=? WHERE id=?'
                val2 = (new_payee_bal, payee.id, )

                try:
                    cur.execute(srch2, val2)

                    new_num = len(cur.execute('SELECT * FROM bank_adjustment_logs').fetchall()) + 1

                    srch3 = 'INSERT INTO bank_adjustment_logs(id,staff,member,amount,method,reason,date) VALUES (?,?,?,?,?,?,?)'
                    val3 = (new_num, payer.id, payee.id, amount, method, reason, today)

                    try:
                        cur.execute(srch3, val3)

                        json_check, curr_bank_bal, new_bank_bal = await update_guild_bank_balance(inter, amount)

                        if json_check == True:
                            return True, curr_bank_bal, curr_payee_bal, new_bank_bal, new_payee_bal
                        else:
                            return await inter.edit_original_message("[JSON][ERROR]: Failed To Update Guild Bank. Contact Developers")
                    except:
                        print("Failed To Updated Logs")
                        return False, None, None, None, None
                except:
                    print("Failed To Update Members Balance")
                    return False, None, None, None, None
            else:
                print("Failed To Pull Member Balance From Database")
                return False, None, None, None

    async def send_notification(self, inter, payer, payee, payer_old_bal, payee_old_bal, payer_new_bal, payee_new_bal, amount, reason):
        payer_embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = "Gawther's Bank Notification System",
            description = f"You Paid {payee.name} ${amount} GB"
        ).add_field(
            name = "Reason",
            value = f"{reason}",
            inline = False
        ).add_field(
            name = "Receipt",
            value = f"Previous Balance: ${payer_old_bal} GB\nAmount Withdrawn: ${amount} GB\nNew Balance: ${payer_new_bal} GB",
            inline = False
        ).set_thumbnail(
            url = self.bot.user.avatar
        ).set_footer(
            text = "If you feel this was done in error, or without your consent, then please contact support!"
        )

        payee_embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = "Gawther's Bank Notification System",
            description = f"{payer.name} Has Paid You ${amount} GB"
        ).add_field(
            name = "Reason",
            value = f"{reason}",
            inline = False
        ).add_field(
            name = "Receipt",
            value = f"Previous Balance: ${payee_old_bal} GB\nAmount Deposited: ${amount} GB\nNew Balance: ${payee_new_bal} GB",
            inline = False
        ).set_thumbnail(
            url = self.bot.user.avatar
        ).set_footer(
            text = "If you feel this was done in error, or without your consent, then please contact support!"
        )

        noti_embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = "Gawther's Bank Notification System",
            description = f"{payer.name} Has Paid {payee.name} ${amount} GB"
        ).add_field(
            name = "Reason",
            value = f"{reason}",
            inline = False
        ).set_thumbnail(
            url = self.bot.user.avatar
        )

        try:
            await payer.send(embed=payer_embed)
            
            try:
                await payee.send(embed=payee_embed)
                
                try:
                    await (disnake.utils.get(inter.guild.text_channels, name="bank_notifications")).send(embed=noti_embed)

                    return True
                except:
                    print("Failed To Send To Notification Channel")
                    return False
            except:
                print("Failed To Send Notification To Payee")
                return False
        except:
            print("Failed To Send Notification To Payer")
            return False

    async def send_adjustment_notification(self, inter, method, payer, payee, payer_old_bal, payee_old_bal, payer_new_bal, payee_new_bal, amount, reason):
        payee_embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = "Gawther's Bank Adjustment Notification System",
            description = f"Your Account Has Been Adjusted By: {payer.name}"
        ).set_thumbnail(
            url = self.bot.user.avatar
        ).set_footer(
            text = "If you feel this was done in error, please contact support"
        )

        if method == "withdrawl":
            payee_embed.add_field(
                name = "Your Account Was Debited Because. . .",
                value = f"{reason}",
                inline = False
            ).add_field(
                name = "Receipt",
                value = f"Previous Balance: ${payee_old_bal} GB\nAdjusted By: $({amount}) GB\nNew Balance: ${payee_new_bal} GB",
                inline = False
            )
        else:
            payee_embed.add_field(
                name = "Your Account Was Credited Because. . .",
                value = f"{reason}",
                inline = False
            ).add_field(
                name = "Receipt",
                value = f"Previous Balance: ${payee_old_bal} GB\nAdjusted By: ${amount} GB\n New Balance: ${payee_new_bal} GB",
                inline = False
            )

        noti_embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = "Gawther's Bank Adjustment Notification System",
            description = f"{inter.author.name} adjusted {payee.name}'s Balance By ${amount} GB"
        ).add_field(
            name = "Reason",
            value = f"{reason}",
            inline = False
        ).add_field(
            name = "Guild Bank Details",
            value = f"Previous Balance ${payer_old_bal} GB\nAdjusted By ${amount} GB\nNew Balance: ${payer_new_bal} GB",
            inline = False
        ).set_thumbnail(
            url = self.bot.user.avatar
        )

        try:
            await payee.send(embed=payee_embed)
            
            try:
                await (disnake.utils.get(inter.guild.text_channels, name="bank_notifications")).send(embed=noti_embed)

                return True
            except:
                print("Failed To Send To Notification Channel")
                return False
        except:
            print("Failed To Send Notification To Payee")
            return False

def setup(bot):
    bot.add_cog(BankCommands(bot))