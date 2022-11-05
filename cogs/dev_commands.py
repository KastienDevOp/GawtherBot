import disnake
import json
import re

from disnake.ext import commands
from helpers.helper_methods import get_guild_id


class DevCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name="developers",
        description="Shows a list of sub commands available to developers of the Gawther Platform.",
        guild_ids=[get_guild_id(),]
    )
    @commands.has_any_role("Owners", "Developers")
    async def developers(self, inter, operation: str = commands.Param(choices=["create_category","create_channel","delete_category","delete_channel","send_dev_note"])):
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

        if all(i.isprintable() for i in note.content):
            await note.delete()
            await noti_chan.send(f"{role_to_mention.mention}\n{note.content}")
        else:
            sentence_parts = [
                "Your Message Must Be A Printable String. Please Use The ",
                "26-Letter English Alphabet, 0-9 Numeric Values, or Special ",
                "Characters Found On Your Number Row At The Top Of Your ",
                "Keyboard. If You Message Is A Printed String, and You Are ",
                "Receiving This Error, Then Please Check The Character Count ",
                "Of Your Message. This Includes Spaces. Your Note Is Returned Along ",
                "With A Prefix OF Mentioning The Dev Role. Your Message Must Be 2000 ",
                "Characters Minus @dev_note Which Totals To 1990 Characters."
            ]

            return await inter.edit_original_message(f"{''.join([p for p in sentence_parts])}")

    async def create_category(self,inter):
        await inter.response.send_message("Enter Name Of Category",ephemeral=True)
        category_name = (await self.bot.wait_for('message')).content

        if all(i.isprintable() for i in category_name):
            await inter.channel.purge(limit=1)

            new_category = await inter.guild.create_category(name=category_name)

            embed = disnake.Embed(
                color = disnake.Colour.random(),
                title = "Gawther's Category and Channel Editor Notification System",
                description = f"{inter.author.name} Has Created A New Category."
            ).add_field(
                name = "Information",
                value = f"Category Name: {new_category.name}",
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

    async def create_channel(self,inter):
        await inter.response.send_message("Enter New Channel Name",ephemeral=True)
        name_of_channel = (await self.bot.wait_for('message')).content

        await inter.edit_original_message("Enter Category Name")
        name_of_category = (await self.bot.wait_for('message')).content
        category = disnake.utils.get(inter.guild.categories, name=name_of_category)

        await inter.edit_original_message("Enter Voice or Text For Channel Type")
        type_of_channel = (await self.bot.wait_for('message')).content

        if all(i.isprintable() for i in name_of_channel):
            if all(i.isprintable() for i in name_of_category):
                if type_of_channel.lower() == "text":
                    await inter.edit_original_message("Enter Topic For New Channel")
                    channel_topic = (await self.bot.wait_for('message')).content

                    new_channel = await inter.guild.create_text_channel(category=category, name=name_of_channel)
                    await new_channel.edit(topic=channel_topic)
                    noti_channel = disnake.utils.get(inter.guild.text_channels, name="category_channel_editing")

                    embed = disnake.Embed(
                        color = disnake.Colour.random(),
                        title = "Gawther's Category and Channel Editor Notification System",
                        description = f"{inter.author.name} Has Created A New Text Channel {new_channel.mention} In Category {category.mention}"
                    ).set_thumbnail(
                        url = self.bot.user.avatar
                    )

                    await noti_channel.send(embed=embed)

                    await inter.channel.purge(limit=4)
                    return await inter.edit_original_message(f"{new_channel.mention} Has Been Created In {category.mention} Successfully.")
                elif type_of_channel.lower() == "voice":
                    new_channel = await inter.guild.create_voice_channel(category=category, name=name_of_channel)
                    noti_channel = disnake.utils.get(inter.guild.text_channels, name="category_channel_editing")

                    embed = disnake.Embed(
                        color = disnake.Colour.random(),
                        title = "Gawther's Category and Channel Editor Notification System",
                        description = f"{inter.author.name} Has Created A New Voice Channel {new_channel.mention} In Category {category.mention}"
                    ).set_thumbnail(
                        url = self.bot.user_avatar
                    )

                    await noti_channel.send(embed=embed)

                    await inter.channel.purge(limit=3)
                    return await inter.edit_original_message(f"{new_channel.mention} Has Been Created In {category.mention} Successfully.")
                else:
                    return await inter.edit_original_message("The Channel Type Must Be Text or Voice")
            else:
                return await inter.edit_original_message("The Category Name Must Be A Printable String!")
        else:
            return await inter.edit_original_message("The Channel Name Must Be A Printable String!")
            
def setup(bot):
    bot.add_cog(DevCommands(bot))
