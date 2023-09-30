from discord.ext import commands
import discord
from discord import app_commands

class test(commands.Cog, name="test"):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #@app_commands.guilds(discord.Object(id=809654746301595679)) # Place your guild ID here
    @commands.hybrid_command(name="test", description="Command description")
    async def test(self, ctx):
        await ctx.send("This is a hybrid command!")

@app_commands.guilds(discord.Object(id=809654746301595679)) # Place your guild ID here
async def setup(bot):
    await bot.add_cog(test(bot))