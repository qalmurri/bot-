import discord
from discord import app_commands
from discord.ext import commands
import json
import os
import requests

from PIL import Image, ImageDraw, ImageFont

class profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setbackground", description="PROFILE: Add image link to change the profile background (png/gif) or type: default.")
    async def setbackground(self, interaction: discord.Interaction, link_image: str):
        self.file_path = f"stats/{interaction.guild.id}/setting.json"
        self.user_setprofile = self.load()

        makedirs = f"stats/{interaction.guild.id}/background"
        if not os.path.exists(makedirs):
            os.makedirs(makedirs)

        if str(interaction.user.id) not in self.user_setprofile:
            self.user_setprofile[str(interaction.user.id)] = {"profile_background": "default"}

        if link_image == "default":
            self.user_setprofile[str(interaction.user.id)]["profile_background"] = "default"
            self.save()
            await interaction.response.send_message("Sudah berganti menjadi default", ephemeral=True)
        else:
            try:
                response = requests.get(link_image)
                response.raise_for_status()
                image_data = response.content

                content_type = response.headers.get("content-type")
                if content_type == "image/png":
                    image_extension = "png"
                elif content_type == "image/gif":
                    image_extension = "gif"
                else:
                    await interaction.response.send_message("Format hanya png & gif")
                    return

                image_filename = f"stats/{interaction.guild.id}/background/{interaction.user.id}.{image_extension}"
                with open(image_filename, "wb") as image_file:
                    image_file.write(image_data)

                self.user_setprofile[str(interaction.user.id)]["profile_background"] = image_filename
                self.save()

                await interaction.response.send_message("Gambar sudah terupdate.", ephemeral=True)
            except requests.exceptions.RequestException:
                await interaction.response.send_message("Gagal Mendownload", ephemeral=True)
        
    def load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return {}
        
    def save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.user_setprofile, f, indent=4)

    @app_commands.command(name="profile", description="PROFILE: See user profile")
    async def profile(self, interaction:discord.Interaction, member:discord.Member):
        def load(filename):
            try:
                with open(filename, "r") as file:
                    data = json.load(file)
                return data
            except FileNotFoundError:
                return {}
            
        makedirs = f"stats/{interaction.guild.id}/background"
        if not os.path.exists(makedirs):
            os.makedirs(makedirs)

        guild_id = interaction.guild_id
        user_message = load(f"stats/{guild_id}/message.json")
        user_react = load(f"stats/{guild_id}/react.json")
        user_setprofile = load(f"stats/{guild_id}/setting.json")

        user_data = {
            "chat": user_message.get(str(member.id), {}).get("chat", 0),
            "delete": user_message.get(str(member.id), {}).get("delete", 0),
            "edit": user_message.get(str(member.id), {}).get("edit", 0),
            "react": user_react.get(str(member.id), {}).get("react", 0),
            "reacted": user_react.get(str(member.id), {}).get("reacted", 0),
            "profile_background": user_setprofile.get(str(member.id), {}).get("profile_background", "default")
        }

        if user_data["profile_background"] == "default":
            with Image.open("assets/profile_background/default.png") as im:
                name_user = str(member)
                chat = str(user_data["chat"])
                avatar_url = member.display_avatar

                text_draw = ImageDraw.Draw(im)
                avatar = Image.open(requests.get(avatar_url, stream=True).raw)
                fnt = ImageFont.truetype("arial.ttf", 24)

                avatar_image = avatar.resize((80, 80))
                avatar_position = (10, 10)
                im.paste(avatar_image, avatar_position)

                text_draw.text((100, 8), name_user, font=fnt, fill="red")
                text_draw.text((100, 40), chat, font=fnt, fill="red")

                im.save(f"stats/{guild_id}/background/profile.png")
                await interaction.response.send_message(file=discord.File(f"stats/{guild_id}/background/profile.png"), ephemeral=True)
        else:
            await interaction.response.send_message(f'Chat: {user_data["chat"]}\nDelete: {user_data["delete"]}\nEdit: {user_data["edit"]}\nReact: {user_data["react"]}\nReacted: {user_data["reacted"]}', file=discord.File(user_data["profile_background"]), ephemeral=True)

async def setup(bot):
    await bot.add_cog(profile(bot))