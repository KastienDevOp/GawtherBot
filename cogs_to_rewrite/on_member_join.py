import disnake
import sqlite3 as sql
import json
import random

from disnake.ext import commands


class OnMemberJoin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        embed = disnake.Embed(
            color=disnake.Colour.random(),
            title="Welcome To Gawther!",
            description=f"Hi, {member.display_name}! Welcome to Gawther! Please Read Below To Find Out More About Us!"
        )

        with open('setup.json', 'r', encoding='utf-8-sig') as f:
            data = json.load(f)

            for i in data["information"].keys():
                item_name = data["information"][i]["name"]
                item_value = data["information"][i]["value"]

                embed.add_field(
                    name=item_name,
                    value=item_value,
                    inline=False
                )

            embed.add_field(
                name="In Addition. . .",
                value="In Addition to those values above, we also would like to go over some rules for the community with you",
                inline=False
            )

            for j in data["rules"].keys():
                rule_name = data["rules"][j]["name"]
                rule_desc = data["rules"][j]["desc"]

                embed.add_field(
                    name=rule_name,
                    value=rule_desc,
                    inline=False
                )

            embed.add_field(
                name="Along With The Rules. . .",
                value="Along With The Rules we also have a punishment chart. This is not written in stone, and the staff are allowed to enter their own custom time frames."
            )

            for k in data["punishmentTable"].keys():
                pTable_name = data["punishmentTable"][k]["name"]
                pTable_desc = data["punishmentTable"][k]["desc"]

                embed.add_field(
                    name=pTable_name,
                    value=pTable_desc,
                    inline=False
                )

            embed.set_footer(
                text="Given that you have agreed and read the rules and statements above, please repond with Confirm or Deny to continue.",
            ).set_thumbnail(
                url=member.guild.icon
            )

            await member.send(embed=embed)
            choice = await self.bot.wait_for('message')

            welcome_channel = disnake.utils.get(
                member.guild.text_channels, name="welcome_members")

            all_quotes = []

            with open('quotes.json', 'r', encoding='utf-8-sig') as f:
                data = json.load(f)

                for i in data.keys():
                    all_quotes.append(data[i])

            quote = random.choice(all_quotes)

            if choice.content.lower() == "confirm":
                member_role = disnake.utils.get(
                    member.guild.roles, name="Member")
                await member.add_roles(member_role)

                with sql.connect('main.db') as mdb:
                    cur = mdb.cursor()

                    current_members = cur.execute(
                        'SELECT id FROM members').fetchall()

                    if member.id not in current_members:
                        srch = 'INSERT INTO members(id, bank) VALUES (?,?)'
                        val = (member.id, 1500.00)

                        cur.execute(srch, val)

                        await member.send("You Have Been Successfully Made A Member! Please Enjoy Your $1500.00GB (Gawther Bucks) Welcome Bonus!")

                        embed = disnake.Embed(
                            color=disnake.Colour.green(),
                            title=f"Welcome {member.display_name}",
                            description="We're Pleased To Have You Aboard! Please Enjoy Your Stay! Remember: If you have any problems, please get in touch with Support!"
                        ).set_footer(text=quote).set_thumbnail(url=member.avatar)

                        await welcome_channel.send(embed=embed)
                    else:
                        await member.send("There was an issue with adding you to the database. Please get in touch with support!")
            else:
                await member.send("Are you sure you want to deny the rules? Y/N")
                choice = await self.bot.wait_for('message')

                if choice.content.lower() == "y":
                    await member.guild.kick(member, "Denied Confirmation To Rules")
                else:
                    self.on_member_join(member)


def setup(bot):
    bot.add_cog(OnMemberJoin(bot))
