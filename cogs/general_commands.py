import disnake
import json

from disnake.ext import commands

with open('config.json','r',encoding='utf-8-sig') as f:
    data = json.load(f)

guild_ids = [data["guild_id"],]

class PingCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name = "ping",
        description = "Returns The Bots Latency.",
        guild_ids = guild_ids
    )
    @commands.has_any_role(
        "Owners","Developers","Head Admins","Moderators","Community Helpers",
        "Programming","Gaming","Artistry","Nitro","Member","Python","JavaScript",
        "Java","Rust","HTML-CSS","Minecraft","Summoners-War","Chess"
    )
    async def ping(self, inter):
        def check(m):
            return inter.author.id == m.author.id

        latency = round(self.bot.latency, 2)

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = "Gawther's Latency",
            description = f"Hey! My latency is currently {str(latency)}ms. Would you like to report it? Please Respond With Yes or No"
        ).set_thumbnail(url = inter.guild.icon)

        await inter.response.send_message(embed=embed, delete_after=15)
        choice = await self.bot.wait_for('message', check=check, timeout=15)

        if choice.content.lower() == "yes":
            await choice.delete()

            if latency >= 20:
                embed.add_field(
                    name = "Report Information",
                    value = f"User: {inter.author.display_name} Has Reported {str(latency)}ms For Being Too High In Latency.",
                    inline = False
                ).add_field(
                    name = "Report Information Cont'd",
                    value = f"If you feel that the latency is ok, please get in touch with {inter.author.display_name} to see if you can figure out the problem and assist in a solution. Thanks!",
                    inline = False
                ).set_footer(
                    text = "Your Report Has Been Sent and A Staff Member Will Be In Touch. Please Be Patient"
                )

                channel = disnake.utils.get(inter.guild.text_channels, name="latency_reports")
                await channel.send(embed=embed)
                await inter.edit_original_message(embed=embed)
            else:
                await inter.edit_original_message("The Latency Is Not High Enough To Report!")


    @commands.slash_command(
        name = "server",
        description = "Returns Information About The Discord Server",
        guild_ids = guild_ids
    )
    @commands.has_any_role(
        "Owners","Developers","Head Admins","Moderators","Community Helpers",
        "Programming","Gaming","Artistry","Nitro","Member","Python","JavaScript",
        "Java","Rust","HTML-CSS","Minecraft","Summoners-War","Chess"
    )
    async def server(self,inter):
        owners = ', '.join([m.name for m in inter.guild.members if m.top_role.name == "Owners"]) or "Applications Open"
        bots = ', '.join([m.name for m in inter.guild.members if m.top_role.name == "Bots"]) or "Applications Open"
        devs = ', '.join([m.name for m in inter.guild.members if m.top_role.name == "Developers"]) or "Applications Open"
        head_admins = ', '.join([m.name for m in inter.guild.members if m.top_role.name == "Head Administrators"]) or "Applications Open"
        admins = ', '.join([m.name for m in inter.guild.members if m.top_role.name == "Administrators"]) or "Applications Open"
        moderators = ', '.join([m.name for m in inter.guild.members if m.top_role.name == "Moderators"]) or "Applications Open"
        comm_helpers = ', '.join([m.name for m in inter.guild.members if m.top_role.name == "Community Helpers"]) or "Applications Open"

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = f"{inter.guild.name}s' Server Information",
            description = f"Below you will find all the relative information belonging to {inter.guild.name}"
        ).set_thumbnail(url=inter.guild.icon)
        
        list1 = ["Owners", "Bots", "Developers", "Head Administrators", "Administrators", "Moderators", "Community Helpers"]
        list2 = [owners, bots, devs, head_admins, admins, moderators, comm_helpers]
        
        for index, value in enumerate(list1):
            embed.add_field(
                name = value,
                value = list2[index],
                inline = False
            )

        await inter.response.send_message(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(PingCommand(bot))