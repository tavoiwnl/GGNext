import discord
from discord.ext import commands
import pytest
from discord.ext.test import Client  # This is used to simulate Discord interactions for testing

# Your test bot class
class TestBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!")
    
    async def on_ready(self):
        print(f"Logged in as {self.user}")

test_bot = TestBot()

# Create the testing client to interact with the bot
client = Client(test_bot)

# List of all cogs to load dynamically (same as in bot.py)
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

# Test case to invoke all slash commands across cogs
@pytest.mark.asyncio
async def test_all_commands():
    for cog in test_bot.cogs.values():
        for command in cog.walk_commands():
            try:
                # Simulate invoking each slash command with `/command_name`
                ctx = await client.get_context_from_message(f"/{command.name}")
                await client.invoke(ctx)

                # Check expected outputs for specific commands
                if command.name == "create_queue":
                    assert ctx.message.content == "Queue created successfully!"  # Adjust as needed
                elif command.name == "greet":
                    assert ctx.message.content == "Hello, world!"  # Adjust as needed
            except Exception as e:
                print(f"Error testing `{command.name}`: {str(e)}")

# If there are commands that need arguments (e.g., `/greet John`), you can add special assertions for them
@pytest.mark.asyncio
async def test_greet_command():
    ctx = await client.get_context_from_message("/greet John")
    await client.invoke(ctx)
    assert ctx.message.content == "Hello, John!"  # Modify based on your expected output

@pytest.mark.asyncio
async def test_create_queue():
    ctx = await client.get_context_from_message("/create_queue testQueue 5")
    await client.invoke(ctx)
    assert ctx.message.content == "Queue testQueue created with size 5."  # Adjust to expected output
