import discord
from discord.ext import commands
from discord import app_commands

class webhooks(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @app_commands.command(name="message", description="send webhooks text and avatar")
    async def message(self, interaction: discord.Interaction):
        user = interaction.user
        avatar_url = user.display_avatar
        username = user.name

        channel_id = 1156794544382283877
        channel = self.bot.get_channel(channel_id)

        if channel is None:
            await interaction.response.send_message("Saluran tidak ditemukan.")
            return

        webhook = await channel.create_webhook(name=username)

        embed = discord.Embed(
            description="Kamu berhasil mendapatkan koin",
            color=0x00ff00 
        )
        embed.set_thumbnail(url=avatar_url)

        # Menggunakan content untuk mengirim pesan teks
        await webhook.send(content=username, avatar_url=avatar_url, embed=embed)

async def setup(bot):
    await bot.add_cog(webhooks(bot))