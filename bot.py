import discord
from discord.ext import commands
import os
import asyncio
import importlib

from cogs.data_store_module import DataStore

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

data_store = DataStore()  # ✅ Properly initialize your DataStore here
bot.data_store = data_store  # ✅ Then attach to bot

GUILD_ID = int(os.getenv("GUILD_ID"))  # Add this to your Railway environment variables
TOKEN = os.getenv("BOT_TOKEN")         # Also add BOT_TOKEN in Railway

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

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} (ID: {bot.user.id})")
    try:
        synced = await bot.tree.sync(guild=discord.Object(id=GUILD_ID))
        print(f"🔁 Synced {len(synced)} commands.")
    except Exception as e:
        print(f"❌ Failed to sync commands: {e}")

async def load_all_cogs():
    for cog_path in COGS:
        try:
            module = importlib.import_module(cog_path)
            await module.setup(bot, data_store)
            print(f"🔹 Loaded {cog_path}")
        except Exception as e:
            print(f"❌ Failed to load {cog_path}: {e}")

async def main():
    async with bot:
        await load_all_cogs()
        await bot.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
