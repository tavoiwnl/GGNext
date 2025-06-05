# --- cogs/custom_game_modes.py ---

import discord
from discord.ext import commands
from discord import app_commands, Interaction, Embed

class CustomGameModes(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store

    @app_commands.command(name="create_game_mode", description="Create a new custom game mode")
    @app_commands.describe(name="Name of the game mode", description="Description for the custom mode")
    async def create_game_mode(self, interaction: Interaction, name: str, description: str):
        success = await self.data_store.add_custom_game_mode(name, description)
        if not success:
            await interaction.response.send_message("❌ A game mode with that name already exists.", ephemeral=True)
            return
        await interaction.response.send_message(f"✅ Custom game mode `{name}` created!", ephemeral=True)

    @app_commands.command(name="list_game_modes", description="List all available custom game modes")
    async def list_game_modes(self, interaction: Interaction):
        modes = await self.data_store.get_custom_game_modes()
        if not modes:
            await interaction.response.send_message("No custom game modes found.", ephemeral=True)
            return

        embed = Embed(title="🎮 Custom Game Modes", color=discord.Color.blurple())
        for mode in modes:
            embed.add_field(name=mode['name'], value=mode['description'], inline=False)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="delete_game_mode", description="Delete a custom game mode")
    @app_commands.describe(name="The name of the game mode to delete")
    async def delete_game_mode(self, interaction: Interaction, name: str):
        success = await self.data_store.remove_custom_game_mode(name)
        if not success:
            await interaction.response.send_message("❌ That game mode does not exist.", ephemeral=True)
            return
        await interaction.response.send_message(f"🗑️ Custom game mode `{name}` has been deleted.", ephemeral=True)

# custom_game_modes_module.py
async def setup(bot, data_store):
    await bot.add_cog(CustomGameModes(bot, data_store))


