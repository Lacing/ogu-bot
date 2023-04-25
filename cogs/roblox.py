import discord
from discord import app_commands
from discord.ext import commands
from ro_py import Client, thumbnails
client = Client()
import datetime


class Roblox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="roblox", description="Fetch roblox user")
    @app_commands.describe(
        username = "Your roblox username"
    )
    async def roblox(self, interaction: discord.Interaction, username: str):
        try:
            robloxuser = await client.get_user_by_username(username)
            badges = await robloxuser.get_roblox_badges()
            roblox_badges = []
            for badge in badges:
                roblox_badges.append(badge.name)
            avatar = await robloxuser.thumbnails.get_avatar_image(shot_type=thumbnails.ThumbnailType.avatar_headshot, size=thumbnails.ThumbnailSize.size_75x75)
            createdUnix = int(str(datetime.datetime.strptime(str(robloxuser.created).split('.')[0], '%Y-%m-%d %H:%M:%S').timestamp()).split(".")[0])

            return await interaction.response.send_message(
            embed=discord.Embed(
                title=f"{robloxuser.name}",
                url=f"https://roblox.com/users/{robloxuser.id}/profile",
                description=f"{robloxuser.description}"
            )
            .set_footer(text=f"ID: {robloxuser.id}")
            .add_field(name="Created", value=f"<t:{createdUnix}:f>")
            .add_field(name=f"Badges ({len(badges)})", value=", ".join(roblox_badges))
            .set_thumbnail(url=avatar)
        )
        except Exception as err:
            print(err)
            return await interaction.response.send_message(f"I ran into an error looking up the account {username}")



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Roblox(bot), guilds= [discord.Object(id = 906257708594896976)])
