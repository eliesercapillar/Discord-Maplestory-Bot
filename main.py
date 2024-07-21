import os
import io
import re
import pytesseract
from PIL import Image
import discord
from typing import Final
from dotenv import load_dotenv
from discord import app_commands
from bot import Bot

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize Bot
bot = Bot()


@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is up and running!')


@bot.tree.command(name="flame", description="Upload a screenshot of your equipment and get it's flame score breakdown.")
@app_commands.describe(equipment="Upload a screenshot of equipment")
async def flame(interaction: discord.Interaction, equipment: discord.Attachment):
    if equipment.content_type.startswith('image/'):
        image_data = await equipment.read()
        img = Image.open(io.BytesIO(image_data))

        text = pytesseract.image_to_string(img)
        #flames_info = extract_flames(text)

        await interaction.response.send_message(f'used the flame command with the passed parameter: {equipment}\nText found is {text}')
    else:
        await interaction.response.send_message("The uploaded file is not a valid image.", ephemeral=True)


def extract_flames(text: str):
    # Regex to find lines with green numbers (flames)
    flame_pattern = re.compile(r'\((\+\d+)\)')
    flames = flame_pattern.findall(text)

    # Identify the individual flames and their tiers
    flame_tiers = analyze_flames(flames)

    return flame_tiers


def analyze_flames(flames):
    # Simplified tier determination logic (based on example data)
    tier_dict = {
        '+12': 'Tier 4',
        '+28': 'Tier 6',
        # Add more mappings as needed
    }

    flame_tiers = {flame: tier_dict.get(flame, 'Unknown Tier') for flame in flames}

    return flame_tiers


if __name__ == '__main__':
    bot.run(token=TOKEN)
