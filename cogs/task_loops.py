import disnake
import json
import sqlite3 as sql

from disnake.ext import commands
from disnake.ext import tasks

with open('./json_files/config.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

guild_id = data["guild_id"]

with open('./json_files/setup.json', 'r', encoding='utf-8-sig') as g:
    data = json.load(g)

noti_chan = data["guilds"][str(guild_id)]["restricted_channels"]["db_notifications"]


class TaskChecks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_pending.start()
        # self.check_database_for_members.start() - need to fix

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

    # @tasks.loop(hours=12)
    # async def check_database_for_members(self):
    #     await self.bot.wait_until_ready()
    #     guild = self.bot.get_guild(guild_id)

    #     with sql.connect('./databases/members.db') as membersDb:
    #         cur = membersDb.cursor()

    #         all_member_ids = cur.execute('SELECT id FROM profile').fetchall()

    #         added_members = []

    #         for member in self.bot.get_guild(guild_id).members:
    #             if member.id in all_member_ids:
    #                 pass
    #             else:
    #                 srch = 'INSERT INTO profile(id,quote,mutes,bans,warnings,kicks,dob,color,bank) VALUES (?,?,?,?,?,?,?,?,?)'
    #                 val = (member.id,"None",0,0,0,0,"None","None","None")

    #                 try:
    #                     cur.execute(srch, val)
    #                     added_members.append(member.name)
    #                 except:
    #                     terminal_channel = disnake.utils.get(guild.text_channels, name="gawther_terminal")
    #                     await terminal_channel.send("Failed To Update Database With New Members - Task Loop")

    #         embed = disnake.Embed(
    #             color=disnake.Colour.random(),
    #             title="Gawther Database Notification System",
    #             description="I have Successfully Updated The Members Table In The Database."
    #         ).add_field(
    #             name="Additional Information",
    #             value=f"{len(added_members)} New Members Added To The Database",
    #             inline=False
    #         ).set_thumbnail(
    #             url=self.bot.user.avatar
    #         ).set_footer(
    #             text="To See The Full List Of Members In The Database, Please Run /db_diag"
    #         )

    #         notification_channel = disnake.utils.get(guild.text_channels, name="db_notifications")
    #         await notification_channel.send(embed=embed)


def setup(bot):
    bot.add_cog(TaskChecks(bot))
