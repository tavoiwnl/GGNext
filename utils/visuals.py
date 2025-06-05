# --- utils/visuals.py ---

from PIL import Image, ImageDraw, ImageFont
import numpy as np
import io
import math

def generate_smoky_animated_profile_card(user_data):
    width, height = 600, 250
    steps = 20  # Number of frames in the animation
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 20)

    frames = []
    for i in range(steps):
        frame = Image.new("RGBA", (width, height), (0, 0, 0, 255))
        draw = ImageDraw.Draw(frame)

        # Simulate smoke using semi-transparent ellipses
        for j in range(25):
            x = np.random.randint(0, width)
            y = np.random.randint(0, height)
            radius = np.random.randint(20, 80)
            opacity = int(60 + 40 * math.sin((i + j) / steps * 2 * math.pi))
            smoke_color = (200, 200, 200, opacity)
            draw.ellipse((x, y, x + radius, y + radius), fill=smoke_color)

        # Overlay text info
        draw.text((20, 20), f"Name: {user_data.get('name', 'Unknown')}", font=font, fill="white")
        draw.text((20, 60), f"Rank: {user_data.get('rank', 'Unranked')}", font=font, fill="white")
        draw.text((20, 100), f"ELO: {user_data.get('elo', 1000)}", font=font, fill="white")
        draw.text((20, 140), f"Wins: {user_data.get('wins', 0)}", font=font, fill="white")
        draw.text((20, 180), f"Losses: {user_data.get('losses', 0)}", font=font, fill="white")

        frames.append(frame)

    buffer = io.BytesIO()
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=100
    )
    buffer.seek(0)
    return buffer.read()

