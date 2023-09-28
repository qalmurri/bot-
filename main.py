import discord
from discord.ext import commands
import traceback
import sys


bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user.name} ({bot.user.id}) on {len(bot.guilds)} Server')

    for a in ['cogs.thread', 'cogs.voice', 'cogs.traffic']:
        try:
            await bot.load_extension(a)
            print(f'Load {a}: Ok')
        except Exception as e:
            print(f'Load {a}: Error\n{str(e)}', file=sys.stderr)
            traceback.print_exc()

bot.run("MTE1MzMyNjY3NjUxMjYxNjQ2OQ.GBuFwf.kOKKr8d2NW15deATZuRC6OkZFgyFuh5XoprIYc")