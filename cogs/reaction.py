from discord.ext import commands
import json
import os

class reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.file_path = "stats/react.json"
        self.user_react = self.load_user_react()

        if not os.path.exists("stats"):
            os.mkdir("stats")

    def load_user_react(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        return {}

    def save_user_react(self):
        with open(self.file_path, "w") as file:
            json.dump(self.user_react, file, indent=4)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        user_id = str(user.id)
        if user_id not in self.user_react:
            self.user_react[user_id] = {"react": 0, "reacted": 0}
        self.user_react[user_id]["react"] += 1

        message_author_id = str(reaction.message.author.id)
        if message_author_id not in self.user_react:
            self.user_react[message_author_id] = {"react": 0, "reacted": 0}
        self.user_react[message_author_id]["reacted"] += 1
        self.save_user_react()

        print(f'{reaction.message.guild.id}/{reaction.message.channel.id}/{reaction.message.id} ')
        print(f"{reaction.message.author.id}: {reaction.message.content} < {user.id}: {reaction.emoji}")

async def setup(bot):
    await bot.add_cog(reaction(bot))