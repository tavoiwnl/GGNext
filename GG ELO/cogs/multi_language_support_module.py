# --- cogs/multi_language_support.py ---

import discord
from discord.ext import commands
from discord import app_commands, Interaction
from utils.data_manager import DataManager

# Sample language packs
LANGUAGE_PACKS = {
    "en": {
        "register_success": "✅ Welcome {name}, you are now registered! Your starting ELO is {elo}.",
        "command_not_found": "❌ Command not found.",
        "language_set": "🌐 Your language has been set to English.",
    },
    "es": {
        "register_success": "✅ Bienvenido {name}, ahora estás registrado! Tu ELO inicial es {elo}.",
        "command_not_found": "❌ Comando no encontrado.",
        "language_set": "🌐 Tu idioma ha sido cambiado a Español.",
    },
    # Additional languages can be added here
}

class MultiLanguageSupport(commands.Cog):
    def __init__(self, bot: commands.Bot, data_store: DataManager):
        self.bot = bot
        self.data_store = data_store

    def get_language(self, user_id):
        return self.data_store.user_languages.get(user_id, "en")

    def t(self, user_id, key, **kwargs):
        lang = self.get_language(user_id)
        return LANGUAGE_PACKS.get(lang, LANGUAGE_PACKS["en"]).get(key, key).format(**kwargs)

    @app_commands.command(name="set_language", description="Set your preferred language")
    @app_commands.describe(language="The language code (e.g. en, es)")
    async def set_language(self, interaction: Interaction, language: str):
        if language not in LANGUAGE_PACKS:
            await interaction.response.send_message("❌ Language not supported.", ephemeral=True)
            return

        self.data_store.user_languages[interaction.user.id] = language
        await interaction.response.send_message(LANGUAGE_PACKS[language]["language_set"], ephemeral=True)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            user_id = ctx.author.id if hasattr(ctx, 'author') else 0
            await ctx.send(self.t(user_id, "command_not_found"))

async def setup(bot: commands.Bot, data_store: DataManager):
    await bot.add_cog(MultiLanguageSupport(bot, data_store))
