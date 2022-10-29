import disnake
import json
import re

from disnake.ext import commands

with open('config.json', 'r', encoding='utf-8-sig') as f:
    data = json.load(f)

guild_ids = [data["guild_id"], ]


class DevCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="developers",
        description="Shows a list of sub commands available to developers of the Gawther Platform.",
        guild_ids=guild_ids
    )
    @commands.has_any_role("Owners", "Developers")
    async def developers(self, inter, operation: str = commands.Param(choices=["send_dev_note","create_category","create_channel"])):
        if operation == "send_dev_note":
            await self.send_dev_note(inter)
        elif operation == "create_category":
            await self.create_category(inter)
        elif operation == "create_channel":
            await self.create_channel(inter)
        else:
            return await inter.response.send_message("Invalid Operation. Contact Developers and Owners")

    async def send_dev_note(self, inter):
        noti_chan = disnake.utils.get(
            inter.guild.text_channels, name="dev_notes")
        role_to_mention = disnake.utils.get(
            inter.guild.roles, name="dev_notes")

        await inter.response.send_message("Enter Note To Send:", ephemeral=True)
        note = await self.bot.wait_for('message')

        await note.delete()

        if all(i.isprintable() for i in note.content):
            await noti_chan.send(f"{role_to_mention.mention}\n{note.content}")
        else:
            sentence_parts = [
                "Your Message Must Be A Printable String. Please Use The ",
                "26-Letter English Alphabet, 0-9 Numeric Values, or Special ",
                "Characters Found On Your Number Row At The Top Of Your ",
                "Keyboard. Thanks"
            ]

            return await inter.edit_original_message(f"{''.join([p for p in sentence_parts])}")

    async def create_category(self,inter):
        await inter.response.send_message("Enter Name Of Category",ephemeral=True)
        category_name = (await self.bot.wait_for('message')).content

        if all(i.isprintable() for i in category_name):
            await inter.edit_original_message("Enter Position Of Channel. Remember: The Very Top Category Is Index ZERO!")
            position = int((await self.bot.wait_for('message')).content)

            await inter.channel.purge(limit=2)

            new_category = await inter.guild.create_category(name=category_name, position=position)

            embed = disnake.Embed(
                color = disnake.Colour.random(),
                title = "Gawther's Category and Channel Editor Notification System",
                description = f"{inter.author.name} Has Created A New Category."
            ).add_field(
                name = "Information",
                value = f"Category Name: {category_name}\nPosition: {position}",
                inline = False
            ).set_thumbnail(
                url = self.bot.user.avatar
            )

            try:
                await (disnake.utils.get(inter.guild.text_channels, name="category_channel_editing")).send(embed=embed)
                await inter.edit_original_message("Category Has Been Successfully Created.")
            except:
                return await inter.edit_original_message("Category Creation Failed. Contact Developers and Owners")
        else:
            return await inter.edit_original_message("Category Name Must Be A Valid String! Please use the 26-Letter English Alphabet, Numeric Values 0-9, and Normal Special Characters.")


def setup(bot):
    bot.add_cog(DevCommands(bot))
