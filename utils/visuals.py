from PIL import Image, ImageDraw, ImageFont
import io

def generate_profile_card_image(user_data):
    """
    Generate a basic profile card image using user stats.
    """
    # Create a blank image
    img = Image.new("RGB", (600, 200), color=(30, 30, 30))
    draw = ImageDraw.Draw(img)

    # Set up fonts (ensure ttf file is present or use default)
    try:
        font = ImageFont.truetype("arial.ttf", 24)
    except:
        font = ImageFont.load_default()

    # Write text
    draw.text((20, 20), f"Username: {user_data.get('name', 'Unknown')}", font=font, fill=(255, 255, 255))
    draw.text((20, 60), f"ELO: {user_data.get('elo', 0)}", font=font, fill=(255, 255, 255))
    draw.text((20, 100), f"Wins: {user_data.get('wins', 0)}", font=font, fill=(100, 255, 100))
    draw.text((20, 140), f"Losses: {user_data.get('losses', 0)}", font=font, fill=(255, 100, 100))

    # Save image to bytes
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer  # Can be sent directly via Discord's file=discord.File(...)
