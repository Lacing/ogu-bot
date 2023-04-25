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
        username = "roblox username"
    )
    async def roblox(self, interaction: discord.Interaction, username: str):
        try:
            # fetching roblox user
            robloxuser = await client.get_user_by_username(username)

            # creating display name
            name = robloxuser.name
            if not name == robloxuser.display_name:
                name = f"{robloxuser.display_name} ({name})"

            # fetching roblox user badges
            badges = await robloxuser.get_roblox_badges()
            roblox_badges = []
            for badge in badges:
                roblox_badges.append(badge.name)
            # fetching roblox user avatar
            avatar = await robloxuser.thumbnails.get_avatar_image(shot_type=thumbnails.ThumbnailType.avatar_headshot, size=thumbnails.ThumbnailSize.size_75x75)

            # fetching roblox user creation date
            createdUnix = int(str(datetime.datetime.strptime(str(robloxuser.created).split('.')[0], '%Y-%m-%d %H:%M:%S').timestamp()).split(".")[0])

            # fetching following/follower count
            followerCount = await robloxuser.get_followers_count()
            followingCount = await robloxuser.get_followings_count()

            # fetching friend count
            friendsCount = await robloxuser.get_friends_count()

            # embedded message
            return await interaction.response.send_message(
            embed=discord.Embed(
                title=name,
                url=f"https://roblox.com/users/{robloxuser.id}/profile",
                description=f"{robloxuser.description}"
            )
            .set_footer(text=f"ID: {robloxuser.id}")
            .add_field(name="Created", value=f"<t:{createdUnix}:f>")
            .add_field(name=f"Badges ({len(badges)})", value=", ".join(roblox_badges))
            .add_field(name="Follower Count", value=followerCount)
            .add_field(name="Following Count", value=followingCount)
            .add_field(name="Friend Count", value=friendsCount)
            .set_thumbnail(url=avatar)
        )
        except Exception as err:
            print(err)
            return await interaction.response.send_message(f"I ran into an error looking up the account {username}")



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Roblox(bot), guilds= [discord.Object(id = 906257708594896976)])
