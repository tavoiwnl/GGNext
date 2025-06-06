# /bot_project_root/bot.py
import discord
from discord.ext import commands
import os
import asyncio
import importlib
from flask import Flask
import threading

from cogs.data_store_module import DataStore

# Set up the bot with necessary intents
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

# Initialize DataStore and attach it to the bot
data_store = DataStore()  # ✅ Properly initialize your DataStore here
bot.data_store = data_store  # ✅ Then attach to bot

# Read environment variables (ensure to set these in your environment variables on Railway)
GUILD_ID = int(os.getenv("GUILD_ID"))  # Add this to your Railway environment variables
print(f"🔍 Using GUILD_ID: {GUILD_ID}")
TOKEN = os.getenv("BOT_TOKEN")         # Also add BOT_TOKEN in Railway

# List of all cogs to load dynamically
COGS = [
    "cogs.admin_tools_module",
    "cogs.captains_ui_module",
    "cogs.challenge_module",
    "cogs.custom_game_modes_module",
    "cogs.custom_notifications_module",
    "cogs.language_localization_module",
    "cogs.map_management_module",
    "cogs.match_analytics_module",
    "cogs.match_flow_module",
    "cogs.match_history_module",
    "cogs.match_reporting_module",
    "cogs.moderation_module",
    "cogs.multi_language_support_module",
    "cogs.nickname_module",
    "cogs.party_system_module",
    "cogs.premium_module",
    "cogs.queue_management_module",
    "cogs.reminders_module",
    "cogs.review_reporting_module",
    "cogs.season_leaderboard_module",
    "cogs.season_management_module",
    "cogs.user_management_module",
    "cogs.user_profile_module",
    "cogs.voice_text_management_module",
    "cogs.webhooks_module",
    "cogs.utils"
]

# Initialize Flask app to keep the bot alive
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"  # Responds with a basic message

def run_flask():
    """Function to run Flask in a separate thread."""
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

# Function to load all cogs dynamically
async def load_all_cogs():
    for cog_path in COGS:
        try:
            # Dynamically load each cog using importlib
            module = importlib.import_module(cog_path)
            await module.setup(bot, data_store)  # Ensure each cog has a setup function that passes bot and data_store
            print(f"🔹 Loaded {cog_path}")
        except Exception as e:
            print(f"❌ Failed to load {cog_path}: {e}")

# Event that triggers when the bot is ready
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        # Sync slash commands globally
        synced = await bot.tree.sync()  # Global sync fallback
        print(f"🌍 Globally synced {len(synced)} commands.")
    except Exception as e:
        print(f"❌ Global sync failed: {e}")

# Main async function to start the bot and load cogs
async def main():
    async with bot:
        # Load all cogs and then start the bot
        await load_all_cogs()
        await bot.start(TOKEN)

# Start Flask server in a separate thread
thread = threading.Thread(target=run_flask)
thread.start()

# Run the bot asynchronously
if __name__ == "__main__":
    asyncio.run(main())




