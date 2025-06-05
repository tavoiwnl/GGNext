# --- cogs/moderation_module.py ---

import discord
from discord.ext import commands
from discord import app_commands, Interaction

class ModerationModule(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store

    @app_commands.command(name="reset_scores", description="Admin: Reset a player's or everyone's scores")
    @app_commands.describe(user="User to reset. Leave blank to reset all.")
    async def reset_scores(self, interaction: Interaction, user: discord.Member = None):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You do not have permission.", ephemeral=True)
            return

        if user:
            self.data_store.players[user.id] = {
                "name": user.name,
                "elo": 100,
                "nickname_format": "[#elo] #name",
                "wins": 0,
                "losses": 0,
                "creator_code": False,
                "priority_pick": False,
                "mvps": 0,
                "streak": 0
            }
            await interaction.response.send_message(f"🔄 Stats reset for {user.display_name}", ephemeral=True)
        else:
            self.data_store.players.clear()
            await interaction.response.send_message("🔄 All players have been reset.", ephemeral=True)

    @app_commands.describe(match_id="ID of the match to cancel")
    async def cancel_match(self, interaction: Interaction, match_id: int):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You need admin permissions.", ephemeral=True)
            return

        match = self.data_store.matches.get(match_id)
        if not match:
            await interaction.response.send_message("❌ Match not found.", ephemeral=True)
            return

        del self.data_store.matches[match_id]
        await interaction.response.send_message(f"🚫 Match {match_id} has been cancelled.", ephemeral=True)

    @app_commands.command(name="set_mmr", description="Set a user's MMR")
    @app_commands.describe(user="The user", amount="MMR to set")
    async def set_mmr(self, interaction: Interaction, user: discord.Member, amount: int):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You need admin permissions.", ephemeral=True)
            return

        if user.id not in self.data_store.players:
            await interaction.response.send_message("❌ User not found in database.", ephemeral=True)
            return

        self.data_store.players[user.id]["elo"] = amount
        await interaction.response.send_message(f"✅ {user.display_name}'s MMR set to {amount}.", ephemeral=True)

    @app_commands.command(name="remove_from_queue", description="Force remove a user from queue")
    @app_commands.describe(user="User to remove from queue")
    async def remove_from_queue(self, interaction: Interaction, user: discord.Member):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You need admin permissions.", ephemeral=True)
            return

        for queue_id, queue_data in self.data_store.queues.items():
            if user.id in queue_data["players"]:
                queue_data["players"].remove(user.id)
                await interaction.response.send_message(f"👋 {user.display_name} removed from queue `{queue_id}`.", ephemeral=True)
                return

        await interaction.response.send_message(f"⚠️ {user.display_name} not found in any queue.", ephemeral=True)

    @app_commands.command(name="reset_mvp", description="Reset MVP votes for everyone or a specific player")
    @app_commands.describe(user="User to reset MVPs for. Leave blank for all.")
    async def reset_mvp(self, interaction: Interaction, user: discord.Member = None):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You do not have permission.", ephemeral=True)
            return

        if user:
            if user.id in self.data_store.players:
                self.data_store.players[user.id]['mvps'] = 0
                await interaction.response.send_message(f"🎯 MVPs reset for {user.mention}.", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Player not found.", ephemeral=True)
        else:
            for player in self.data_store.players.values():
                player['mvps'] = 0
            await interaction.response.send_message("🎯 MVP votes reset for all players.", ephemeral=True)

# moderation_module.py
async def setup(bot, data_store):
    await bot.add_cog(ModerationModule(bot, data_store))

