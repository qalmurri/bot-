from discord.ext import commands
import json
import os

class message(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_message = self.load_user_message()

    def load_user_message(self):
        if os.path.exists("user_message.json"):
            with open("user_message.json", "r") as file:
                return json.load(file)
        return {}

    def save_user_message(self):
        with open("user_message.json", "w") as file:
            json.dump(self.user_message, file, indent=4)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.reference and message.author != self.bot.user:
            a = await message.channel.fetch_message(message.reference.message_id)
            if a:
                print(f"{message.guild.id}/{message.channel.id}/{message.id}")
                print(f"{a.author.id}: {a.content} < {message.author.id}: {message.content}")

                user_id = str(message.author.id)
                if user_id not in self.user_message:
                    self.user_message[user_id] = {"reply": 0, "replied": 0, "chat": 0}
                self.user_message[user_id]["reply"] += 1
                self.user_message[user_id]["chat"] += 1

                message_author_id = str(a.author.id)
                if message_author_id not in self.user_message:
                    self.user_message[message_author_id] = {"reply": 0, "replied": 0, "chat": 0}
                self.user_message[message_author_id]["replied"] += 1

                self.save_user_message()
        else:
            print(f'{message.guild.id}/{message.channel.id}')
            print(f'{message.author.id}: {message.content}')

            user_id = str(message.author.id)
            if user_id not in self.user_message:
                self.user_message[user_id] = {"reply": 0, "replied": 0, "chat": 0}
            self.user_message[user_id]["chat"] += 1

            self.save_user_message()

            await self.bot.process_commands(message)

async def setup(bot):
    await bot.add_cog(message(bot))