import discord
from discord import app_commands
from discord.ext import commands

import database as db

import typing
from PIL import Image, ImageDraw, ImageFont
import requests

class profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="set_profile", description="Setting Profile bio")
    async def set_profile(self, interaction: discord.Interaction, bio: str):
        player = await db.player[f"{interaction.guild.id}"].find_one({"_id": interaction.user.id})
        if player is None:
            await db.player[f"{interaction.guild.id}"].insert_one(
                {
                    "_id": interaction.user.id,
                    "profile": {
                        "bio": bio
                        },
                    "game": {}
                    }
                )
            await interaction.response.send_message(f"Yeay! Kamu sudah mengatur biomu, sekarang kamu bisa join Game dari server ini")
        else:
            await db.player[f"{interaction.guild.id}"].update_one(
                {"_id": interaction.user.id},
                    {
                        "$set": {
                            "profile.bio": bio
                            }
                        }
                    )
            await interaction.response.send_message(f"Kamu sudah memperbarui bio kamu")
        
    @app_commands.command(name="profile", description="Profile")
    @app_commands.describe(game="Refreshing")
    @app_commands.choices(
        game=[
            app_commands.Choice(name="RPG", value="0"),
            app_commands.Choice(name="Unknown", value="1")
            ]
        )
    async def profile(self, interaction:discord.Interaction, member:discord.Member, game: typing.Optional[app_commands.Choice[str]] = None,):
        if member is None and game is None:
            await interaction.response.send_message("ya kamu harus milih dulu dong dengan pilihan yang sudah tersedia")
        elif game is None:
            await interaction.response.send_message(f"ini profilmu {member}")
        elif member is None:
            await interaction.response.send_message(f"Kamu harus memilih membernya terlebih dulu")
        else:
            if game.value == "0":
                player = await db.player[f"{interaction.guild.id}"].find_one({"_id": member.id})
                if player is None:
                    await interaction.response.send_message("User belum set_profile")
                else:
                    check = player.get("game", {}).get("rpg", {})
                    if check is not None and check :
                        with Image.open("rpg/assets/profile/default.png") as a:
                            avatar_url = interaction.user.display_avatar
                            username = interaction.user.name

                            bar = player.get("game", {}).get("rpg", {}).get("bar", {})
                            exp = bar.get("exp", {})
                            hp = bar.get("hp", {})
                            mana = bar.get("mana", {})

                            stats = player.get("game", {}).get("rpg", {}).get("stats", {})
                            vitality = stats.get("vit", {})
                            agility = stats.get("agi", {})
                            inteligent = stats.get("int", {})
                            strength = stats.get("str", {})

                            head = player.get("game", {}).get("rpg", {}).get("use", {}).get("head", {})
                            headstr = head.get("str", 0)
                            headvit = head.get("vit", 0)
                            headint = head.get("int", 0)
                            headagi = head.get("agi", 0)

                            statsvitality = headvit + 123
                            statsagility = headagi
                            statsinteligent = headint
                            statsstrength = headstr

                            attribut = player.get("game", {}).get("rpg", {}).get("attribut", {})
                            fire = attribut.get("fire", {})
                            water = attribut.get("water", {})
                            earth = attribut.get("earth", {})
                            wind = attribut.get("wind", {})

                            c = ImageFont.truetype("arial.ttf", 15)
                            b = ImageDraw.Draw(a)
                            avatar = Image.open(requests.get(avatar_url, stream=True).raw)
                            avatar_image = avatar.resize((70, 70))
                            avatar_position = (4, 24)
                            
                            a.paste(avatar_image, avatar_position)

                            b.text((4, 2), username, font=c, fill="blue")
                            b.text((80, 23), f"vit\nagi\nint\nstr", font=c, fill="red")
                            b.text((100, 23), ":\n:\n:\n:", font=c, fill="red")
                            b.text((105, 23), f"{vitality} ({statsvitality})\n{agility} ({statsagility})\n{inteligent} ({statsinteligent})\n{strength} ({statsstrength})", font=c, fill="red")

                            b.text((200, 23), f"fire\nwind\nwater\nearth", font=c, fill="red")
                            b.text((235, 23), ":\n:\n:\n:", font=c, fill="red")
                            b.text((240, 23), f"{fire}\n{wind}\n{water}\n{earth}", font=c, fill="red")

                            b.text((4, 95), f"exp\nhp\nmana", font=c, fill="red")
                            b.text((45, 95), ":\n:\n:\n:", font=c, fill="red")
                            b.text((50, 95), f"{exp}\n{hp}\n{mana}", font=c, fill="red")

                            a.save(f"rpg/stats/profile/{interaction.guild.id}.png")
                            await interaction.response.send_message(file=discord.File(f"rpg/stats/profile/{interaction.guild.id}.png"))
                            #await interaction.response.send_message("user sudah punya game rpg")
                    else:
                        await interaction.response.send_message("user belum punya game rpg")
            elif game.value == "1":
                await interaction.response.send_message("Unknown")

async def setup(bot):
    await bot.add_cog(profile(bot))