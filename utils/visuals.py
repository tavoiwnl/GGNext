from PIL import Image, ImageDraw, ImageFont, ImageSequence
import numpy as np
import io
import math

def generate_smoky_animated_profile_card(user_data):
    width, height = 600, 250
    steps = 20  # Number of animation frames
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Adjust if needed

    try:
        font_large = ImageFont.truetype(font_path, 36)
        font_small = ImageFont.truetype(font_path, 24)
    except:
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    def generate_smoke_frame(frame_idx):
        frame = Image.new("RGBA", (width, height), (10, 10, 10, 255))
        draw = ImageDraw.Draw(frame)

        for i in range(40):
            x = int(width / 2 + 200 * math.sin((frame_idx + i) * 0.3 + i))
            y = int(height / 2 + 100 * math.cos((frame_idx + i) * 0.2 + i))
            radius = 80
            smoke_color = (120, 120, 120, int(80 + 50 * math.sin(frame_idx * 0.5 + i)))
            draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=smoke_color)

        return frame

    frames = []
    for i in range(steps):
        base = generate_smoke_frame(i)

        draw = ImageDraw.Draw(base)
        draw.text((40, 30), user_data.get("name", "Unknown"), font=font_large, fill="white")
        draw.text((40, 90), f"ELO: {user_data.get('elo', 0)}", font=font_small, fill="lightgray")
        draw.text((40, 120), f"Wins: {user_data.get('wins', 0)}", font=font_small, fill="gray")
        draw.text((40, 150), f"Losses: {user_data.get('losses', 0)}", font=font_small, fill="gray")

        frames.append(base)

    buffer = io.BytesIO()
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=120,
        loop=0,
        disposal=2
    )
    buffer.seek(0)
    return buffer

# Sample user data for demonstration
sample_user_data = {
    "name": "GGNext Player",
    "elo": 1740,
    "wins": 42,
    "losses": 18
}

gif_buffer = generate_smoky_animated_profile_card(sample_user_data)
