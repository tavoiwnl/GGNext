# --- cogs/nickname_module.py ---

import discord
from discord.ext import commands
from discord import app_commands, Interaction

class Nickname(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store

    def format_nickname(self, user_id):
        player = self.data_store.players.get(user_id)
        if not player:
            return None
        fmt = player.get("nickname_format", "[#elo] #name")
        name = player.get("name", "Player")
        elo = player.get("elo", 100)
        return fmt.replace("#elo", str(elo)).replace("#name", name)

    async def update_user_nickname(self, user: discord.Member):
        nickname = self.format_nickname(user.id)
        if nickname:
            try:
                await user.edit(nick=nickname)
            except discord.Forbidden:
                pass

    @app_commands.command(name="set_nickname_format", description="Customize how your nickname should look")
    @app_commands.describe(format_string="Use #elo and #name to style your nickname")
    async def set_nickname_format(self, interaction: Interaction, format_string: str):
        user_id = interaction.user.id
        if user_id not in self.data_store.players:
            await interaction.response.send_message("❗ You must register first using `/register`.", ephemeral=True)
            return

        self.data_store.players[user_id]['nickname_format'] = format_string
        await self.update_user_nickname(interaction.user)
        await interaction.response.send_message(f"✅ Your nickname format is now: `{format_string}`", ephemeral=True)

    @app_commands.command(name="refresh_nickname", description="Update your nickname with current stats")
    async def refresh_nickname(self, interaction: Interaction):
        user_id = interaction.user.id
        if user_id not in self.data_store.players:
            await interaction.response.send_message("❗ You must register first using `/register`.", ephemeral=True)
            return

        await self.update_user_nickname(interaction.user)
        await interaction.response.send_message("✅ Your nickname has been refreshed.", ephemeral=True)

    @app_commands.command(name="reset_nickname", description="Reset your nickname to your Discord username")
    async def reset_nickname(self, interaction: Interaction):
        try:
            await interaction.user.edit(nick=None)
            await interaction.response.send_message("🔄 Your nickname has been reset to default.", ephemeral=True)
        except discord.Forbidden:
            await interaction.response.send_message("⚠️ I do not have permission to reset your nickname.", ephemeral=True)

    @commands.Cog.listener()
    async def on_match_end(self, match_data):
        guild = self.bot.get_guild(match_data['guild_id'])
        for player_id in match_data['team_a'] + match_data['team_b']:
            member = guild.get_member(player_id)
            if member:
                await self.update_user_nickname(member)

# nickname_module.py
async def setup(bot, data_store):
    await bot.add_cog(NicknameManager(bot, data_store))

