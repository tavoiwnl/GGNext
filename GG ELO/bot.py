import os
import discord
from discord.ext import commands
from utils.data_store_manager import DataStore
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="/", intents=intents)

# Load Data Store
data_store = DataStore()

# Set your GUILD_ID for fast slash command registration
guild_id = int(os.getenv("GUILD_ID")) if os.getenv("GUILD_ID") else None

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    try:
        if guild_id:
            await bot.tree.sync(guild=discord.Object(id=guild_id))
            print(f"🔁 Synced commands to guild {guild_id}")
        else:
            await bot.tree.sync()
            print("🌍 Synced global commands")
    except Exception as e:
        print(f"❌ Sync error: {e}")

@bot.event
async def setup_hook():
    # Auto-load all cogs from your list
    cog_paths = [
        "cogs.admin_tools_module",
        "cogs.captains_ui_module",
        "cogs.challenge_module",
        "cogs.custom_game_modes_module",
        "cogs.custom_notifications_module",
        "cogs.data_manager",
        "cogs.data_store_module",
        "cogs.language_localization_module",
        "cogs.map_management_module",
        "cogs.match_analytics_module",
        "cogs.match_flow_module",
        "cogs.match_history_module",
        "cogs.match_reporting_module",
        "cogs.moderation",
        "cogs.moderation_module",
        "cogs.multi_language_support_module",
        "cogs.nickname",
        "cogs.nickname_module",
        "cogs.party_system",
        "cogs.party_system_module",
        "cogs.premium_module",
        "cogs.queue_management_module",
        "cogs.reminders_module",
        "cogs.review_reporting",
        "cogs.review_reporting_module",
        "cogs.season_leaderboard_module",
        "cogs.season_management_module",
        "cogs.user_management",
        "cogs.user_management_module",
        "cogs.user_profile_module",
        "cogs.utils",
        "cogs.voice_text_management_module",
        "cogs.webhooks_module",
    ]

    for cog in cog_paths:
        try:
            await bot.load_extension(cog, data_store=data_store)
            print(f"✅ Loaded {cog}")
        except Exception as e:
            print(f"❌ Failed to load {cog}: {e}")

# Run the bot with your Railway token
if __name__ == "__main__":
    token = os.getenv("DISCORD_TOKEN")
    if not token:
        raise ValueError("🚫 DISCORD_TOKEN environment variable not set.")
    bot.run(token)
