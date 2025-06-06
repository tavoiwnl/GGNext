# --- match_history_module.py ---

import discord
from discord.ext import commands
from discord import app_commands, Interaction, Embed
from typing import Optional
from cogs.data_store_module import DataStore


class MatchHistory(commands.Cog):
    def __init__(self, bot, data_store: DataStore):
        self.bot = bot
        self.data_store = data_store

    @app_commands.command(name="match_history", description="View your recent match history")
    @app_commands.describe(user="User to view history for", limit="How many matches to view (max 10)")
    async def match_history(self, interaction: Interaction, user: Optional[discord.Member] = None, limit: int = 5):
        user = user or interaction.user
        matches = await self.data_store.get_user_match_history(user.id, limit=limit)

        if not matches:
            await interaction.response.send_message(f"❌ No match history found for {user.mention}.", ephemeral=True)
            return

        embed = Embed(
            title=f"🗂 Match History for {user.display_name}",
            description=f"Showing last {len(matches)} matches",
            color=discord.Color.blue()
        )

        for match in matches:
            result = "🏆 Win" if match["result"] == "win" else "❌ Loss"
            mvp = "🌟 MVP" if match.get("mvp") == user.id else ""
            timestamp = f"<t:{int(match['timestamp'])}:R>" if match.get("timestamp") else "Unknown"
            elo_change = f"{match.get('elo_change', 0)}"

            embed.add_field(
                name=f"Match #{match['id']} | {result} {mvp}",
                value=(
                    f"**Opponent:** <@{match['opponent']}>\n"
                    f"**ELO Change:** `{elo_change}`\n"
                    f"**Played:** {timestamp}"
                ),
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="match_detail", description="View full detail of a match by ID")
    @app_commands.describe(match_id="The match ID to view")
    async def match_detail(self, interaction: Interaction, match_id: int):
        match = await self.data_store.get_match(match_id)

        if not match:
            await interaction.response.send_message("❌ Match not found.", ephemeral=True)
            return

        winner = self.bot.get_user(match.get("winner"))
        loser = self.bot.get_user(match.get("loser"))
        mvp = self.bot.get_user(match.get("mvp")) if match.get("mvp") else None
        notes = match.get("notes", "None")
        screenshot = match.get("screenshot_url")

        embed = Embed(
            title=f"📄 Match #{match_id} Details",
            color=discord.Color.orange()
        )

        embed.add_field(name="Winner", value=winner.mention if winner else "Unknown", inline=True)
        embed.add_field(name="Loser", value=loser.mention if loser else "Unknown", inline=True)
        embed.add_field(name="MVP", value=mvp.mention if mvp else "None", inline=True)
        embed.add_field(name="Notes", value=notes, inline=False)

        if screenshot:
            embed.set_image(url=screenshot)

        embed.set_footer(text="Match result history")

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot, data_store):
    await bot.add_cog(MatchHistory(bot, data_store))
