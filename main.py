import discord
from discord.ext import commands
import traceback
import sys

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
a = ['cogs.message', 'cogs.voice']

@bot.event
async def on_ready():
    print(f'{bot.user.name} ({bot.user.id}) on {len(bot.guilds)} Server')

    for b in a:
        try:
            await bot.load_extension(b)
            print(f'Load {b}: Ok')
        except Exception as e:
            print(f'Load {b}: Error.', file=sys.stderr)
            traceback.print_exc()

bot.run("MTE1MzMyNjY3NjUxMjYxNjQ2OQ.GBuFwf.kOKKr8d2NW15deATZuRC6OkZFgyFuh5XoprIYc")