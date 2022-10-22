import disnake
import random
import json
import asyncio

from disnake.ext import commands

with open('config.json','r',encoding='utf-8-sig') as f:
    data = json.load(f)

guild_ids = [data["guild_id"],]


class ServerSetup(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        name = "server_setup",
        description = "Builds All Roles, Categories, Text Channels, and Voice Channels For The Server.",
        guild_ids = guild_ids
    )
    @commands.has_any_role("Owners")
    async def server_setup(self, ctx):
        await ctx.response.send_message("Building Roles, Categories, and Channels. . . Please Wait. . .")
        # Staff Roles
        
        await ctx.guild.create_role(name = "Head Administrator")
        await ctx.guild.create_role(name = "Administrator")
        await ctx.guild.create_role(name = "Moderator")
        await ctx.guild.create_role(name = "Community Helper")
        await ctx.guild.create_role(name = "Member")
        
        # Member Roles
        await ctx.guild.create_role(name = "Programming") if not disnake.utils.get(ctx.guild.roles, name="Programming")
        await ctx.guild.create_role(name = "Gaming") if not disnake.utils.get(ctx.guild.roles, name="Gaming")
        await ctx.guild.create_role(name = "Artistry") if not disnake.utils.get(ctx.guild.roles, name="Artistry")
        await ctx.guild.create_role(name = "Nitro") if not disnake.utils.get(ctx.guild.roles, name="Nitro")
        await ctx.guild.create_role(name = "Python") if not disnake.utils.get(ctx.guild.roles, name="Python")
        await ctx.guild.create_role(name = "JS") if not disnake.utils.get(ctx.guild.roles, name="JS")
        await ctx.guild.create_role(name = "Java") if not disnake.utils.get(ctx.guild.roles, name="Java")
        await ctx.guild.create_role(name = "CSharp") if not disnake.utils.get(ctx.guild.roles, name="CSharp")
        await ctx.guild.create_role(name = "C") if not disnake.utils.get(ctx.guild.roles, name="C")
        await ctx.guild.create_role(name = "Rust") if not disnake.utils.get(ctx.guild.roles, name="Rust")
        await ctx.guild.create_role(name = "HTML-CSS") if not disnake.utils.get(ctx.guild.roles, name="HTML-CSS")

        # Categories
        await ctx.guild.create_category(name = "Bot Stuff", position = 6) if not disnake.utils.get(ctx.guild.categories, name="Bot Stuff") # welcome
        await ctx.guild.create_category(name = "Staff", position = 5) if not disnake.utils.get(ctx.guild.categoies) # general
        await ctx.guild.create_category(name = "General", position = 0) # programming
        await ctx.guild.create_category(name = "Programming", position = 1) # gaming
        await ctx.guild.create_category(name = "Gaming", position = 2) # artistry
        await ctx.guild.create_category(name = "Artistry", position = 4) # staff
        await ctx.guild.create_category(name = "Logs", position = 3) # logs

        await ctx.response.defer()
        await ctx.edit_original_message("Finished Setting Up The Server!")


def setup(bot):
    bot.add_cog(ServerSetup(bot))
