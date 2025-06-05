# --- cogs/season_management_module.py ---

import discord
from discord.ext import commands
from discord import app_commands, Interaction, Embed

class SeasonManagement(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store

    @app_commands.command(name="season_start", description="Start a new competitive season")
    @app_commands.describe(season="Season number to start")
    async def season_start(self, interaction: Interaction, season: int):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ This command is restricted to admins.", ephemeral=True)
            return
        await self.data_store.start_season(season)
        await interaction.response.send_message(f"✅ Season `{season}` has been successfully started.")

    @app_commands.command(name="season_end", description="End an ongoing competitive season")
    @app_commands.describe(season="Season number to end")
    async def season_end(self, interaction: Interaction, season: int):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ This command is restricted to admins.", ephemeral=True)
            return
        await self.data_store.end_season(season)
        await interaction.response.send_message(f"📅 Season `{season}` has been marked as ended.")

    @app_commands.command(name="season_info", description="Get detailed info about a season")
    @app_commands.describe(season="Season number")
    async def season_info(self, interaction: Interaction, season: int):
        info = await self.data_store.get_season_info(season)
        if not info:
            await interaction.response.send_message("❌ No data found for that season.", ephemeral=True)
            return

        embed = Embed(
            title=f"🏆 Season {season} Information",
            color=discord.Color.purple()
        )
        embed.add_field(name="Start Date", value=info.get("start_date", "❓ Unknown"), inline=True)
        embed.add_field(name="End Date", value=info.get("end_date", "🟢 Ongoing"), inline=True)
        embed.add_field(name="Status", value=info.get("status", "N/A"), inline=True)

        await interaction.response.send_message(embed=embed)

async def setup(bot, data_store):
    await bot.add_cog(SeasonManagement(bot, data_store))
