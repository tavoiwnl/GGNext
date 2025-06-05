# cogs/voice_text_management.py

import discord
from discord.ext import commands
from discord import app_commands, Interaction
from typing import Optional

class VoiceTextManagement(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store

    @app_commands.command(name="voice_create_vc", description="Toggle voice channel creation for match lobbies")
    @app_commands.describe(enabled="Enable or disable automatic VC creation")
    async def voice_create_vc(self, interaction: Interaction, enabled: bool):
        guild_id = interaction.guild.id
        self.data_store.guild_settings[guild_id]['voice_create'] = enabled
        status = "enabled" if enabled else "disabled"
        await interaction.response.send_message(f"🔊 Voice channel creation has been **{status}**.", ephemeral=True)

    @app_commands.command(name="voice_set", description="Set the category or template for automatic VC")
    @app_commands.describe(category="Voice category to use for team channels")
    async def voice_set(self, interaction: Interaction, category: discord.CategoryChannel):
        guild_id = interaction.guild.id
        self.data_store.guild_settings[guild_id]['voice_category'] = category.id
        await interaction.response.send_message(f"📁 Voice channels will be created under **{category.name}**.", ephemeral=True)

    @app_commands.command(name="defaults_mute_spectators", description="Toggle muting spectators in VC")
    @app_commands.describe(mute="Mute spectators when joining team VCs")
    async def defaults_mute_spectators(self, interaction: Interaction, mute: bool):
        guild_id = interaction.guild.id
        self.data_store.guild_settings[guild_id]['mute_spectators'] = mute
        status = "muted" if mute else "unmuted"
        await interaction.response.send_message(f"👥 Spectators will be **{status}** in voice channels.", ephemeral=True)

    @app_commands.command(name="defaults_allow_spectators", description="Allow or disallow spectators in lobbies")
    @app_commands.describe(allow="Whether spectators can join voice lobbies")
    async def defaults_allow_spectators(self, interaction: Interaction, allow: bool):
        guild_id = interaction.guild.id
        self.data_store.guild_settings[guild_id]['allow_spectators'] = allow
        status = "allowed" if allow else "disallowed"
        await interaction.response.send_message(f"👤 Spectators are now **{status}** in lobbies.", ephemeral=True)

    @app_commands.command(name="defaults_show_lobby", description="Toggle game lobby visibility for users")
    @app_commands.describe(visible="Should lobbies be visible to players")
    async def defaults_show_lobby(self, interaction: Interaction, visible: bool):
        guild_id = interaction.guild.id
        self.data_store.guild_settings[guild_id]['show_lobby'] = visible
        status = "visible" if visible else "hidden"
        await interaction.response.send_message(f"📣 Match lobbies are now **{status}**.", ephemeral=True)

    @app_commands.command(name="defaults_send_ready_up_dm", description="Toggle DMing players when a match is ready")
    @app_commands.describe(enabled="Whether players get DMs on match found")
    async def defaults_send_ready_up_dm(self, interaction: Interaction, enabled: bool):
        guild_id = interaction.guild.id
        self.data_store.guild_settings[guild_id]['send_ready_up_dm'] = enabled
        status = "enabled" if enabled else "disabled"
        await interaction.response.send_message(f"📬 Ready-up DMs have been **{status}**.", ephemeral=True)

# voice_text_management_module.py
async def setup(bot, data_store):
    await bot.add_cog(VoiceTextManagement(bot, data_store))

