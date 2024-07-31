import os
import random
import uuid

# Define the new naming components
language_name = "ENG"
font_name = "MAPLE"
file_extension = "png"

# Define the paths
data_folder = "S:/Repositories/Discord-Maplestory-Bot/data"  # Adjust this path if the script is in a different location
desired_extensions = ['.jpg', '.jpeg', '.png', '.PNG']  # Add any other extensions you want to include

# Get a list of all files in the data folder
files = os.listdir(data_folder)

# Filter only files with the desired extension (in this case, .jpg)
files = [f for f in files if any(f.endswith(ext) for ext in desired_extensions)]

# Initialize the counter
counter = 0


# Function to generate new file name
def generate_new_file_name(counter):
    return f"{language_name}.{font_name}.exp{counter}.{file_extension}"


# Rename the files
for file in files:
    # Generate new file name
    new_file_name = generate_new_file_name(counter)
    # new_file_name = uuid.uuid4().hex.upper()[0:6] + ".png"
    new_file_path = os.path.join(data_folder, new_file_name)

    # Define the full path for the old file name
    old_file_path = os.path.join(data_folder, file)

    # Rename the file
    os.rename(old_file_path, new_file_path)

    # Increment the counter for the next file
    counter += 1

print("Files renamed successfully.")