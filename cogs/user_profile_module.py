# --- user_profile_module.py ---

import discord
from discord.ext import commands
from discord import app_commands, Interaction, Embed
from utils.visuals import generate_profile_card_image

class UserProfile(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store

    @app_commands.command(name="profile", description="View your profile card")
    async def profile(self, interaction: Interaction):
        user_id = interaction.user.id
        stats = await self.data_store.get_player_stats(user_id)
        if not stats:
            await interaction.response.send_message("❗ You are not registered.", ephemeral=True)
            return

        image = await generate_profile_card_image(interaction.user, stats)
        await interaction.response.send_message(file=image)

    @app_commands.command(name="profile_customize", description="Customize your profile banner or card style")
    @app_commands.describe(style="Choose a display style", banner_url="Optional banner image URL")
    async def profile_customize(self, interaction: Interaction, style: str, banner_url: str = None):
        await self.data_store.set_profile_customization(interaction.user.id, style, banner_url)
        await interaction.response.send_message("✅ Your profile settings have been updated!", ephemeral=True)

    @app_commands.command(name="profile_settings", description="View your current profile customization settings")
    async def profile_settings(self, interaction: Interaction):
        settings = await self.data_store.get_profile_customization(interaction.user.id)
        if not settings:
            await interaction.response.send_message("No customization settings found.", ephemeral=True)
            return

        embed = Embed(title="🎨 Profile Settings", color=discord.Color.blurple())
        embed.add_field(name="Style", value=settings.get("style", "Default"), inline=True)
        embed.add_field(name="Banner URL", value=settings.get("banner_url", "None"), inline=True)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot, data_store):
    await bot.add_cog(UserProfile(bot, data_store))
