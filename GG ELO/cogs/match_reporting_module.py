# --- cogs/match_reporting.py ---

import discord
from discord.ext import commands
from discord import app_commands, Interaction, File, Embed, ui
from datetime import datetime
import time
from typing import Optional

class MatchReporting(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store
        self.match_id_counter = 1

    class ScreenshotModal(ui.Modal, title="📸 Submit Match Screenshot"):
        def __init__(self, callback):
            super().__init__()
            self.callback_func = callback
            self.notes = ui.TextInput(label="Match Notes (Optional)", style=discord.TextStyle.paragraph, required=False)
            self.add_item(self.notes)

        async def on_submit(self, interaction: Interaction):
            await self.callback_func(interaction, self.notes.value)

    @app_commands.command(name="report_match", description="Submit your match screenshot to finalize the match")
    @app_commands.describe(match_id="Match ID", screenshot="Screenshot of the results", mvp="Player voted MVP")
    async def report_match(
        self,
        interaction: Interaction,
        match_id: int,
        screenshot: discord.Attachment,
        mvp: Optional[discord.Member] = None
    ):
        if not screenshot:
            await interaction.response.send_message("❗ You must attach a screenshot.", ephemeral=True)
            return

        match = await self.data_store.get_match(match_id)
        if not match:
            await interaction.response.send_message("❌ Match not found.", ephemeral=True)
            return

        async def after_modal_submit(modal_interaction, notes):
            match['screenshot_url'] = screenshot.url
            match['notes'] = notes
            match['mvp'] = mvp.id if mvp else None
            match['reported_by'] = interaction.user.id
            match['reported_at'] = int(time.time())
            match['finalized'] = True

            await self.data_store.save_match(match_id, match)

            embed = Embed(title=f"📄 Match #{match_id} Finalized", color=discord.Color.green())
            embed.add_field(name="Submitted By", value=interaction.user.mention, inline=True)
            embed.add_field(name="MVP", value=mvp.mention if mvp else "Not selected", inline=True)
            if notes:
                embed.add_field(name="Notes", value=notes, inline=False)
            embed.set_image(url=screenshot.url)
            embed.timestamp = datetime.utcnow()

            await modal_interaction.response.send_message(embed=embed)

        await interaction.response.send_modal(self.ScreenshotModal(after_modal_submit))

    @app_commands.command(name="review_match", description="Admins: Review a submitted match")
    @app_commands.describe(match_id="Match ID to review")
    async def review_match(self, interaction: Interaction, match_id: int):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You do not have permission to review matches.", ephemeral=True)
            return

        match = await self.data_store.get_match(match_id)
        if not match:
            await interaction.response.send_message("❌ Match not found.", ephemeral=True)
            return

        embed = Embed(title=f"🧐 Review Match #{match_id}", color=discord.Color.orange())
        embed.add_field(name="Submitted By", value=f"<@{match.get('reported_by', 'Unknown')}>", inline=True)
        embed.add_field(name="MVP", value=f"<@{match.get('mvp')}>", inline=True)
        embed.add_field(name="Notes", value=match.get("notes", "None provided"), inline=False)
        embed.set_image(url=match.get("screenshot_url"))
        embed.timestamp = datetime.utcfromtimestamp(match.get("reported_at", int(time.time())))

        await interaction.response.send_message(embed=embed)

async def setup(bot, data_store):
    await bot.add_cog(MatchReporting(bot, data_store))
