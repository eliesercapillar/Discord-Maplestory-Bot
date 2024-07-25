import os
import io
import re
import cv2
import pytesseract
import numpy as np
from PIL import Image
import discord
from typing import Final
from dotenv import load_dotenv
from discord import app_commands
from bot import Bot
import tempfile
from util import get_limits
import easyocr

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Initialize Bot
bot = Bot()
reader = easyocr.Reader(['en'])
green = [0, 255, 204]  # Maplestory Flame Green in BGR colorspace

@bot.event
async def on_ready() -> None:
    print(f'{bot.user} is up and running!')


@bot.tree.command(name="flame", description="Upload a screenshot of your equipment and get its flame score breakdown.")
@app_commands.describe(equipment="Upload a screenshot of equipment")
async def flame(interaction: discord.Interaction, equipment: discord.Attachment):
    if equipment.content_type.startswith('image/'):
        image_data = await equipment.read()
        img = Image.open(io.BytesIO(image_data))
        preprocessed_images = preprocess_image(img)

        # Load the binary image for Tesseract OCR
        binary_image = cv2.imread(preprocessed_images["binary"], cv2.IMREAD_GRAYSCALE)

        # Use pytesseract to extract text from the preprocessed image
        # custom_config = r'--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789+% '
        custom_config = r'-c tessedit_char_whitelist=0123456789+% '
        # text = pytesseract.image_to_string(preprocessed_images["mask"], config=custom_config)
        result = reader.readtext(preprocessed_images["mask"], detail=0, allowlist ='0123456789+%')

        # Send the preprocessed images and extracted text back to the user
        await interaction.response.send_message(
            f'Used the flame command with the passed parameter: {equipment.filename}\nText found is:\n{result}')
        await interaction.followup.send(files=[
            discord.File(preprocessed_images["original"], 'original_image.png'),
            discord.File(preprocessed_images["hsv"], 'hsv_image.png'),
            discord.File(preprocessed_images["mask"], 'mask.png'),
            discord.File(preprocessed_images["green_text"], 'green_text.png'),
            discord.File(preprocessed_images["gray"], 'gray_image.png'),
            discord.File(preprocessed_images["binary"], 'binary_image.png')
        ])

        # Remove the temporary files
        for path in preprocessed_images.values():
            os.remove(path)
    else:
        await interaction.response.send_message("The uploaded file is not a valid image.", ephemeral=True)


def preprocess_image(image: Image):
    """
    Preprocess the image to isolate green text and visualize intermediate steps.
    """
    open_cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    hsv_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2HSV)

    # Save the original and HSV images for debugging
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        original_img_path = temp_file.name
        cv2.imwrite(original_img_path, open_cv_image)

    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        hsv_img_path = temp_file.name
        cv2.imwrite(hsv_img_path, hsv_image)

    # Define the range for green color in HSV
    lower_limit, upper_limit = get_limits(green)

    # Create a mask for green color
    mask = cv2.inRange(hsv_image, lower_limit, upper_limit)

    # Save the mask for debugging
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        mask_path = temp_file.name
        cv2.imwrite(mask_path, mask)

    # Bitwise-AND mask and original image to isolate green text
    green_text = cv2.bitwise_and(open_cv_image, hsv_image, mask=mask)

    # Save the isolated green text for debugging
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        green_text_path = temp_file.name
        cv2.imwrite(temp_file.name, green_text)

    # Convert the masked image to grayscale
    gray_image = cv2.cvtColor(green_text, cv2.COLOR_BGR2GRAY)

    # Save the grayscale image for debugging
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        gray_image_path = temp_file.name
        cv2.imwrite(temp_file.name, gray_image)

    # Apply thresholding to get a binary image
    _, binary_image = cv2.threshold(gray_image, 1, 255, cv2.THRESH_BINARY)

    # Save the binary image for debugging
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        binary_image_path = temp_file.name
        cv2.imwrite(temp_file.name, binary_image)

    return {
        "original": original_img_path,
        "hsv": hsv_img_path,
        "mask": mask_path,
        "green_text": green_text_path,
        "gray": gray_image_path,
        "binary": binary_image_path
    }


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
