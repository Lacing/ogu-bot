import discord
from discord import app_commands
from discord.ext import commands
from requests_html import HTMLSession
session = HTMLSession()


class soloto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="soloto", description="Fetch solo.to user")
    @app_commands.describe(
        username = "solo.to username"
    )
    async def soloto(self, interaction: discord.Interaction, username: str):
        try:
            # fetching info
            result = session.get(f"https://api.solo.to/{username}")
            result = result.json()
            
            # fetching last active
            last_active = result['recent_update']
            if not last_active:
                last_active = "N/A"

            # creating embed
            embed = discord.Embed(
                title=result['name'],
                url=f"https://solo.to/{username}",
                color=result['theme_color']
            ).set_thumbnail(url=result['avatar']).add_field(name="Last Active", value={})

            return await interaction.response.send_message("temp")
        except Exception as err:
            print(err)
            return await interaction.response.send_message(f"I ran into an error looking up the account {username}")



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(soloto(bot), guilds= [discord.Object(id = 906257708594896976)])
