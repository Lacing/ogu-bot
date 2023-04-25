import discord
from discord import app_commands
from discord.ext import commands
from requests_html import AsyncHTMLSession
session = AsyncHTMLSession()


class soloto(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="soloto", description="Fetch solo.to user")
    @app_commands.describe(
        username = "solo.to username"
    )
    async def soloto(self, interaction: discord.Interaction, username: str):
        try:
            await interaction.response.defer()
            # fetching info
            result = await session.get(f"https://api.solo.to/{username}") # type: ignore
            result = result.json()
            
            # fetching last active
            last_active = result['status']['recent_update']
            if not last_active:
                last_active = "N/A"

            # fetching subscribed
            subscribed = result['status']['upgraded']

            # fetching bio
            bio = result['bio']

            # fetching location
            location = result['location']

            # fetching badge
            badge = result['badge']

            # creating embed
            embed = discord.Embed(
                title=result['name'],
                url=f"https://solo.to/{username}"
            ).set_thumbnail(url=result['avatar']).add_field(name="Last Active", value=last_active).add_field(name="Paid Account", value=subscribed)

            if not bio is None:
                embed.description = bio
            
            if not location is None:
                embed.add_field(name="Location", value=location)

            if not badge is None:
                embed.add_field(name="Badge", value=badge)
            
            if result['status']['has_links']:
                endArr = []

                result2 = await session.get(f"https://solo.to/{username}") # type: ignore
                await result2.html.arender() # type: ignore

                links = result2.html.find(".link-button") # type: ignore
                
                for link in links:
                    endArr.append(link.links.pop())

                embed.add_field(name="Links", value="\n".join(endArr), inline=False)

            return await interaction.followup.send(embed=embed)
        except Exception as err:
            print(err)
            return await interaction.followup.send(f"I ran into an error looking up the account {username}, it may not exist.")



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(soloto(bot), guilds= [discord.Object(id = 906257708594896976)])
