import discord
# bot.py

import discord
from discord.ext import commands
from utils.data_store_manager import DataStore  # Adjust if renamed
import os
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
data_store = DataStore()

TOKEN = os.getenv("BOT_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))

COGS = [
    # Core / Queue System
    "cogs.queue_management_module",
    "cogs.matchmaking_module",
    "cogs.registration_module",
    "cogs.match_flow_module",

    # Leaderboards & Stats
    "cogs.leaderboard_module",
    "cogs.stats_leaderboard_module",
    "cogs.stats_leaderboard_role_season_module",
    "cogs.season_leaderboard_module",

    # User Features
    "cogs.nickname_module",
    "cogs.user_profile_module",
    "cogs.user_management_module",
    "cogs.premium_module",

    # Match Processing
    "cogs.match_reporting_module",
    "cogs.match_history_module",
    "cogs.match_analytics_module",

    # Party / Captain Features
    "cogs.party_system_module",
    "cogs.captain_ui_module",

    # Challenges & Customization
    "cogs.challenge_module",
    "cogs.custom_game_modes_module",
    "cogs.custom_notifications_module",

    # Moderation & Admin
    "cogs.admin_tools_module",
    "cogs.moderation_module",
    "cogs.voice_text_management_module",

    # Language & Localization
    "cogs.multi_language_support_module",
    "cogs.language_localization_module",

    # Season & Review
    "cogs.season_management_module",
    "cogs.review_reporting_module",

    # Extra
    "cogs.reminders_module",
    "cogs.map_management_module",
    "cogs.webhooks_module",
    "cogs.utils"
]

@bot.event
async def on_ready():
    print(f"✅ Bot is online as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"🌐 Synced {len(synced)} application commands.")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

async def load_extensions():
    for cog in COGS:
        try:
            await bot.load_extension(cog, data_store=data_store)
            print(f"📦 Loaded: {cog}")
        except Exception as e:
            print(f"❌ Failed to load {cog}: {e}")

if __name__ == "__main__":
    asyncio.run(load_extensions())
    bot.run(os.getenv("DISCORD_TOKEN"))
