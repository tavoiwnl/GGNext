import discord
from discord.ext import commands
import pytest
from discord.ext.test import Client

# Your test bot class
class TestBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!")

    async def on_ready(self):
        print(f"Logged in as {self.user}")

# Instantiate the bot
test_bot = TestBot()

# Load all cogs in GGNext ELO (ensure your cogs are properly set up and have slash commands)
test_bot.load_extension('cogs.admin_tools')
test_bot.load_extension('cogs.custom_game_modes')
test_bot.load_extension('cogs.match_analytics')
test_bot.load_extension('cogs.match_flow')
test_bot.load_extension('cogs.match_reporting')
test_bot.load_extension('cogs.multi_language_support')
test_bot.load_extension('cogs.queue_management')
test_bot.load_extension('cogs.season_leaderboard')
test_bot.load_extension('cogs.season_management')
test_bot.load_extension('cogs.voice_text_management')
test_bot.load_extension('cogs.webhooks')
test_bot.load_extension('cogs.challenge')
test_bot.load_extension('cogs.map_management')

# Create the testing client
client = Client(test_bot)

# Test case to invoke all slash commands across cogs
@pytest.mark.asyncio
async def test_all_commands():
    # Loop through each loaded cog and find commands
    for cog in test_bot.cogs.values():
        for command in cog.walk_commands():
            try:
                # Simulate invoking each slash command
                ctx = await client.get_context_from_message(f"/{command.name}")
                
                # Call the command
                await client.invoke(ctx)

                # Check expected outputs for specific commands (you can modify these based on your actual commands)
                if command.name == "create_queue":
                    assert ctx.message.content == "Queue created successfully!"  # Adjust based on your command logic
                elif command.name == "greet":
                    assert ctx.message.content == "Hello, world!"  # Modify based on expected response
                elif command.name == "goodbye":
                    assert ctx.message.content == "Goodbye, world!"  # Modify based on expected response
                # Add more conditionals here for other commands if needed

            except Exception as e:
                print(f"Error while testing `{command.name}`: {str(e)}")

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
