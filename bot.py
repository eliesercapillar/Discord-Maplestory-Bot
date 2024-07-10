import discord
from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True # NOQA
        super().__init__(command_prefix='/', intents=intents)

    async def setup_hook(self):
        try:
            synced = await self.tree.sync()
            print(f'Synced {len(synced)} commands for {self.user}.')
        except Exception as ex:
            print(ex)
