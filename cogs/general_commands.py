import disnake
import io
import json
import asyncio
import sqlite3 as sql

from disnake.ext import commands
from Paginator import CreatePaginator
from typing import List
from datetime import datetime

with open('config.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

guild_ids = [data["guild_id"], ]


class GeneralCommandsRewrite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="member",
        description="A command that includes all general member commands and shows options",
        guild_ids=guild_ids
    )
    @commands.has_any_role(
        "Owners", "Developers", "Head Admins", "Moderators", "Community Helpers",
        "Programming", "Gaming", "Artistry", "Nitro", "Member", "Python", "JavaScript",
        "Java", "Rust", "HTML-CSS", "Minecraft", "Summoners-War", "Chess"
    )
    async def member(self, inter, operation: str = commands.Param(
            choices=["fav_quote", "help", "ping", "rules", "server", "solved", "subscribe", "who_is"])):

        if operation == "ping":
            await self.ping(inter)
        elif operation == "server":
            await self.server(inter)
        elif operation == "who_is":
            await inter.response.send_message("Enter The Member's Id", ephemeral=True)
            member_iden = await self.bot.wait_for('message')
            await member_iden.delete()
            await self.who_is(inter, member_iden.content)
        elif operation == "fav_quote":
            await inter.response.send_message("Please Enter Your New Quote", ephemeral=True)
            quote = await self.bot.wait_for('message')
            await quote.delete()
            await self.fav_quote(inter, quote.content)
        elif operation == "solved":
            if inter.channel.type is disnake.ChannelType.public_thread:
                if inter.channel.parent.type is disnake.ChannelType.forum:
                    await self.solved(inter)
                else:
                    await inter.response.send_message("This Channel Is Not A Support Forum!\n If you find this to be an error, please use /report", delete_after=15)
            else:
                await inter.response.send_message("This Channel Is Not In The Support Forums!\nIf you find this to be an error, please use /report", delete_after=15)
        elif operation == "help":
            await self.gawther_help(inter)
        elif operation == "subscribe":
            await self.subscribe(inter)
        elif operation == "rules":
            await self.show_rules(inter)
        else:
            await inter.response.send_message("Error On Param Selection")

    async def ping(self, inter):
        latency = round(self.bot.latency, 2)

        embed = disnake.Embed(
            color=disnake.Colour.random(),
            title="Gawther's Latency",
            description=f"Hey! My latency is currently {str(latency)}ms. Would you like to report it? Please Respond With Yes or No"
        ).set_thumbnail(url=inter.guild.icon)

        await inter.response.send_message(embed=embed, ephemeral=True)
        choice = await self.bot.wait_for('message', timeout=15)

        if choice.content.lower() == "yes":
            await choice.delete()

            if latency >= 20:
                embed.add_field(
                    name="Report Information",
                    value=f"User: {inter.author.display_name} Has Reported {str(latency)}ms For Being Too High In Latency.",
                    inline=False
                ).add_field(
                    name="Report Information Cont'd",
                    value=f"If you feel that the latency is ok, please get in touch with {inter.author.display_name} to see if you can figure out the problem and assist in a solution. Thanks!",
                    inline=False
                ).set_footer(
                    text="Your Report Has Been Sent and A Staff Member Will Be In Touch. Please Be Patient"
                )

                channel = disnake.utils.get(
                    inter.guild.text_channels, name="latency_reports")
                await channel.send(embed=embed)
                await inter.edit_original_message(embed=embed)
            else:
                await inter.edit_original_message("The Latency Is Not High Enough To Report!", embed=None)

    async def server(self, inter):
        await inter.response.defer(ephemeral=True)

        owners = ', '.join(
            [m.name for m in inter.guild.members if m.top_role.name == "Owners"]) or "Applications Open"
        bots = ', '.join(
            [m.name for m in inter.guild.members if m.top_role.name == "Bots"]) or "Applications Open"
        devs = ', '.join([m.name for m in inter.guild.members if m.top_role.name ==
                         "Developers"]) or "Applications Open"
        head_admins = ', '.join(
            [m.name for m in inter.guild.members if m.top_role.name == "Head Administrators"]) or "Applications Open"
        admins = ', '.join([m.name for m in inter.guild.members if m.top_role.name ==
                           "Administrators"]) or "Applications Open"
        moderators = ', '.join(
            [m.name for m in inter.guild.members if m.top_role.name == "Moderators"]) or "Applications Open"
        comm_helpers = ', '.join(
            [m.name for m in inter.guild.members if m.top_role.name == "Community Helpers"]) or "Applications Open"

        all_roles = ', '.join(
            [r.name for r in inter.guild.roles if not r.managed])
        member_count = len([m for m in inter.guild.members if not m.bot])
        bot_count = len([b for b in inter.guild.members if b.bot])
        category_count = len([cat for cat in inter.guild.categories])
        text_channel_count = len(
            [channel for channel in inter.guild.text_channels])
        voice_channel_count = len(
            [channel for channel in inter.guild.voice_channels])

        embed = disnake.Embed(
            color=disnake.Colour.random(),
            title=f"{inter.guild.name}s' Server Information",
            description=f"Below you will find all the relative information belonging to {inter.guild.name}"
        ).set_thumbnail(url=inter.guild.icon)

        list1 = ["Owners", "Bots", "Developers", "Head Administrators",
                 "Administrators", "Moderators", "Community Helpers"]
        list2 = [owners, bots, devs, head_admins,
                 admins, moderators, comm_helpers]

        for index, value in enumerate(list1):
            embed.add_field(
                name=value,
                value=list2[index],
                inline=False
            )

        list3 = ["Members", "Bots", "Roles", "Categories",
                 "Text Channels", "Voice Channels"]
        list4 = [member_count, bot_count, len(
            all_roles), category_count, text_channel_count, voice_channel_count]

        embed2 = disnake.Embed(
            color=disnake.Colour.random(),
            title="Our Server Counts",
            description="Please See Below"
        )

        for ind, val in enumerate(list3):
            embed2.add_field(
                name=val,
                value=list4[ind],
                inline=False
            )

        embeds = [embed, embed2]
        author_id = inter.author.id
        timeout = 300

        await inter.edit_original_message(embed=embeds[0], view=CreatePaginator(embeds, author_id, timeout))

    async def who_is(self, inter, member):
        member_id = member if member is not None else inter.author.id

        if int(member_id):
            member = disnake.utils.get(inter.guild.members, id=int(member_id))

            user_embed = disnake.Embed(
                color=disnake.Colour.random(),
                title=f"Who Is. . .{member.name}",
                description="The Information You Requested Can Be Found In The Following Pages"
            ).set_image(url=member.avatar)

            user_embed2 = disnake.Embed(
                color=disnake.Colour.random(),
                title="General Information",
                description=f"""__**ID:**__\n{member.id}
                                  __**Tag:**__\n{member}
                                  __**Name:**__\n{member.name}
                                  __**Display Name:**__\n{member.display_name}
                                  __**Nickname:**__\n{member.nick}
                                  __**Created At:**__\n{member.created_at.__format__('%m/%d/%Y %H:%M:%S')}
                                  __**Joined At:**__\n{member.joined_at.__format__('%m/%d/%Y %H:%M:%S')}
                                  __**Premium Since:**__\n{member.premium_since}
                                  __**Discord Rep?**__\n{member.system}"""
            ).set_thumbnail(url=member.avatar)

            user_embed3 = disnake.Embed(
                color=disnake.Colour.random(),
                title="Mutual Guilds",
                description=f"{', '.join([g.name for g in member.mutual_guilds])}"
            ).set_thumbnail(url=member.avatar)

            all_activities = [a for a in member.activities]
            all_activs = ""

            if 0 < len(all_activities) < 2:
                ', '.join(all_activities)
            else:
                all_activs = "None"

            user_embed4 = disnake.Embed(
                color=disnake.Colour.random(),
                title="Activities",
                description=f"{all_activs}"
            ).set_thumbnail(url=member.avatar)

            user_embed5 = disnake.Embed(
                color=disnake.Colour.random(),
                title="Roles",
                description=f"Top Role: {member.top_role.name}\nAll Roles: {', '.join([r.name for r in member.roles])}"
            ).set_thumbnail(url=member.avatar)

            mem_voice = "True" if member.voice else "False"

            user_embed6 = disnake.Embed(
                color=disnake.Colour.random(),
                title="Status'",
                description=f"""__**Desktop Status:**__\n{member.desktop_status}
                                  __**Mobile Status:**__\n{member.mobile_status}
                                  __**Online Status:**__\n{member.status}
                                  __**Web Status:**__\n{member.web_status}
                                  __**Voice Status:**__\n{mem_voice}"""
            ).set_thumbnail(
                url=member.avatar
            )

            user_embed7 = disnake.Embed(
                color=disnake.Colour.random(),
                title="Reputation Information",
                description="Gawther's Reputations Are Currently Under Development. Please Check Back For Regular Updates."
            ).set_thumbnail(
                url=member.avatar
            )

            user_embed8 = disnake.Embed(
                color=disnake.Colour.random(),
                title="Bank Information",
                description="Gawther Is Currently Handling A Poll For Whether Or Not You Guys Want Your Current Bank Balance To Show On This Command."
            ).add_field(
                name="What To Do?",
                value="Head over to the Support threads and look for the polls thread for Should Bank Balance Be Public? and enter your response.",
                inline=False
            ).set_thumbnail(
                url=member.avatar
            )

            embeds = [user_embed, user_embed2, user_embed3,
                      user_embed4, user_embed5, user_embed6,
                      user_embed7, user_embed8]

            timeout = 300
            author_id = inter.author.id

            await inter.edit_original_message(embed=embeds[0], view=CreatePaginator(embeds, author_id, timeout))
        else:
            await inter.edit_original_message("The member_id Must Be A Number!", delete_after=10, ephemeral=True)

    async def fav_quote(self, inter, quote):
        with sql.connect('main.db') as mdb:
            cur = mdb.cursor()

            def update_quote():
                cur.execute("UPDATE members SET quote=? WHERE id=?",
                            (quote, inter.author.id))
                try:
                    mdb.commit()
                    return True
                except:
                    return False

            def get_current_quote():
                cur.execute("SELECT quote FROM members WHERE id=?",
                            (inter.author.id,))
                # <-- Temp index 1st value -- [("some quote"),]
                return cur.fetchone()[0]

        cur_quote = get_current_quote()
        tf_check = update_quote()

        if tf_check is True:
            embed = disnake.Embed(
                color=disnake.Colour.random(),
                title="Gawther Database Notification System",
                description="You've Updated Your Favorite Quote!"
            ).add_field(
                name="Previous Quote",
                value=cur_quote,
                inline=False
            ).add_field(
                name="New Quote",
                value=quote,
                inline=False
            ).set_thumbnail(
                url=self.bot.user.avatar
            ).set_footer(
                text="If you feel this has been done in error, please contact support!"
            )

            await inter.edit_original_message(embed=embed)
        else:
            await inter.edit_original_message(f"{inter.author.mention}, There was an issue with updating your favorite quote. Please get in touch with support!")
            log_channel = disnake.utils.get(
                inter.guild.text_channels, name="fav-quote_logs")
            await log_channel.send(f"{inter.author} Attempted To Update Their Quote In The Database, And The Database Failed. Please See Terminal.")

    async def solved(self, inter):
        await inter.response.send_message(":exclamation: This Thread Has Been Closed. Do Not Type In This Channel Anymore. :exclamation:")
        await asyncio.sleep(1)
        await inter.edit_original_message(":eyeglasses: Reading and :pen_fountain: Writing Message To A :notebook: Text File For You. . . :warning: Please Wait :warning: . . .")
        await asyncio.sleep(1.5)

        purged = await inter.channel.purge(limit=None)

        _file = self.delete_messages_log(purged)

        embed = disnake.Embed(
            color=disnake.Colour.random(),
            title="Gawther Transcript Service Notification",
            description="Attached You Will Find A Text File Containing All Messages From Your Support Channel."
        ).set_thumbnail(url=self.bot.user.avatar)

        await inter.author.send(embed=embed, file=_file)

        await asyncio.sleep(2)
        await inter.channel.edit(locked=True, archived=True)
        await inter.channel.delete()

    """Does Not Need To Be Asyncronous Function"""

    def delete_messages_log(self, messages: List[disnake.Message]) -> disnake.File:
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
            _file.write(f'{json.dumps(line, indent=2)}\n')

        _file.seek(0)
        return disnake.File(_file, filename=f"Deleted_{datetime.now()}.txt")

    async def gawther_help(self, inter):
        await inter.response.defer(ephemeral=True)

        with open('setup.json', 'r', encoding='utf-8-sig') as file:
            data = json.load(file)

            member_commands = []
            staff_commands = []

            member_embeds = []
            staff_embeds = []

            embeds = {}

            print("arrays and dicts created")

            # 1. Build member_commands list
            for command in information["members"]:
                member_commands.append(command)

            print("iteration one done")

            # 2. Build staff_commands list
            for command in information["staff"]:
                staff_commands.append(command)

            print("iteration two done")

            # 3. Build member_embeds list
            for command in member_commands:
                embed = disnake.Embed(
                    title=command,
                    description=information["members"][command]["desc"],
                    color=0x00ff00
                )
                embed.add_field(
                    name="Command",
                    value=information["members"][command]["command"],
                    inline=False
                )
                embed.add_field(
                    name="Rests",
                    value=information["members"][command]["rests"],
                    inline=False
                )
                member_embeds.append(embed)

            print("interation three done")

            # 4. Build staff_embeds list
            for command in staff_commands:
                embed = disnake.Embed(
                    title=command,
                    description=information["staff"][command]["desc"],
                    color=0x00ff00
                )
                embed.add_field(
                    name="Command",
                    value=information["staff"][command]["command"],
                    inline=False
                )
                embed.add_field(
                    name="Rests",
                    value=information["staff"][command]["rests"],
                    inline=False
                )
                staff_embeds.append(embed)

            print("iteration four done")

            # 5. Build embeds dictionary
            embeds["member"] = member_embeds
            embeds["staff"] = staff_embeds

            print(member_embeds)
            print(staff_embeds)

        leading_embed = disnake.Embed(
            color=disnake.Colour.random(),
            title=information["intro"]["title"],
            description=information["intro"]["desc"]
        ).set_thumbnail(url=self.bot.user.avatar)

        if inter.author.top_role.name in ["Owners", "Developers", "Head Administrators", "Administrators", "Moderators", "Community Helpers"]:
            list_of_embeds = embeds["member"] + embeds["staff"]
            list_of_embeds.insert(0, leading_embed)
            print(list_of_embeds)
        else:
            list_of_embeds = embeds["member"]
            list_of_embeds.insert(0, leading_embed)
            print(list_of_embeds)

        author = inter.author
        timeout = 300
        await asyncio.sleep(5)
        await inter.edit_original_message(embed=list_of_embeds[0], view=CreatePaginator(list_of_embeds, author, timeout))

    async def subscribe(self, inter):
        await inter.response.send_message("Gawther's Subscription Options Are Still In The Workings. Please Check Back Frequently For Updates!", delete_after=15)

    async def show_rules(self, inter):
        await inter.response.defer(ephemeral=True)

        embed = disnake.Embed(
            color=disnake.Colour.random(),
            title="Gawther's Rules",
            description="In The Following Pages Are The Rules For The Gawther Platform As A Whole."
        ).set_thumbnail(
            url=self.bot.user.avatar
        ).set_footer(
            text="If you would like to see a new rule, edit to a current rule, or appeal an existing rule, please use /rules"
        )

        embed2 = disnake.Embed(
            color = disnake.Colour.random(),
            title = "Gawther's Punishment Table",
            description = "In The Following Pages Are The Punishment Table Tiers For The Gawther Platform As A Whole."
        ).set_thumbnail(
            url = self.bot.user.avatar
        ).set_footer(
            text = "If you would like to see a new table item, edit to a current table item, or appeal an existing table item, please use /table"
        )

        all_rule_embeds = []
        all_rule_embeds.insert(0, embed)

        with open('rules.json', 'r', encoding='utf-8-sig') as g:
            data = json.load(g)

            for i in data["rules"]:
                rule_num = i
                rule_name = data["rules"][i]["name"]
                rule_desc = data["rules"][i]["desc"]

                all_rule_embeds.append(await self.build_embed(rule_num, rule_name, rule_desc))

        all_punish_embeds = []
        all_punish_embeds.insert(0, embed2)

        with open('rules.json','r',encoding='utf-8-sig') as h:
            data = json.load(h)

            for j in data["punishmentTable"]:
                table_num = j
                table_name = data["punishmentTable"][table_num]["name"]
                table_desc = data["punishmentTable"][table_num]["desc"]

                all_punish_embeds.append(await self.build_embed(table_num, table_name, table_desc))

        all_embeds = all_rule_embeds + all_punish_embeds

        await inter.edit_original_message(embed=all_embeds[0], view=CreatePaginator(all_embeds, inter.author.id, 300))

    async def build_embed(self, a, b, c):
        embed = disnake.Embed(
            color=disnake.Colour.random(),
            title=f"__{a}__",
            description=f"**{b}**"
        ).add_field(
            name="\u200b",
            value=c,
            inline=False
        ).set_thumbnail(
            url=self.bot.user.avatar
        )

        return embed


def setup(bot):
    bot.add_cog(GeneralCommandsRewrite(bot))
