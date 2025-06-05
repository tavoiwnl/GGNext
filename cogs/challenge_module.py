# challenge_module.py

import discord
from discord.ext import commands
from discord import app_commands, Interaction, Embed
from utils.database import DataStore

class PlayerChallenges(commands.Cog):
    def __init__(self, bot, data_store: DataStore):
        self.bot = bot
        self.data_store = data_store

    # USER: View All Challenges
    @app_commands.command(name="challenges", description="View available challenges")
    async def view_challenges(self, interaction: Interaction):
        challenges = await self.data_store.get_all_challenges()
        if not challenges:
            await interaction.response.send_message("❌ No challenges currently available.", ephemeral=True)
            return

        embed = Embed(title="🏆 Active Player Challenges", color=discord.Color.orange())
        for challenge in challenges:
            embed.add_field(
                name=challenge.get("name") or challenge.get("title"),
                value=f"{challenge['description']}\nReward: {challenge['reward']} ELO",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    # USER: View Own Progress
    @app_commands.command(name="challenge_progress", description="View your personal challenge progress")
    async def challenge_progress(self, interaction: Interaction):
        user_id = interaction.user.id
        progress = await self.data_store.get_challenge_progress(user_id)

        if not progress:
            await interaction.response.send_message("You haven't made any challenge progress yet!", ephemeral=True)
            return

        embed = Embed(title=f"📈 {interaction.user.display_name}'s Challenge Progress", color=discord.Color.green())
        for ch in progress:
            embed.add_field(
                name=ch.get("name") or ch.get("title"),
                value=f"Progress: {ch['current']} / {ch['goal']} - {'✅ Completed' if ch['completed'] else 'In Progress'}",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    # USER: Start Challenge Set
    @app_commands.command(name="challenge_start", description="Start a new set of challenges")
    async def challenge_start(self, interaction: Interaction):
        await self.data_store.start_user_challenges(interaction.user.id)
        await interaction.response.send_message("🚀 Challenge progression started. Good luck!", ephemeral=True)

    # USER: Refresh Challenges
    @app_commands.command(name="challenge_refresh", description="Refresh your challenge list")
    async def challenge_refresh(self, interaction: Interaction):
        await self.data_store.refresh_user_challenges(interaction.user.id)
        await interaction.response.send_message("🔄 Your challenges have been refreshed.", ephemeral=True)

    # USER: Pause Challenge Tracking
    @app_commands.command(name="challenge_pause", description="Pause your personal challenge progression")
    async def challenge_pause(self, interaction: Interaction):
        await self.data_store.pause_user_challenges(interaction.user.id)
        await interaction.response.send_message("⏸️ Challenge progression paused.", ephemeral=True)

    # ADMIN: Reset All Challenge Progress
    @app_commands.command(name="reset_challenges", description="Admin-only: Reset all player challenge progress")
    async def reset_challenges(self, interaction: Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You don't have permission to do this.", ephemeral=True)
            return

        await self.data_store.reset_all_challenges()
        await interaction.response.send_message("🧹 All player challenge progress has been reset.", ephemeral=True)

    # ADMIN: Pause Global Challenge Tracking
    @app_commands.command(name="pause_challenges", description="Admin-only: Pause or resume challenge tracking globally")
    async def pause_challenges(self, interaction: Interaction):
        if not interaction.user.guild_permissions.administrator:
            await interaction.response.send_message("❌ You don't have permission to do this.", ephemeral=True)
            return

        status = await self.data_store.toggle_challenge_pause()
        await interaction.response.send_message(f"⏸️ Challenge tracking is now {'paused' if status else 'active'}.", ephemeral=True)

# challenge_module.py
async def setup(bot, data_store):
    await bot.add_cog(ChallengeModule(bot, data_store))

