from PIL import Image, ImageDraw, ImageFont
import io
import os

def generate_profile_card_image(user_data):
    """
    Generates a stylish profile card with background and rank icon.
    Requires:
    - A background image: `assets/profile_bg.png`
    - Rank icons in `assets/ranks/` (e.g., bronze.png, silver.png, etc.)
    """

    # Load background image
    bg_path = "assets/profile_bg.png"
    bg = Image.open(bg_path).convert("RGBA")
    draw = ImageDraw.Draw(bg)

    # Load font
    try:
        font_large = ImageFont.truetype("arial.ttf", 36)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Determine rank
    elo = user_data.get("elo", 0)
    rank, rank_icon = get_rank_and_icon(elo)

    # Draw text
    name = user_data.get("name", "Unknown")
    wins = user_data.get("wins", 0)
    losses = user_data.get("losses", 0)

    draw.text((220, 40), f"{name}", font=font_large, fill="white")
    draw.text((220, 100), f"ELO: {elo} ({rank})", font=font_small, fill="lightgray")
    draw.text((220, 140), f"Wins: {wins}", font=font_small, fill="green")
    draw.text((220, 170), f"Losses: {losses}", font=font_small, fill="red")

    # Paste rank icon
    if rank_icon:
        icon = Image.open(rank_icon).convert("RGBA").resize((160, 160))
        bg.paste(icon, (30, 30), icon)

    # Export to buffer
    buffer = io.BytesIO()
    bg.save(buffer, format="PNG")
    buffer.seek(0)
    return buffer

def get_rank_and_icon(elo):
    """
    Assign rank and corresponding icon based on ELO.
    You must place PNG icons in `assets/ranks/`.
    """
    if elo >= 2500:
        return "Legend", "assets/ranks/legend.png"
    elif elo >= 2000:
        return "Master", "assets/ranks/master.png"
    elif elo >= 1500:
        return "Gold", "assets/ranks/gold.png"
    elif elo >= 1000:
        return "Silver", "assets/ranks/silver.png"
    else:
        return "Bronze", "assets/ranks/bronze.png"
