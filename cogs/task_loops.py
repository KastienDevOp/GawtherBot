import disnake
import json
import random

from disnake.ext import commands
from disnake.ext import tasks
from helpers import get_guild_id

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
        self.change_presence.start()

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

    """
    Setting `Playing` Status
    await bot.change_presence(activity=disnake.Game(name="a game"))

    Setting `Streaming` Status
    await bot.change_presence(activity=disnake.Streaming(name="My Stream", url=my_twitch_url))

    Setting `Listening` Status
    await bot.change_presence(activity=disnake.Activity(type=discord.ActivityType.listening, name="a song"))

    Setting `Watching` Status
    await bot.change_presence(activity=disnake.Activity(type=disnake.ActivityType.watching, name="a movie"))
    """

    @tasks.loop(seconds=90)
    async def change_presence(self):
        await self.bot.wait_until_ready()

        activities = [
            disnake.Game(name="Minecraft ⚒️"),
            disnake.Activity(type=disnake.ActivityType.listening, name="2 Ur Txts 📱"),
            disnake.Activity(type=disnake.ActivityType.listening, name="Need Help?"),
            disnake.Game(name=" and Burble Flurpin Around 🏃")
        ]

        await self.bot.change_presence(
            status = disnake.Status.online,
            activity = random.choice(activities)
        )

def setup(bot):
    bot.add_cog(TaskChecks(bot))
