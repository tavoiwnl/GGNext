# --- cogs/language_localization_module.py ---

from discord.ext import commands
from discord import app_commands, Interaction
import discord

class LanguageLocalization(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store

    supported_languages = {
        "en": "English",
        "es": "Spanish",
        "fr": "French",
        "de": "German",
        "zh": "Chinese",
        "jp": "Japanese",
    }

    @app_commands.command(name="language", description="Change your preferred language")
    @app_commands.describe(code="Language code (e.g., en, es, fr)")
    async def language(self, interaction: Interaction, code: str):
        code = code.lower()
        if code not in self.supported_languages:
            await interaction.response.send_message(
                f"❌ Unsupported language. Available: {', '.join(self.supported_languages.keys())}", ephemeral=True
            )
            return

        user_id = interaction.user.id
        await self.data_store.set_user_language(user_id, code)
        await interaction.response.send_message(
            f"🌍 Language updated to **{self.supported_languages[code]}**.", ephemeral=True
        )

    @app_commands.command(name="server_language", description="Set the server default language (Admin only)")
    @app_commands.describe(code="Language code (e.g., en, es, fr)")
    async def server_language(self, interaction: Interaction, code: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ Admin permission required.", ephemeral=True)
            return

        code = code.lower()
        if code not in self.supported_languages:
            await interaction.response.send_message(
                f"❌ Unsupported language. Available: {', '.join(self.supported_languages.keys())}", ephemeral=True
            )
            return

        guild_id = interaction.guild.id
        await self.data_store.set_server_language(guild_id, code)
        await interaction.response.send_message(
            f"✅ Server default language set to **{self.supported_languages[code]}**."
        )

    @app_commands.command(name="available_languages", description="List all supported languages")
    async def available_languages(self, interaction: Interaction):
        formatted = "\n".join([f"`{code}` - {lang}" for code, lang in self.supported_languages.items()])
        await interaction.response.send_message(f"🌐 Supported Languages:\n{formatted}", ephemeral=True)


# language_localization_module.py
async def setup(bot, extras):
    data_store = extras["data_store"]
    await bot.add_cog(LanguageLocalization(bot, data_store))

