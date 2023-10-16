import discord
from discord import app_commands
from discord.ext import commands

class basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="avatar", description="Get user avatar")
    async def avatar(self, interaction:discord.Interaction, member:discord.Member):
        await interaction.response.send_message(member.display_avatar)

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction:discord.Interaction):
        latency = round(self.bot.latency * 1000)
        await interaction.response.send_message(f"Pong! Latency is {latency}ms")

async def setup(bot):
    await bot.add_cog(basic(bot))