from discord.ext import commands
import json
import os

class reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_react = self.load_user_react()

    def load_user_react(self):
        if os.path.exists("user_react.json"):
            with open("user_react.json", "r") as file:
                return json.load(file)
        return {}

    def save_user_react(self):
        with open("user_react.json", "w") as file:
            json.dump(self.user_react, file, indent=4)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print(f'{reaction.message.guild.id}/{reaction.message.channel.id}/{reaction.message.id} ')
        print(f"{reaction.message.author.id}: {reaction.message.content} < {user.id}: {reaction.emoji}")

        user_id = str(user.id)
        if user_id not in self.user_react:
            self.user_react[user_id] = {"react": 0, "reacted": 0}
        self.user_react[user_id]["react"] += 1

        message_author_id = str(reaction.message.author.id)
        if message_author_id not in self.user_react:
            self.user_react[message_author_id] = {"react": 0, "reacted": 0}
        self.user_react[message_author_id]["reacted"] += 1

        self.save_user_react()

async def setup(bot):
    await bot.add_cog(reaction(bot))