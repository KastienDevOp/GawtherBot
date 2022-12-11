import json
import disnake
import sqlite3 as sql

from disnake.ext import commands
from helpers import get_guild_id


class RulesCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="rules",
        description="Allows A Staff Member Of Head Admin/Owner To Create/Edit/Delete Rules Within The Database",
        guildids=[get_guild_id(), ]
    )
    @commands.has_any_role("Owners", "Developers", "Head Administrators")
    async def rules(self, inter, command: str = commands.Param(choices=["create", "edit", "delete"])):
        if command == "create":
            await self.create_rule(inter)
        elif command == "edit":
            await self.edit_rule(inter)
        elif command == "delete":
            await self.delete_rule(inter)
        else:
            return await inter.response.send_message("[Error] Function: rules; File: rules_commands.py")

    async def create_rule(self, inter):
        with open('./json_files/rules.json','r',encoding='utf-8-sig') as f:
            data = json.load(f)

            await inter.response.send_message("Enter New Rule Title")
            new_rule_title = (await self.bot.wait_for('message')).content

            if not all(i.isprintable() for i in new_rule_title):
                await inter.channel.purge(limit=1)
                return await inter.edit_original_message("That Is Not A Valid Entry. Try Again")

            await inter.channel.purge(limit=1)

            await inter.edit_original_message("Enter The Description For The Rule")
            new_rule_desc = (await self.bot.wait_for('message')).content

            if not all(i.isprintable() for i in new_rule_desc):
                await inter.channel.purge(limit=1)
                return await inter.edit_original_message("That Is Not A Valid Entry. Try Again")
            
            await inter.channel.purge(limit=1)

            with open('./json_files/rules.json','r',encoding='utf-8-sig') as f:
                data = json.load(f)

                new_rule_number = str(len(data["rules"].keys()) + 1)

                data["rules"][new_rule_number] = {
                    "title": new_rule_title,
                    "rule": new_rule_desc
                }

                with open('./json_files/rules.json','w+',encoding='utf-8-sig') as new:
                    data = json.dump(data, new, indent=4)

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = "Gawther's Rule Editor System Notifications",
            description = f"{inter.author.name} Has Created A New Rule"
        ).add_field(
            name = new_rule_title,
            value = new_rule_desc,
            inline = False
        )

        await inter.edit_original_message(embed=embed)
        return await disnake.utils.get(inter.guild.text_channels,name="other").send(embed=embed)

    async def edit_rule(self, inter):
        with open('./json_files/rules.json','r',encoding='utf-8-sig') as f:
            data = json.load(f)

            embed = disnake.Embed(
                color = disnake.Colour.random(),
                title = "Gawther's Rule Editor System",
                description = "Please Select Which Rule To Edit"
            ).set_thumbnail(url = self.bot.user.avatar)

            await inter.response.send_message(embed=embed)
            rule_number = (await self.bot.wait_for('message')).content

            if rule_number in data["rules"].keys():
                await inter.edit_original_message("Enter The New Title For The Rule. If None, Enter None.",embed=None)
                new_rule_title = (await self.bot.wait_for('message')).content

                if not all(i.isprintable() for i in new_rule_title):
                    await inter.channel.purge(limit=1)
                    return await inter.edit_original_message("That Is Not A Valid Entry. Try Again")

                await inter.channel.purge(limit=1)

                await inter.edit_original_message("Enter The New Details Of The Rule")
                new_rule_desc = (await self.bot.wait_for('message')).content

                if not all(i.isprintable() for i in new_rule_title):
                    await inter.channel.purge(limit=1)
                    return await inter.edit_original_message("That Is Not A Valid Entry. Try Again")

                data[rule_number] = {
                    "title": new_rule_title,
                    "rule": new_rule_desc
                }

                with open('./json_files/rules.json','w+',encoding='utf-8-sig') as new:
                    data = json.dump(data, new, indent=4)

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = "Gawther's Rule Editor System Notification",
            description = f"{inter.author.name} Has Edited Rule #{rule_number}"
        ).add_field(
            name = f"Previous Rule",
            value = "\u200b",
            inline = False
        ).add_field(
            name = rule_number + ') ' + new_rule_title,
            value = new_rule_desc,
            inline = False
        ).set_thumbnail(url = self.bot.user.avatar)

        await inter.edit_original_message(embed=embed)
        return await disnake.utils.get(inter.guild.text_channels, name="other").send(embed=embed)
                    

    # build with kastien
    async def delete_rule(self, inter):
        pass


def setup(bot):
    bot.add_cog(RulesCommands(bot))
