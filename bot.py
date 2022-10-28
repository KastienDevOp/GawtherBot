import disnake
import json
import os
import asyncio

from disnake.ext import commands
from createDb import create_db


with open('./config.json','r',encoding='utf-8-sig') as f:
    data = json.load(f)

token = data["token"]
cp = data["cp"]
guild_id = data["guild_id"]

with open('./setup.json','r',encoding="utf-8-sig") as g:
    data = json.load(g)
    
terminal_id = data["terminalId"] # gawthers terminal channel for the server

intent = disnake.Intents.all()

bot = commands.Bot(
    command_prefix = cp,
    intents = intent
)

@bot.event
async def on_ready():
    terminal = disnake.utils.get(bot.get_guild(guild_id).text_channels, id=terminal_id)
    all_cogs = []

    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            all_cogs.append(f"cogs.{filename[:-3]}")

    print("="*20)
    print("Gawther Is Booting Up. . .")
    msg = await terminal.send("Gawther Is Booting Up. . .")
    await asyncio.sleep(2)
    await msg.edit(f"Preparing To Load {len(all_cogs)} cog(s). . .")
    print(f"Preparing To Load {len(all_cogs)} cog(s). . .")
    await asyncio.sleep(2)

    for cog in all_cogs:
        bot.load_extension(cog)
        await msg.edit(f"Loaded {cog} (/)")
        print(f"Loaded {cog} (/)")
        await asyncio.sleep(0.5)

    await msg.edit("Gawther Has Booted and Is Online. Enjoy!")
    print("Gawther Online")
    print("="*20)

@bot.command()
@commands.has_any_role("Owners","Developers","Head Administrators")
async def update(ctx):
    async def start():
        await msg.delete()
        os.system("python ./bot.py")
        await confirm(ctx)

    msg = await ctx.send("Gawther Is Restarting. . .")
    print("Restarting Gawther. . .")
    await asyncio.sleep(2)
    await start()


async def confirm(ctx):
    print("Restarted Gawther. . .")
    msg = await ctx.send("Gawther Has Restarted. . .")
    await asyncio.sleep(1)
    await msg.delete()

if __name__ == '__main__':
    create_db()
    bot.run(token)