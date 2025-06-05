# --- utils.py ---

import discord
from discord.ext import commands
from discord import app_commands, Interaction
from typing import Optional

# Utility functions for visual enhancements and data formatting
def elo_tier_color(elo: int) -> discord.Color:
    if elo >= 900: return discord.Color.gold()
    elif elo >= 700: return discord.Color.orange()
    elif elo >= 500: return discord.Color.blue()
    elif elo >= 300: return discord.Color.green()
    else: return discord.Color.greyple()

def rank_emoji(elo: int) -> str:
    if elo >= 900: return "🏅"
    elif elo >= 700: return "🎖️"
    elif elo >= 500: return "🎯"
    elif elo >= 300: return "⭐"
    else: return "⚪"

def format_name(name: str, elo: int, template: Optional[str] = None) -> str:
    if not template:
        template = "[#elo] #name"
    return template.replace("#elo", str(elo)).replace("#name", name)

def can_access_admin(interaction: Interaction) -> bool:
    return interaction.user.guild_permissions.administrator

def can_access_mod(interaction: Interaction, mod_role_id: Optional[int] = None) -> bool:
    if interaction.user.guild_permissions.administrator:
        return True
    if mod_role_id:
        return any(role.id == mod_role_id for role in interaction.user.roles)
    return False

class UtilCommands(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store

    @app_commands.command(name="check_permissions", description="See your InHouseQueue bot access levels")
    async def check_permissions(self, interaction: Interaction):
        is_admin = interaction.user.guild_permissions.administrator
        mod_role_id = self.data_store.config.get("mod_role_id")
        is_mod = can_access_mod(interaction, mod_role_id)

        embed = discord.Embed(title="🔐 Permission Check", color=discord.Color.blurple())
        embed.add_field(name="Admin", value="✅" if is_admin else "❌", inline=True)
        embed.add_field(name="Moderator", value="✅" if is_mod else "❌", inline=True)
        embed.set_footer(text="Use this to verify your access.")
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot, data_store):
    await bot.add_cog(UtilCommands(bot, data_store))
