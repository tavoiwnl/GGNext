# --- map_management_module.py ---

import discord
from discord.ext import commands
from discord import app_commands, Interaction, Embed
from typing import List

class MapManagement(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store

    @app_commands.command(name="add_map", description="Add a new map to the pool (Admin only)")
    @app_commands.describe(name="Map name", description="Brief description of the map")
    async def add_map(self, interaction: Interaction, name: str, description: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You need admin permissions to add a map.", ephemeral=True)
            return

        await self.data_store.add_map(name, description)
        await interaction.response.send_message(f"✅ Map **{name}** has been added to the pool.", ephemeral=True)

    @app_commands.command(name="remove_map", description="Remove a map from the pool (Admin only)")
    @app_commands.describe(name="Name of the map to remove")
    async def remove_map(self, interaction: Interaction, name: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You need admin permissions to remove a map.", ephemeral=True)
            return

        success = await self.data_store.remove_map(name)
        if success:
            await interaction.response.send_message(f"🗑️ Map **{name}** has been removed.", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ Map **{name}** not found in the pool.", ephemeral=True)

    @app_commands.command(name="map_pool", description="View the current map pool")
    async def map_pool(self, interaction: Interaction):
        maps = await self.data_store.get_map_pool()

        if not maps:
            await interaction.response.send_message("🗺️ No maps currently in the pool.", ephemeral=True)
            return

        embed = Embed(title="🗺️ Current Map Pool", color=discord.Color.blue())
        for map_data in maps:
            embed.add_field(name=map_data["name"], value=map_data["description"], inline=False)

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="random_map", description="Get a random map from the pool")
    async def random_map(self, interaction: Interaction):
        map_data = await self.data_store.get_random_map()
        if not map_data:
            await interaction.response.send_message("❌ No maps available in the pool.", ephemeral=True)
            return

        embed = Embed(
            title=f"🎲 Random Map Selected",
            description=f"**{map_data['name']}**\n{map_data['description']}",
            color=discord.Color.random()
        )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="map_vote", description="Vote for your favorite maps (Max 3)")
    @app_commands.describe(choices="Comma-separated list of maps to vote for")
    async def map_vote(self, interaction: Interaction, choices: str):
        map_names = [name.strip() for name in choices.split(",") if name.strip()]
        if len(map_names) > 3:
            await interaction.response.send_message("❗ You can only vote for **up to 3 maps**.", ephemeral=True)
            return

        existing_maps = await self.data_store.get_map_names()
        invalid = [m for m in map_names if m not in existing_maps]

        if invalid:
            await interaction.response.send_message(f"❌ These maps are not in the pool: {', '.join(invalid)}", ephemeral=True)
            return

        await self.data_store.record_map_votes(interaction.user.id, map_names)
        await interaction.response.send_message("✅ Your votes have been submitted!", ephemeral=True)

    @app_commands.command(name="map_votes", description="See current map vote leaderboard")
    async def map_votes(self, interaction: Interaction):
        leaderboard = await self.data_store.get_map_vote_leaderboard()
        if not leaderboard:
            await interaction.response.send_message("📭 No votes have been cast yet.", ephemeral=True)
            return

        embed = Embed(title="📊 Map Vote Leaderboard", color=discord.Color.gold())
        for entry in leaderboard:
            embed.add_field(name=entry["name"], value=f"Votes: {entry['votes']}", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot, data_store):
    await bot.add_cog(MapManagement(bot, data_store))

