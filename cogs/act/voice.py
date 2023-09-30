from discord.ext import commands
import json
import os

class voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def guild_folder(self, member):
        guild_id = member.guild.id
        directory = f"stats/{guild_id}/"
        self.file_path = f"stats/{guild_id}/voice.json"
        self.user_voice = self.load()
        if not os.path.exists(directory):
            os.makedirs(directory)

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        return {}

    def save(self):
        with open(self.file_path, "w") as file:
            json.dump(self.user_voice, file, indent=4)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        self.guild_folder(member)
        user_id = str(member.id)
        
        if before.channel is None and after.channel is not None:
            if user_id not in self.user_voice:
                self.user_voice[user_id] = {"join": 0, "leave": 0}
            self.user_voice[user_id]["join"] += 1
            self.save()

            print(f'{member.guild.id}/{after.channel.id}')
            print(f'{member.id}: Join Voice')

        elif before.channel is not None and after.channel is None:
            if user_id not in self.user_voice:
                self.user_voice[user_id] = {"join": 0, "leave": 0}
            self.user_voice[user_id]["leave"] += 1
            self.save()

            print(f'{member.guild.id}/{before.channel.id}')
            print(f'{member.id}: Leave Voice')

async def setup(bot):
    await bot.add_cog(voice(bot))