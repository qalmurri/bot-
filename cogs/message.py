from discord.ext import commands
import json
import os

class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = "stats/message.json"
        self.file_json = {"chat": 0, "reply": 0, "replied": 0, "delete": 0}
        self.user_message = self.load_user_message()

        if not os.path.exists("stats"):
            os.mkdir("stats")

    def load_user_message(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        return {}

    def save_user_message(self):
        with open(self.file_path, "w") as file:
            json.dump(self.user_message, file, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.reference and message.author != self.bot.user:
            a = await message.channel.fetch_message(message.reference.message_id)
            if a:
                user_id = str(message.author.id)
                if user_id not in self.user_message:
                    self.user_message[user_id] = self.file_json
                self.user_message[user_id]["reply"] += 1
                self.user_message[user_id]["chat"] += 1

                message_author_id = str(a.author.id)
                if message_author_id not in self.user_message:
                    self.user_message[message_author_id] = self.file_json
                self.user_message[message_author_id]["replied"] += 1
                self.save_user_message()

                print(f"{message.guild.id}/{message.channel.id}/{message.id}")
                print(f"{a.author.id}: {a.content} < {message.author.id}: {message.content}")
        else:
            user_id = str(message.author.id)
            if user_id not in self.user_message:
                self.user_message[user_id] = self.file_json
            self.user_message[user_id]["chat"] += 1
            self.save_user_message()
            print(f'{message.guild.id}/{message.channel.id}')
            print(f'{message.author.id}: {message.content}')

            await self.bot.process_commands(message)

    @commands.Cog.listener()
    async def on_message_delete(self, message):        
        user_id = str(message.author.id)
        if user_id in self.user_message:
            self.user_message[user_id] = self.file_json
        self.user_message[user_id]["delete"] += 1
        self.save_user_message()
            

async def setup(bot):
    await bot.add_cog(message(bot))