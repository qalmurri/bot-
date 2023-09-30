from discord.ext import commands
import json
import os


class voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = "stats/voice.json"
        self.user_voice = self.load_user_voice()

        if not os.path.exists("stats"):
            os.mkdir("stats")

    def load_user_voice(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        return {}

    def save_user_voice(self):
        with open(self.file_path, "w") as file:
            json.dump(self.user_voice, file, indent=4)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        user_id = str(member.id)
        if before.channel is None and after.channel is not None:
            if user_id not in self.user_voice:
                self.user_voice[user_id] = {"join": 0, "leave": 0}
            self.user_voice[user_id]["join"] += 1
            self.save_user_voice()

            print(f'{member.guild.id}/{after.channel.id}')
            print(f'{member.id}: Join Voice')

        elif before.channel is not None and after.channel is None:
            if user_id not in self.user_voice:
                self.user_voice[user_id] = {"join": 0, "leave": 0}
            self.user_voice[user_id]["leave"] += 1
            self.save_user_voice()

            print(f'{member.guild.id}/{before.channel.id}')
            print(f'{member.id}: Leave Voice')

async def setup(bot):
    await bot.add_cog(voice(bot))