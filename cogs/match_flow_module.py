# --- cogs/match_flow.py ---

import discord
from discord.ext import commands
from discord import app_commands, Interaction, Embed
from typing import Dict
from datetime import datetime, timedelta
import asyncio

class MatchFlowController(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store
        self.tempbans = {}  # user_id -> expiry datetime

    async def handle_match_start(self, queue_data):
        match_id = self.data_store.generate_match_id()
        queue_data['match_id'] = match_id

        players = queue_data['players']
        guild = self.bot.get_guild(queue_data['guild_id'])
        category = discord.utils.get(guild.categories, name="Matches")

        overwrites = {guild.default_role: discord.PermissionOverwrite(read_messages=False)}
        for user_id in players:
            member = guild.get_member(user_id)
            overwrites[member] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)

        text_channel = await guild.create_text_channel(f"match-{match_id}", category=category, overwrites=overwrites)
        voice_channel = await guild.create_voice_channel(f"Match VC {match_id}", category=category, overwrites=overwrites)

        match_data = {
            "id": match_id,
            "guild_id": guild.id,
            "queue": queue_data['queue_name'],
            "players": players,
            "team_a": [],
            "team_b": [],
            "text_channel_id": text_channel.id,
            "voice_channel_id": voice_channel.id,
            "start_time": discord.utils.utcnow(),
        }

        self.data_store.matches[match_id] = match_data

        await text_channel.send(embed=Embed(title="📸 Screenshot Required", description="Please post your screenshot of the match results here.", color=discord.Color.orange()))
        await text_channel.send(embed=Embed(title="🏅 MVP Voting", description="Vote for the MVP of the match!", color=discord.Color.gold()))
        await text_channel.send(embed=Embed(title="🔄 Rematch?", description="React below to vote for a rematch.", color=discord.Color.blurple()))

        return match_data

    async def cleanup_match(self, match_id):
        match = self.data_store.matches.get(match_id)
        if not match:
            return

        guild = self.bot.get_guild(match['guild_id'])
        text_channel = guild.get_channel(match['text_channel_id'])
        voice_channel = guild.get_channel(match['voice_channel_id'])

        if text_channel:
            await text_channel.delete()
        if voice_channel:
            await voice_channel.delete()

        self.data_store.matches.pop(match_id, None)

    async def tempban_user(self, user_id, duration_minutes=30):
        expiry = datetime.utcnow() + timedelta(minutes=duration_minutes)
        self.tempbans[user_id] = expiry

    def is_user_tempbanned(self, user_id):
        now = datetime.utcnow()
        if user_id in self.tempbans and self.tempbans[user_id] > now:
            return True
        if user_id in self.tempbans and self.tempbans[user_id] <= now:
            del self.tempbans[user_id]
        return False

    @app_commands.command(name="match_cancel", description="Cancel an ongoing match (Admin only)")
    async def match_cancel(self, interaction: Interaction, match_id: int):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You lack permission to cancel matches.", ephemeral=True)
            return

        if match_id not in self.data_store.matches:
            await interaction.response.send_message("❌ Match ID not found.", ephemeral=True)
            return

        await self.cleanup_match(match_id)
        await interaction.response.send_message(f"🚫 Match {match_id} has been cancelled and cleaned up.", ephemeral=True)

    @app_commands.command(name="leave_during_draft", description="Admin: Simulate a user leaving captain draft (for penalty test)")
    @app_commands.describe(user="The user who left")
    async def leave_during_draft(self, interaction: Interaction, user: discord.Member):
        await self.tempban_user(user.id, 30)
        await interaction.response.send_message(f"⏳ {user.display_name} has been temporarily banned from queueing for 30 minutes.", ephemeral=True)

async def setup(bot, extras):
    data_store = extras["data_store"]
    await bot.add_cog(YourCogClass(bot, data_store))

