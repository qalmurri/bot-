from discord.ext import commands
import json
import os

class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def guild_folder(self, message):
        guild_id = message.guild.id
        directory = f"stats/{guild_id}/"
        self.file_path = f"stats/{guild_id}/message.json"
        self.user_message = self.load()
        if not os.path.exists(directory):
            os.makedirs(directory)

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        return {}

    def save(self):
        with open(self.file_path, "w") as file:
            json.dump(self.user_message, file, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        self.guild_folder(message)
        user_id = str(message.author.id)

        if user_id not in self.user_message:
            self.user_message[user_id] = {"chat": 0, "delete": 0}
        self.user_message[user_id]["chat"] += 1
        self.save()
        await self.bot.process_commands(message)

        print(f'{message.guild.id}/{message.channel.id}')
        print(f'{message.author.id}: {message.content}')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.guild_folder(message)
        user_id = str(message.author.id)

        if user_id in self.user_message:
            self.user_message[user_id]["delete"] += 1
        self.save()

async def setup(bot):
    await bot.add_cog(message(bot))