from PIL import Image, ImageDraw, ImageFont
import io
import os

def generate_animated_profile_card(user_data):
    """
    Creates an animated GIF profile card.
    - ELO number will count up
    - Rank icon will fade/pulse slightly
    """
    frames = []
    steps = 10
    final_elo = user_data.get("elo", 0)

    rank, rank_icon_path = get_rank_and_icon(final_elo)
    base = Image.open("assets/profile_bg.png").convert("RGBA")
    rank_icon = Image.open(rank_icon_path).convert("RGBA").resize((160, 160))

    try:
        font_large = ImageFont.truetype("arial.ttf", 36)
        font_small = ImageFont.truetype("arial.ttf", 24)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    name = user_data.get("name", "Unknown")
    wins = user_data.get("wins", 0)
    losses = user_data.get("losses", 0)

    for i in range(1, steps + 1):
        current_elo = int(final_elo * (i / steps))
        glow_alpha = int(150 + (105 * (i % 2)))  # pulse effect

        frame = base.copy()
        draw = ImageDraw.Draw(frame)

        draw.text((220, 40), f"{name}", font=font_large, fill="white")
        draw.text((220, 100), f"ELO: {current_elo}", font=font_small, fill="lightgray")
        draw.text((220, 140), f"Rank: {rank}", font=font_small, fill="lightblue")
        draw.text((220, 170), f"Wins: {wins} | Losses: {losses}", font=font_small, fill="gray")

        # Apply glowing effect to icon
        icon = rank_icon.copy()
        glow_layer = Image.new("RGBA", icon.size, (255, 255, 255, glow_alpha))
        icon = Image.alpha_composite(icon, glow_layer)
        frame.paste(icon, (30, 30), icon)

        frames.append(frame)

    # Export animated GIF
    buffer = io.BytesIO()
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0,
        disposal=2
    )
    buffer.seek(0)
    return buffer
