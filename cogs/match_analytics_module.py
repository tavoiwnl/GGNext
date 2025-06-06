# --- cogs/match_analytics.py ---

import discord
from discord.ext import commands
from discord import app_commands, Interaction, Embed
from cogs.data_store_module import DataStore
from datetime import datetime, timedelta

class MatchAnalytics(commands.Cog):
    def __init__(self, bot: commands.Bot, data_store: DataStore):
        self.bot = bot
        self.data_store = data_store

    @app_commands.describe(user="User to check match history for", limit="Number of recent matches to show")
    async def match_history(self, interaction: Interaction, user: discord.User = None, limit: int = 5):
        user = user or interaction.user
        matches = await self.data_store.get_recent_matches(user.id, limit)

        if not matches:
            await interaction.response.send_message(f"❌ No recent matches found for {user.display_name}.", ephemeral=True)
            return

        embed = Embed(title=f"📜 Match History - {user.display_name}", color=discord.Color.dark_teal())
        for match in matches:
            result = "Win" if match['winner'] == user.id else "Loss"
            mvp = " 🌟 MVP" if match.get('mvp') == user.id else ""
            embed.add_field(
                name=f"Match #{match['id']}",
                value=f"Result: **{result}**{mvp}\nELO: {match['elo_after']}\nDate: <t:{int(match['timestamp'].timestamp())}:R>",
                inline=False
            )

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="game_summary", description="View a summary of a specific match")
    @app_commands.describe(match_id="The match ID to view")
    async def game_summary(self, interaction: Interaction, match_id: int):
        match = await self.data_store.get_match(match_id)
        if not match:
            await interaction.response.send_message("❌ Match not found.", ephemeral=True)
            return

        embed = Embed(title=f"📘 Match Summary #{match_id}", color=discord.Color.blurple())
        embed.add_field(name="Winner", value=f"<@{match['winner']}>", inline=True)
        embed.add_field(name="Loser", value=f"<@{match['loser']}>", inline=True)
        if match.get("mvp"):
            embed.add_field(name="MVP", value=f"<@{match['mvp']}>", inline=True)
        embed.add_field(name="Date", value=f"<t:{int(match['timestamp'].timestamp())}:F>", inline=False)
        if match.get("notes"):
            embed.add_field(name="Notes", value=match['notes'], inline=False)
        if match.get("screenshot_url"):
            embed.set_image(url=match['screenshot_url'])

        await interaction.response.send_message(embed=embed)

# match_analytics_module.py
async def setup(bot, data_store):
    await bot.add_cog(MatchAnalytics(bot, data_store))

