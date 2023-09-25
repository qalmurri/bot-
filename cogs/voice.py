import discord
from discord.ext import commands

class voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if before.channel is None and after.channel is not None:
            print(f'{member.guild.id}/{after.channel.id}')
            print(f'{member.id}: Join Voice')

        elif before.channel is not None and after.channel is None:
            print(f'{member.guild.id}/{before.channel.id}')
            print(f'{member.id}: Leave Voice')

async def setup(bot):
    await bot.add_cog(voice(bot))