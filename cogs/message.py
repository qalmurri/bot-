from discord.ext import commands

class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.reference:
            a = await message.channel.fetch_message(message.reference.message_id)
            if a:
                print(f"{message.guild.id}/{message.channel.id}/{message.id}")
                print(f"{a.author.id}: {a.content} < {message.author.id}: {message.content}")
        else:
            print(f'{message.guild.id}/{message.channel.id}')
            print(f'{message.author.id}: {message.content}')
            await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        a = reaction.message
        print(f'{a.guild.id}/{a.channel.id}/{a.id} ')
        print(f"{a.author.id}: {a.content} < {user.id}: {reaction.emoji}")

async def setup(bot):
    await bot.add_cog(message(bot))