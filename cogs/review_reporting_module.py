# === cogs/review_reporting.py ===

from discord.ext import commands
from discord import app_commands, Interaction, Embed
import discord
import time

class ReviewReporting(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store

    @app_commands.command(name="report_match", description="Report an issue with a match")
    @app_commands.describe(match_id="ID of the match", reason="Reason for the report")
    async def report_match(self, interaction: Interaction, match_id: str, reason: str):
        match = await self.data_store.get_match(match_id)
        if not match:
            await interaction.response.send_message("❌ Match not found.", ephemeral=True)
            return
        report_data = {
            "match_id": match_id,
            "reporter_id": interaction.user.id,
            "reason": reason,
            "timestamp": int(time.time())
        }
        await self.data_store.log_report(report_data)
        await interaction.response.send_message("✅ Your report has been submitted. Admins will review it.", ephemeral=True)

    @app_commands.command(name="view_reports", description="View recent reports (Admins only)")
    async def view_reports(self, interaction: Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You lack permission to view reports.", ephemeral=True)
            return
        reports = await self.data_store.get_reports()
        if not reports:
            await interaction.response.send_message("No reports found.", ephemeral=True)
            return

        embed = Embed(title="Recent Match Reports", color=discord.Color.orange())
        for report in reports[:10]:
            reporter = self.bot.get_user(report["reporter_id"])
            embed.add_field(
                name=f"Match {report['match_id']}",
                value=f"Reported by {reporter.display_name if reporter else 'Unknown'}: {report['reason']}",
                inline=False
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)

# review_reporting_module.py
async def setup(bot, extras):
    data_store = extras["data_store"]
    await bot.add_cog(ReviewReporting(bot, data_store))
