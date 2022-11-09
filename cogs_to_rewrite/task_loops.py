import disnake
import json
import sqlite3 as sql

from disnake.ext import commands
from disnake.ext import tasks

with open('config.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

guild_id = data["guild_id"]

with open('setup.json', 'r', encoding='utf-8-sig') as g:
    data = json.load(g)

noti_chan = data["dbNotifications"]


class TaskChecks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_pending.start()
        self.check_database_for_members.start()

    @tasks.loop(hours=24)
    async def check_pending(self):
        await self.bot.wait_until_ready()

        embed = disnake.Embed(
            color=disnake.Colour.orange(),
            title="Pending Member Verification",
            description="Below You Will Find The List Of Members Still Pending Verification.\nI Will Be Sending A Courtesy Notification To These Members In A Moment."
        ).set_thumbnail(
            url=self.bot.user.avatar
        )

        pending_members = []

        guild = self.bot.get_guild(guild_id)

        for member in guild.members:
            if member.pending == True:
                pending_members.append(member.id)

        if len(pending_members) == 0:
            embed.add_field(
                name="Members Pending Verification",
                value="No Pending Member Verifications At This Time.",
                inline=False
            )
        else:
            embed.add_field(
                name="Members Pending Verification",
                value=f"{', '.join([m.name for m in pending_members])}",
                inline=False
            )

        staff_channel_announcements = disnake.utils.get(
            guild.text_channels, name="pending_verification")
        await staff_channel_announcements.send(embed=embed)

        alerted_members = []

        for member in guild.members:
            if member.pending == True:
                alerted_members.append(member.name)

                embed = disnake.Embed(
                    color=disnake.Colour.random(),
                    title="Gawther's Member Pending Verification Notification System",
                    description=f"Hey, {member.name}. We noticed that you have not verified your account through Discord. Please go into your account settings to verify your account."
                ).add_field(
                    name="Furthermore",
                    value="Every 24 hours, Gawther will check all members for a verified account. You'll receive this message once every 24 hours until verified.",
                    inline=False
                ).set_thumbnail(
                    url=self.bot.user.avatar
                ).set_footer(
                    text="This Message Is Automated and Will Send Every 24hours Until Verification Has Been Completed, Or You Have Left The Server."
                )

                await member.send(embed=embed)

        if len(alerted_members) == 0:
            embed2 = disnake.Embed(
                color=disnake.Colour.random(),
                title="Gawther's Member Pending Verification Notification System",
                description="There Are No Members With A Pending Verification Status. No Notifications Sent."
            ).set_thumbnail(
                url=self.bot.user.avatar
            )

            await staff_channel_announcements.send(embed=embed2)
        else:
            embed2 = disnake.Embed(
                color=disnake.Colour.random(),
                title="Gawther's Member Pending Verification Notification System",
                description=f"I have Notified The Following Members"
            ).add_field(
                name="Alerted Members",
                value=f"{', '.join(alerted_members)}",
                inline=False
            ).set_thumbnail(
                url=self.bot.user.avatar
            )

            await staff_channel_announcements.send(embed=embed2)

    @tasks.loop(hours=12)
    async def check_database_for_members(self):
        await self.bot.wait_until_ready()

        with sql.connect('members.db') as mdb:
            cur = mdb.cursor()

            guild = self.bot.get_guild(guild_id)
            notification_channel = disnake.utils.get(
                guild.text_channels, id=noti_chan)
            all_guild_members = [
                member for member in guild.members if not member.bot]
            
            try:
                all_db_member_ids = [id[0] for id in cur.execute(
                    'SELECT id FROM profiles').fetchall()]
            except:
                all_db_member_ids = []

            added_members = []

            if len(all_db_member_ids) > 0:
                for member in all_guild_members:
                    if member.id in all_db_member_ids:
                        pass
                    else:
                        srch = 'INSERT INTO profiles(member,bank,quote) VALUES (?,?,?)'
                        val = (member.id, 1500, "None")

                        cur.execute(srch, val)
                        added_members.append(member.name)
            else:
                for member in guild.members:
                    srch = 'INSERT INTO profiles(member,bank,quote) VALUES (?,?,?)'
                    val = (member.id, 1500, "None")

                    added_members.append(member.name)

            embed = disnake.Embed(
                color=disnake.Colour.random(),
                title="Gawther Database Notification System",
                description="I have Successfully Updated The Members Table In The Database."
            ).add_field(
                name="Additional Information",
                value=f"{len(added_members)} New Members Added To The Database",
                inline=False
            ).set_thumbnail(
                url=self.bot.user.avatar
            ).set_footer(
                text="To See The Full List Of Members In The Database, Please Run /db_diag"
            )

            await notification_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(TaskChecks(bot))
