import os
import discord
from typing import Final
from dotenv import load_dotenv
from discord import app_commands
from bot import Bot

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

# Initialize Bot
bot = Bot()


@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is up and running!')


@bot.tree.command(name="flame", description="Upload a screenshot of your equipment and get it's flame score breakdown.")
@app_commands.describe(equipment="Upload a screenshot of equipment")
async def flame(interaction: discord.Interaction, equipment: discord.Attachment):
    if equipment.content_type.startswith('image/'):
        await interaction.response.send_message(f'used the flame command with the passed parameter: {equipment}')
    else:
        await interaction.response.send_message("The uploaded file is not a valid image.", ephemeral=True)


if __name__ == '__main__':
    bot.run(token=TOKEN)
