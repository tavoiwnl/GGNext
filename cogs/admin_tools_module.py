# --- cogs/admin_tools.py ---

import discord
from discord.ext import commands
from discord import app_commands, Interaction, Member, Role
from typing import Optional

class AdminTools(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store

    # Command: Reset Player's MMR
    @app_commands.command(name="reset_mmr", description="Reset the MMR of a player or all players")
    @app_commands.describe(member="Leave blank to reset all players")
    async def reset_mmr(self, interaction: Interaction, member: Optional[Member] = None):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
            return

        if member:
            if member.id in self.data_store.players:
                self.data_store.players[member.id]['elo'] = 100
                await interaction.response.send_message(f"🔁 MMR reset for {member.mention}", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Member not registered.", ephemeral=True)
        else:
            for pid in self.data_store.players:
                self.data_store.players[pid]['elo'] = 100
            await interaction.response.send_message("🔁 MMR reset for all players.", ephemeral=True)

    # Command: Remove Player From Queue
    @app_commands.command(name="dequeue_user", description="Remove a user from all queues")
    @app_commands.describe(member="User to remove")
    async def dequeue_user(self, interaction: Interaction, member: Member):
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message("❌ You lack permission to do this.", ephemeral=True)
            return

        removed = self.data_store.dequeue_user(member.id)
        if removed:
            await interaction.response.send_message(f"✅ {member.mention} removed from all queues.", ephemeral=True)
        else:
            await interaction.response.send_message(f"⚠️ {member.mention} was not in any queue.", ephemeral=True)

    # Command: Set Admin Role for Command Access
    @app_commands.command(name="grant_admin", description="Grant a role permission to use admin commands")
    @app_commands.describe(role="Role to grant access")
    async def grant_admin(self, interaction: Interaction, role: Role):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You need admin permission.", ephemeral=True)
            return

        self.data_store.admin_roles.add(role.id)
        await interaction.response.send_message(f"✅ `{role.name}` can now use admin commands.", ephemeral=True)

    # Command: Revoke Admin Role Access
    @app_commands.command(name="revoke_admin", description="Revoke admin access from a role")
    @app_commands.describe(role="Role to revoke access")
    async def revoke_admin(self, interaction: Interaction, role: Role):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You need admin permission.", ephemeral=True)
            return

        if role.id in self.data_store.admin_roles:
            self.data_store.admin_roles.remove(role.id)
            await interaction.response.send_message(f"🚫 `{role.name}` no longer has admin access.", ephemeral=True)
        else:
            await interaction.response.send_message(f"⚠️ `{role.name}` was not granted admin access.", ephemeral=True)

    # Command: Cancel Ongoing Match
    @app_commands.command(name="cancel_match", description="Cancel an ongoing match by ID")
    @app_commands.describe(match_id="ID of the match to cancel")
    async def cancel_match(self, interaction: Interaction, match_id: int):
        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message("❌ You don't have permission.", ephemeral=True)
            return

        success = await self.data_store.cancel_match(match_id)
        if success:
            await interaction.response.send_message(f"🛑 Match `{match_id}` has been cancelled.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Match not found or already completed.", ephemeral=True)

# admin_tools_module.py
async def setup(bot, extras):
    data_store = extras["data_store"]
    await bot.add_cog(AdminTools(bot, data_store))

