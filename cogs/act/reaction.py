from discord.ext import commands
import json
import os

class reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    def guild_folder(self, member):
        guild_id = member.guild.id
        directory = f"stats/{guild_id}/"
        self.file_path = f"stats/{guild_id}/react.json"
        self.user_react = self.load()
        if not os.path.exists(directory):
            os.makedirs(directory)

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                return json.load(file)
        return {}

    def save(self):
        with open(self.file_path, "w") as file:
            json.dump(self.user_react, file, indent=4)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        self.guild_folder(user)
        user_id = str(user.id)
        message_author_id = str(reaction.message.author.id)

        if user_id not in self.user_react:
            self.user_react[user_id] = {"react": 0, "reacted": 0}
        self.user_react[user_id]["react"] += 1

        if message_author_id not in self.user_react:
            self.user_react[message_author_id] = {"react": 0, "reacted": 0}
        self.user_react[message_author_id]["reacted"] += 1
        self.save()

        print(f'{reaction.message.guild.id}/{reaction.message.channel.id}/{reaction.message.id} ')
        print(f"{reaction.message.author.id}: {reaction.message.content} < {user.id}: {reaction.emoji}")

async def setup(bot):
    await bot.add_cog(reaction(bot))