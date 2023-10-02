import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=".",intents=discord.Intents.all())
extensions = ['cogs.act.message', 'cogs.act.reaction', 'cogs.act.voice']

@bot.event
async def on_ready():
    print(f'{bot.user.name} ({bot.user.id}) on {len(bot.guilds)} Server')

@bot.event
async def setup_hook() -> None:
    for extension in extensions:
        await bot.load_extension(extension)

@bot.tree.command(name="ping", description="test slash command")
async def ping(interaction:discord.Interaction):
    await interaction.response.send_message("ping!")

@bot.tree.command(name="avatar", description="Get user avatar")
async def avatar(interaction:discord.Interaction, member:discord.Member):
    await interaction.response.send_message(member.display_avatar)

bot.run("OTY3MTcwODYxNTA3NDQwNjUw.GiW7ve.QIFchpfuJfdLByji1jMdIE7J3KxF3of6Ejt2Is")
#Utama OTY3MTcwODYxNTA3NDQwNjUw.GiW7ve.QIFchpfuJfdLByji1jMdIE7J3KxF3of6Ejt2Is
#kedua MTE1MzMyNjY3NjUxMjYxNjQ2OQ.GBuFwf.kOKKr8d2NW15deATZuRC6OkZFgyFuh5XoprIYc
