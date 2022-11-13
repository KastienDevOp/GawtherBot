import disnake
import asyncio

from disnake.ext import commands
from API.helpers import get_guild_id


class DeveloperCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name = "devs",
        description = "Shows a list of buttons available to the developer",
        guild_ids = [get_guild_id(),]
    )
    @commands.has_any_role("Owners","Developers")
    async def devs(self, inter: disnake.ApplicationCommandInteraction):
        buttons = [
            disnake.ui.Button(label="Create Category", custom_id="CreateCat"),
            disnake.ui.Button(label="Create Channel", custom_id="CreateChan"),
            disnake.ui.Button(label="Create Role", custom_id="CreateRole"),
            disnake.ui.Button(label="Create Dev Note", custom_id="CreateNote"),
            disnake.ui.Button(label="Delete Category", custom_id="DeleteCat"),
            disnake.ui.Button(label="Delete Channel", custom_id="DeleteChan"),
            disnake.ui.Button(label="Delete Role", custom_id="DeleteRole")
        ]

        embed = disnake.Embed(
            color = disnake.Colour.random(),
            title = "Developer Commands",
            description = "Below Are The Available Developer Buttons. Please Use Them With Caution And With Permission!"
        ).set_thumbnail(
            url = self.bot.user.avatar
        )

        await inter.channel.send(embed=embed,components=buttons,delete_after=10)

    @commands.Cog.listener()
    async def on_button_click(self,inter: disnake.MessageInteraction):
        button = inter.component
        
        if button.custom_id == "CreateCat":
            await self.create_category(inter)
        elif button.custom_id == "CreateChan":
            await self.create_channel(inter)
        elif button.custom_id == "CreateRole":
            await self.create_role(inter)
        elif button.custom_id == "CreateNote":
            await self.send_dev_note(inter)
        elif button.custom_id == "DeleteCat":
            await self.delete_category(inter)
        elif button.custom_id == "DeleteChan":
            await self.delete_channel(inter)
        elif button.custom_id == "DeleteRole":
            await self.delete_role(inter)

    async def send_dev_note(self, inter: disnake.MessageInteraction):
        await asyncio.sleep(1)
        noti_chan = disnake.utils.get(
            inter.guild.text_channels, name="dev_notes")
        role_to_mention = disnake.utils.get(
            inter.guild.roles, name="dev_notes")

        await inter.edit_original_message("Enter Note To Send:")
        note = await self.bot.wait_for('message')

        if all(i.isprintable() for i in note.content):
            await inter.channel.purge(limit=1)
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

    async def create_category(self,inter: disnake.MessageInteraction):
        await asyncio.sleep(1)
        await inter.edit_original_message("Enter Name Of Category",ephemeral=True)
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

    async def create_channel(self,inter: disnake.MessageInteraction):
        await asyncio.sleep(1)
        await inter.edit_original_message("Enter New Channel Name",ephemeral=True)
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

    async def create_role(self, inter: disnake.MessageInteraction):
        return await inter.response.send_message("This Command Needs To Be Built By A Better Programmer Since It Includes Setting Permissions For The Role Programmatically. -Mek",ephemeral=True)
    
    async def delete_category(self,inter: disnake.MessageInteraction):
        await asyncio.sleep(1)
        await inter.edit_original_message("Enter Name Of Category To Delete",ephemeral=True)
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

    async def delete_channel(self, inter: disnake.MessageInteraction):
        await asyncio.sleep(1)
        await inter.edit_original_message("Enter The Channel ID For The Channel You Want To Delete",ephemeral=True)
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

    async def delete_role(self, inter: disnake.MessageInteraction):
        return await inter.edit_original_message("This Command Needs To Be Built After The Create Role Command Has Been Built. -Mek",ephemeral=True)

def setup(bot):
    bot.add_cog(DeveloperCommands(bot))