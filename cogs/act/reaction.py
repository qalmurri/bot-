from discord.ext import commands
import json
import os

class reaction(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        print(f'Exstension Reaction Ready')

    def guild(self, member):
        self.file_path = f"stats/{member.guild.id}/react.json"
        self.user_react = self.load()

        if not os.path.exists(f"stats/{member.guild.id}/"):
            os.makedirs(f"stats/{member.guild.id}/")

    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return {}

    def save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.user_react, f, indent=4)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        self.guild(user)

        if str(user.id) not in self.user_react:
            self.user_react[str(user.id)] = {"react": 0, "reacted": 0}
        self.user_react[str(user.id)]["react"] += 1

        if str(reaction.message.author.id) not in self.user_react:
            self.user_react[str(reaction.message.author.id)] = {"react": 0, "reacted": 0}
        self.user_react[str(reaction.message.author.id)]["reacted"] += 1
        self.save()

        print(f'{reaction.message.guild.id}/{reaction.message.channel.id}/{reaction.message.id} ')
        print(f"{reaction.message.author.id}: {reaction.message.content} < {user.id}: {reaction.emoji}")

async def setup(bot):
    await bot.add_cog(reaction(bot))