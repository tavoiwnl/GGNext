# --- cogs/user_management.py ---

import discord
from discord.ext import commands
from discord import app_commands, Interaction, Member

class UserManagement(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store

    # --- User: Set Their Own IGN ---
    @app_commands.command(name="set_ign", description="Set your In-Game Name (IGN)")
    @app_commands.describe(ign="Your in-game name")
    async def set_ign(self, interaction: Interaction, ign: str):
        await self.data_store.set_ign(interaction.user.id, ign)
        try:
            await interaction.user.edit(nick=ign)
        except discord.Forbidden:
            pass  # Bot lacks permission to change nickname
        await interaction.response.send_message(f"✅ Your IGN has been set to `{ign}`.", ephemeral=True)

    # --- View Another User's IGN ---
    @app_commands.command(name="get_ign", description="Check a user's In-Game Name")
    @app_commands.describe(user="User to check")
    async def get_ign(self, interaction: Interaction, user: Member):
        ign = await self.data_store.get_ign(user.id)
        if not ign:
            await interaction.response.send_message(f"❌ {user.display_name} has not set an IGN.", ephemeral=True)
        else:
            await interaction.response.send_message(f"🧾 {user.display_name}'s IGN is `{ign}`.", ephemeral=True)

    # --- Admin: Force Set IGN for Someone ---
    @app_commands.command(name="force_set_ign", description="Admin only: Set a user's IGN manually")
    @app_commands.describe(member="User to set IGN for", ign="New IGN to assign")
    async def force_set_ign(self, interaction: Interaction, member: Member, ign: str):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You need admin permissions to use this command.", ephemeral=True)
            return

        await self.data_store.set_ign(member.id, ign)
        try:
            await member.edit(nick=ign)
        except discord.Forbidden:
            pass
        await interaction.response.send_message(f"✅ IGN for {member.display_name} has been set to `{ign}`.", ephemeral=True)

async def setup(bot, data_store):
    await bot.add_cog(UserManagement(bot, data_store))

