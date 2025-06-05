# --- cogs/seasonal_leaderboards.py ---

import discord
from discord.ext import commands
from discord import app_commands, Interaction, Embed
from datetime import datetime

class SeasonalLeaderboards(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store

    @app_commands.command(name="season_stats", description="View the current season's stats for a player")
    @app_commands.describe(user="User to check stats for")
    async def season_stats(self, interaction: Interaction, user: discord.User = None):
        user = user or interaction.user
        stats = await self.data_store.get_season_stats(user.id)

        if not stats:
            await interaction.response.send_message("❌ No season stats found.", ephemeral=True)
            return

        embed = Embed(title=f"📆 Season Stats for {user.display_name}", color=discord.Color.purple())
        embed.add_field(name="ELO", value=str(stats.get("elo", 0)), inline=True)
        embed.add_field(name="Wins", value=str(stats.get("wins", 0)), inline=True)
        embed.add_field(name="Losses", value=str(stats.get("losses", 0)), inline=True)
        embed.add_field(name="MVPs", value=str(stats.get("mvps", 0)), inline=True)
        embed.add_field(name="Win Rate", value=f"{stats.get('win_rate', 0.0):.2f}%", inline=True)
        embed.add_field(name="Games Played", value=str(stats.get("games_played", 0)), inline=True)
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="season_leaderboard", description="Show the top players for the current season")
    @app_commands.describe(limit="Number of top players to display")
    async def season_leaderboard(self, interaction: Interaction, limit: int = 10):
        leaderboard = await self.data_store.get_leaderboard(season_only=True, limit=limit)

        if not leaderboard:
            await interaction.response.send_message("❌ No leaderboard data for this season.", ephemeral=True)
            return

        embed = Embed(title=f"🏆 Season Leaderboard (Top {limit})", color=discord.Color.gold())
        for i, entry in enumerate(leaderboard, start=1):
            embed.add_field(
                name=f"#{i} {entry['name']}",
                value=f"ELO: {entry['elo']} | Wins: {entry['wins']} | MVPs: {entry.get('mvps', 0)}",
                inline=False
            )
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="queue_analytics", description="View performance data for queues")
    async def queue_analytics(self, interaction: Interaction):
        analytics = await self.data_store.get_queue_analytics()

        if not analytics:
            await interaction.response.send_message("❌ No queue analytics available.", ephemeral=True)
            return

        embed = Embed(title="📈 Queue Analytics", color=discord.Color.blurple())
        for queue, data in analytics.items():
            embed.add_field(
                name=f"Queue: {queue}",
                value=(
                    f"Games Played: {data['games_played']}\n"
                    f"Avg Match Time: {data['avg_time']} mins\n"
                    f"Most Played Map: {data['top_map']}"
                ),
                inline=False
            )
        await interaction.response.send_message(embed=embed)

# season_leaderboard_module.py
async def setup(bot, extras):
    data_store = extras["data_store"]
    await bot.add_cog(SeasonLeaderboard(bot, data_store))
