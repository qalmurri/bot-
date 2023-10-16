import discord
from discord import app_commands
from discord.ext import commands
import database as db

from PIL import Image, ImageDraw, ImageFont

class basic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="profile", description="Profile RPG")
    async def profile(self, interaction:discord.Interaction, member:discord.Member):
        player = await db.player[f"{interaction.guild.id}"].find_one({"_id": member.id})
        if player is None:
            await interaction.response.send_message("user tidak ada")
        else:
            jdate = player["game"]["rpg"]["jdate"]
            str = player["game"]["rpg"]["stats"]["str"]
            int = player["game"]["rpg"]["stats"]["int"]
            atk = player["game"]["rpg"]["stats"]["atk"]

            await interaction.response.send_message("profile")

async def setup(bot):
    await bot.add_cog(basic(bot))