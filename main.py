import discord
from discord.ext import commands
import traceback
import sys

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
extensions = ['cogs.message', 'cogs.threads', 'cogs.voice']

@bot.event
async def on_ready():
    print(bot.user.name + " (" + str(bot.user.id) + ") ON")
    
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            print(f'Memuat {extension} : OK')
        except Exception as e:
            print(f'Memuat {extension} : GAGAL.', file=sys.stderr)
            traceback.print_exc()

bot.run("MTE1MzMyNjY3NjUxMjYxNjQ2OQ.GBuFwf.kOKKr8d2NW15deATZuRC6OkZFgyFuh5XoprIYc")