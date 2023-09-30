import discord
from discord.ext import commands
import random
import json

class traffic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def load_json_file(filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            return {}
    
    user_react = load_json_file("stats/user_react.json")
    user_message = load_json_file("stats/user_message.json")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        MemberMention = member.mention
        Sentence = [
            f'Hai {MemberMention}, kamu bisa mengunjungi https://discord.com/channels/809654746301595679/1110105612790005812 untuk melakukan perkenalan dengan yang lain',
            f'Hai {MemberMention}, taukah kamu, channel ini https://discord.com/channels/809654746301595679/1110105612790005812 bisa untuk bermain lo'
        ]

        embed = discord.Embed(description=random.choice(Sentence), color=discord.Color.random())
        embed.set_thumbnail(url=member.avatar)
        embed.add_field(name="Akun",
                    value=f'{member.created_at.strftime("%Y-%m-%d")}',
                    inline=True)
        embed.add_field(name="Umur",
                    value=str((member.joined_at - member.created_at).days) + " Hari",
                    inline=True)
        
        JoinChannel = 1156797680807313448
        e = self.bot.get_channel(JoinChannel)
        if e is not None:
            await e.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        member_id = str(member.id)

        MemberMention = member.mention
        SentenceOne = [
            f'Selamat jalan {MemberMention}',
            f'Sayonara {MemberMention}',
            f'Dada {MemberMention}',
            f'Sampai jumpa kembali {MemberMention}',
        ]

        MemberJoin = member.joined_at.strftime("%Y-%m-%d")
        JoiningAge = str((member.joined_at - discord.utils.utcnow()).days)
        SentenceTwo = [
            f'Pada {MemberJoin} kamu bergabung dan hanya sampai umur ini {JoiningAge} hari',
            f'kamu bergabung pada {MemberJoin}, dan sekarang umur {JoiningAge} hari kamu keluar',
        ]

        Reply = str(self.user_message.get(member_id, {"reply": 0})["reply"])
        Replied = str(self.user_message.get(member_id, {"replied": 0})["replied"])
        SentenceThree = [
            f'Kamu sudah {Reply} reply kepada temanmu, dan kamu juga mendapatkan {Replied} replied dari teman-temanmu',
            f'{Reply} reply kepada temanmu dan {Replied} replied dari teman-temanmu',
            f'Kamu mendapatkan {Replied} replied dari teman-temanmu, dan kamu reply {Reply} ke teman-temanmu',
        ]

        Chat = str(self.user_message.get(member_id, {"chat": 0})["chat"])
        VoiceTotal = "2"
        SentenceFour = [
            f'Chatmu yang ke {Chat} dan {VoiceTotal} jam voicemu menjadi perpisahan kita',
            f'{Chat} chat dan {VoiceTotal} jam di voice channelmu menjadi riwayat yang tidak pernah kita lupakan',
        ]

        ReactTotal = str(self.user_react.get(member_id, {"react": 0})["react"])
        ReactedTotal = str(self.user_react.get(member_id, {"reacted": 0})["reacted"])
        SentenceFive = [
            f'Chatmu juga mendapatkan {ReactedTotal} reaksi dari temanmu dan kamu mereaksi chat temanmu {ReactTotal}',
            f'Kamu mereaksi chat temanmu {ReactTotal} dan chatmu mendapatkan reaksi dari temanmu {ReactedTotal}',
        ]
        
        Sentence = [
            f'{random.choice(SentenceTwo)}, {random.choice(SentenceThree)}. {random.choice(SentenceFour)}, {random.choice(SentenceFive)}. {random.choice(SentenceOne)}.'
        ]

        embed = discord.Embed(description=random.choice(Sentence), color=discord.Color.random())
        embed.set_thumbnail(url=member.avatar)

# KIRIM DM KE USER JIKA USER LEAVE DARI SERVER
#        try:
#            await member.send(embed=d)
#            print(f"Dapat mengirim pesan ke DM {member.display_name}")
#        except discord.Forbidden:
#            print(f"Tidak dapat mengirim pesan ke DM {member.display_name}: DM dinonaktifkan atau bot diblokir")

        LeaveChannel = 1156797728957943868
        a = self.bot.get_channel(LeaveChannel)
        if a is not None:
            await a.send(embed=embed)

async def setup(bot):
    await bot.add_cog(traffic(bot))