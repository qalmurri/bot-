from discord.ext import commands
import json
import os
import time

class voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f'Exstension Voice Ready')

    def guild(self, member):
        self.file_path = f"stats/{member.guild.id}/voice.json"
        self.user_voice = self.load()

        if not os.path.exists(f"stats/{member.guild.id}/"):
            os.makedirs(f"stats/{member.guild.id}/")

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return {}

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.user_voice, f, indent=4)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        self.guild(member)
        
        if before.channel is None and after.channel is not None:
            if str(member.id) not in self.user_voice:
                self.user_voice[str(member.id)] = {"join": 0, "leave": 0, "status": 0, "total": { "start_time": 0, "total_time": 0}}
            self.user_voice[str(member.id)]["join"] += 1
            self.user_voice[str(member.id)]["status"] = 1
            self.user_voice[str(member.id)]["total"]["start_time"] = time.time()
            self.save()

            print(f'{member.guild.id}/{after.channel.id}')
            print(f'{member.id}: Join Voice {time.time()}')

        elif before.channel is not None and after.channel is None:
            if str(member.id) not in self.user_voice:
                self.user_voice[str(member.id)] = {"join": 0, "leave": 0, "status": 0, "total": { "start_time": 0, "total_time": 0}}
            self.user_voice[str(member.id)]["leave"] += 1
            self.user_voice[str(member.id)]["status"] = 0

            total_time = time.time() - self.user_voice[str(member.id)]["total"]["start_time"]
            self.user_voice[str(member.id)]["total"]["total_time"] += total_time
            self.save()

            print(f'{member.guild.id}/{before.channel.id}')
            print(f'{member.id}: Leave Voice {total_time}')

async def setup(bot):
    await bot.add_cog(voice(bot))