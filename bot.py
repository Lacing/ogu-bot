import logging
import os
import sys

import discord
from discord.ext import commands

import config


class PhobosBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            case_insensitive=True,
            intents=discord.Intents.all(),
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="Phobos.gg",
            ),
            allowed_mentions=discord.AllowedMentions(roles=False, everyone=False, users=True)
        )
        self.logger = logging.getLogger("bot")

        self.admins = [249318304768983050]

    async def setup_hook(self) -> None:
        await self.load_cogs()
        await self.tree.sync(guild = discord.Object(id = 906257708594896976))

    async def on_ready(self):
        ...

    @staticmethod
    def setup_logging() -> None:
        logging.getLogger("discord").setLevel(logging.INFO)
        logging.getLogger("discord.http").setLevel(logging.WARNING)
        logging.basicConfig(
            level=logging.INFO,
            format="%(levelname)s | %(asctime)s | %(name)s | %(message)s",
            stream=sys.stdout,
        )

    async def load_cogs(self, directory="./cogs") -> None:
        for file in os.listdir(directory):
            if file.endswith(".py") and not file.startswith("_"):
                await self.load_extension(
                    f"{directory[2:].replace('/', '.')}.{file[:-3]}"
                )
                self.logger.info(f"Loaded: {file[:-3]}")
            elif not (
                file in ["__pycache__"] or file.endswith(("pyc", "txt"))
            ) and not file.startswith("_"):
                await self.load_cogs(f"{directory}/{file}")

        await self.load_extension("jishaku")


if __name__ == "__main__":
    bot = PhobosBot()
    bot.remove_command("help")
    bot.setup_logging()
    bot.run(config.TOKEN, log_handler=None)