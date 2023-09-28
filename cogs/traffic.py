import discord
from discord.ext import commands
import random

class traffic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        a = 1156797680807313448
        b = member.mention
        c = [
            f'Hai {b}, kamu bisa mengunjungi https://discord.com/channels/809654746301595679/1110105612790005812 untuk melakukan perkenalan dengan yang lain',
            f'Hai {b}, taukah kamu, channel ini https://discord.com/channels/809654746301595679/1110105612790005812 bisa untuk bermain lo'
        ]
        d = discord.Embed(
            description=random.choice(c),
            color=discord.Color.random()
        )
        d.set_thumbnail(url=member.avatar)
        d.add_field(name="Akun Dibuat",
                    value=f'{member.created_at.strftime("%Y-%m-%d")}', #("%Y-%m-%d %H:%M:%S")
                    inline=True)
        d.add_field(name="Umur Akun",
                    value=str((member.joined_at - member.created_at).days) + " Hari",
                    inline=True)
        e = self.bot.get_channel(a)
        if e is not None:
            await e.send(embed=d)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        a = 1156797728957943868
        b = member.mention
        c = [
            f'Selamat Jalan {b}',
            f'Sayonara {b}'
        ]
        d = discord.Embed(
            description=random.choice(c),
            color=discord.Color.random()
        )
        d.set_thumbnail(url=member.avatar)
        d.add_field(name="Bergabung di Server",
                    value=f'{member.joined_at.strftime("%Y-%m-%d")}',
                    inline=True)
        d.add_field(name="Umur Bergabung",
                    value=str((member.joined_at - discord.utils.utcnow()).days) + " Hari",
                    inline=True)
        e = self.bot.get_channel(a)
        if e is not None:
            await e.send(embed=d)

async def setup(bot):
    await bot.add_cog(traffic(bot))