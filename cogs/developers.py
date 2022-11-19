import disnake
import asyncio

from disnake.ext import commands
from helpers import get_guild_id


class DeveloperCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name = "devs",
        description = "Shows a list of buttons available to the developer",
        guild_ids = [get_guild_id(),]
    )
    @commands.has_any_role("Owners","Developers")
    async def devs(self, inter, cmd: str = commands.Param(choices=["Create Category","Create Channel","Create Role","Create Dev Note","Delete Category","Delete Channel","Delete Role","Update Database"])):

        if cmd == "Create Category":
            await self.create_category(inter)
        elif cmd == "Create Channel":
            await self.create_channel(inter)
        elif cmd == "Create Role":
            await self.create_role(inter)
        elif cmd == "Create Dev Note": #finished
            await self.send_dev_note(inter)
        elif cmd == "Delete Category":
            await self.delete_category(inter)
        elif cmd == "Delete Channel":
            await self.delete_channel(inter)
        elif cmd == "Delete Role":
            await self.delete_role(inter)
        elif cmd == "Update Database":
            await self.update_database(inter)
        else:
            pass

    #finished
    async def send_dev_note(self, inter):
        await asyncio.sleep(1)
        noti_chan = disnake.utils.get(
            inter.guild.text_channels, name="dev_notes")
        role_to_mention = disnake.utils.get(
            inter.guild.roles, name="dev_notes")

        await inter.response.send_message("Enter Note To Send:",ephemeral=True)
        note = await self.bot.wait_for('message')

        if all(i.isprintable() for i in note.content):
            await inter.channel.purge(limit=1)
            await noti_chan.send(f"{role_to_mention.mention}\n{note.content}")

            return await inter.edit_original_message("Your Note Was Sent Successfully")
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
        await asyncio.sleep(1)
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
                return await inter.edit_original_message("Category Has Been Successfully Created.")
            except:
                return await inter.edit_original_message("Category Creation Failed. Contact Developers and Owners")
        else:
            return await inter.edit_original_message("Category Name Must Be A Valid String! Please use the 26-Letter English Alphabet, Numeric Values 0-9, and Normal Special Characters.")

    async def create_channel(self,inter):
        await asyncio.sleep(1)
        await inter.response.send_message("Enter New Channel Name")
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
                        url = self.bot.user.avatar
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

    async def create_role(self, inter):
        return await inter.response.send_message("This Command Needs To Be Built By Kas Since It Includes Setting Permissions For The Role Programmatically. -Mek",ephemeral=True)
    
    async def delete_category(self, inter):
        await asyncio.sleep(1)
        await inter.response.send_message("Enter Name Of Category To Delete")
        cat_name = (await self.bot.wait_for('message')).content

        if cat_name in [cat.name for cat in inter.guild.categories]:
            category_to_delete = disnake.utils.get(inter.guild.categories, name=cat_name)
            noti_chan = disnake.utils.get(inter.guild.text_channels, name="category_channel_editing")

            embed = disnake.Embed(
                color = disnake.Colour.random(),
                title = "Gawther's Category and Channel Editor Notification System",
                description = f"{inter.author.name} Has Deleted The Category, {category_to_delete.name}."
            ).set_thumbnail(
                url = self.bot.user.avatar
            )

            await noti_chan.send(embed=embed)
            await inter.edit_original_message(f"{inter.author.mention}, You Have Successfully Deleted The Category {category_to_delete.name}.")
            return await category_to_delete.delete()
        else:
            return await inter.edit_original_message("That Category Does Not Exist. Try Again")    

    async def delete_channel(self, inter):
        await asyncio.sleep(1)
        await inter.response.send_message("Enter The Channel ID For The Channel You Want To Delete",ephemeral=True)
        channel_id = int((await self.bot.wait_for('message')).content)

        if channel_id in [chan.id for chan in inter.guild.channels]:
            channel_to_delete = disnake.utils.get(inter.guild.channels, id=channel_id)
            noti_chan = disnake.utils.get(inter.guild.text_channels, name="category_channel_editing")

            embed = disnake.Embed(
                color = disnake.Colour.random(),
                title = f"Gawther's Category and Channel Editor Notification System",
                description = f"{inter.author.name} Has Deleted The {channel_to_delete.type} Channel, {channel_to_delete.name}."
            ).set_thumbnail(
                url = self.bot.user.avatar
            )

            await noti_chan.send(embed=embed)
            await inter.edit_original_message(f"{inter.author.mention} You Have Successfully Deleted The Channel {channel_to_delete.name}.")
            return await channel_to_delete.delete()

    async def delete_role(self, inter):
        return await inter.edit_original_message("This Command Needs To Be Built By Kas After The Create Role Command Has Been Built. -Mek",ephemeral=True)

    async def update_database(self, inter):
        return await inter.response.send_message("This command will need to be built by KastienDev as I cannot figure out the database logic. ~Mek", delete_after=30)


def setup(bot):
    bot.add_cog(DeveloperCommands(bot))