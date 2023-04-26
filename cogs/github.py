import discord
from discord import app_commands
from discord.ext import commands
from requests_html import AsyncHTMLSession
session = AsyncHTMLSession()


class Github(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="github", description="Fetch github user")
    @app_commands.describe(
        username = "github username"
    )
    async def github(self, interaction: discord.Interaction, username: str):
        try:
            await interaction.response.defer()
            # fetching info
            result = await session.get(f"https://api.github.com/users/{username}") # type: ignore
            result = result.json()

            # creating embed
            embed = discord.Embed(
                title=result['name'],
                url=f"https://github.com/{username}"
            )
            embed.set_thumbnail(url=result['avatar_url'])
            embed.add_field(name="Last Active", value=result['updated_at'])
            embed.add_field(name="Created At", value=result['created_at'])
            embed.add_field(name="Follower Count", value=result['followers'])
            embed.add_field(name="Following Count", value=result['following'])
            embed.add_field(name="Public Repos", value=result['public_repos'])

            if not result['location'] == None:
                embed.add_field(name="Location",value=result['location'])
                
            if not result['twitter_username'] == None:
                embed.add_field(name="Linked Twitter",value=result['twitter_username'])

            if not result['type'] == None:
                embed.add_field(name="Account Type",value=result['type'])

            if not result['bio'] == None:
                embed.description = result["bio"]

            return await interaction.followup.send(embed=embed)
        except Exception as err:
            print(err)
            return await interaction.followup.send(f"I ran into an error looking up the account {username}, it may not exist.")



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Github(bot), guilds= [discord.Object(id = 906257708594896976)])
