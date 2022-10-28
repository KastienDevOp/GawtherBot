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
    async def developers(self, inter, operation: str = commands.Param(choices=["send_dev_note"])):
        if operation == "send_dev_note":
            await self.send_dev_note(inter)

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


def setup(bot):
    bot.add_cog(DevCommands(bot))
