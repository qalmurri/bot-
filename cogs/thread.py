import discord
from discord.ext import commands
from discord.ui import Button

class threads(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='list_threads')
    async def list_threads(self, ctx):
        if isinstance(ctx.channel, discord.TextChannel):
            if ctx.channel.threads:
                for a in ctx.channel.threads:
                    b = discord.ui.View()
                    b.add_item(Button(style=discord.ButtonStyle.link,
                                         label=a.name,
                                         url=f'https://discord.com/channels/{ctx.guild.id}/{a.id}'))
                    await ctx.send(view=b)
            else:
                await ctx.send("No Threads.")
        else:
            await ctx.send("Can't.")


async def setup(bot):
    await bot.add_cog(threads(bot))