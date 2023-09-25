import discord
from discord.ext import commands

class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        print(f'{message.guild.id}/{message.channel.id}')
        print(f'{message.author.id}: {message.content}')
        await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print(f'{reaction.message.guild.id}/{reaction.message.channel.id}/{reaction.message.id} ')
        print(f"{user.id} {reaction.emoji} {reaction.message.author.id}")

async def setup(bot):
    await bot.add_cog(message(bot))