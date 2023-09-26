import discord
from discord.ext import commands
from discord.ui import Button

class threads(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='list_threads')
    async def list_threads(self, ctx):
        if isinstance(ctx.channel, discord.TextChannel):
            threads = ctx.channel.threads
            if threads:
                for thread in threads:
                    button = Button(style=discord.ButtonStyle.link, label=thread.name, url=f'https://discord.com/channels/{ctx.guild.id}/{thread.id}')
                    view = discord.ui.View()
                    view.add_item(button)
                    await ctx.send(view=view)
                    #await ctx.send(f"{thread.name}: https://discord.com/channels/{ctx.guild.id}/{thread.id}")
            else:
                await ctx.send("No Threads.")
        else:
            await ctx.send("Can't.")


async def setup(bot):
    await bot.add_cog(threads(bot))