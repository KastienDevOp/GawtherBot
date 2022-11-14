import disnake
import sqlite3 as sql

from disnake.ext import commands
from helpers import get_guild_id


class RulesCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name = "rules",
        description = "Allows A Staff Member Of Head Admin/Owner To Create/Edit/Delete Rules Within The Database",
        guildids = [get_guild_id(),]
    )
    @commands.has_any_role("Owners","Developers","Head Administrators")
    async def rules(self, inter, command: str = commands.Param(
        choices = ["create","edit","delete"]
    )):
        if command == "create":
            self.create_rule()
        elif command == "edit":
            self.edit_rule()
        elif command == "delete":
            self.delete_rule()
        else:
            return await inter.reponse.send_message("That Is Not A Valid Option. Try Again!")

    async def create_rule(self):
        await inter.response.send_message("Enter The Name Of The Rule",ephemeral=True)
        rule_name = await self.check_input((await self.bot.wait_for('message')).content)
        await inter.channel.purge(limit=1)

        await inter.edit_original_message("Enter The Rules Description")
        rule_desc = await self.check_input((await self.bot.wait_for('message')).content)
        await inter.channel.purge(limit=1)

        await self.update_db(self,rule_name,rule_desc)

    async def update_db(self,name,description):
        with sql.connect('rules.db') as rules:
            cur = rules.cursor()

            new_rule_num = len(cur.execute('SELECT * FROM current').fetchall()) + 1

            if option == "new":
                srch = 'INSERT INTO current(rule_number, rule_name, rule_details) VALUES (?,?,?)'
                val = (new_rule_num, name, description)

                try:
                    cur.execute(srch, val)
                    return True
                except:
                    return False
            elif option == "edit":
                pass
            elif option == "delete":
                pass
            else:
                return await inter.edit_original_message("Database Failed To Update. Contact Developers")

    async def check_input(self, message):
        if all(i.isprintable() for i in message):
            return True
        else:
            return False


def setup(bot):
    bot.add_cog(RulesCommands(bot))