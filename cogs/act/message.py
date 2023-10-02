from discord.ext import commands
import json
import os

class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f'Exstension Message Ready')

    def guild(self, message):
        self.file_path = f"stats/{message.guild.id}/message.json"
        self.user_message = self.load()
        
        if not os.path.exists(f"stats/{message.guild.id}/"):
            os.makedirs(f"stats/{message.guild.id}/")

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return {}

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.user_message, f, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        self.guild(message)
 
        if str(message.author.id) not in self.user_message:
            self.user_message[str(message.author.id)] = {"chat": 0, "delete": 0, "edit": 0}
        self.user_message[str(message.author.id)]["chat"] += 1
        self.save()
    
        await self.bot.process_commands(message)

        print(f'{message.guild.id}/{message.channel.id}')
        print(f'{message.author.id}: {message.content}')

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.guild(message)

        if str(message.author.id) in self.user_message:
            self.user_message[str(message.author.id)]["delete"] += 1
        self.save()

        print(f'{message.guild.id}/{message.channel.id}')
        print(f'{message.author.id} delete: {message.content}')

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        self.guild(after)

        if str(after.author.id) in self.user_message:
            self.user_message[str(after.author.id)]["edit"] += 1
        self.save()

        print(f'{before.guild.id}/{before.channel.id}')
        print(f'{before.author.id} edit: {before.content}')

async def setup(bot):
    await bot.add_cog(message(bot))