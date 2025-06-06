# /cogs/queue_management_module.py
import discord
from discord.ext import commands
from discord import app_commands, Interaction, Embed

class QueueManagement(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store

    @app_commands.command(name="create_queue", description="Create a new matchmaking queue")
    @app_commands.describe(
        name="Name of the queue",
        size="Number of players required to start a match",
        allow_parties="Allow parties to join",
        captain_mode="Enable manual captain selection mode"
    )
    async def create_queue(self, interaction: Interaction, name: str, size: int, allow_parties: bool = True, captain_mode: bool = True):
        if name in self.data_store.queues:
            await interaction.response.send_message(f"❗ A queue named `{name}` already exists.", ephemeral=True)
            return

        self.data_store.queues[name] = {
            "name": name,
            "size": size,
            "allow_parties": allow_parties,
            "captain_mode": captain_mode,
            "players": [],
            "parties": [],
            "active": True
        }

        await interaction.response.send_message(f"✅ Queue `{name}` created with size {size} players.", ephemeral=True)

    @app_commands.command(name="edit_queue", description="Edit queue settings")
    @app_commands.describe(
        name="Queue to edit",
        size="New size for match",
        allow_parties="Allow parties",
        captain_mode="Use captains manually?"
    )
    async def edit_queue(self, interaction: Interaction, name: str, size: int = None, allow_parties: bool = None, captain_mode: bool = None):
        queue = self.data_store.queues.get(name)
        if not queue:
            await interaction.response.send_message(f"❌ Queue `{name}` not found.", ephemeral=True)
            return

        if size:
            queue['size'] = size
        if allow_parties is not None:
            queue['allow_parties'] = allow_parties
        if captain_mode is not None:
            queue['captain_mode'] = captain_mode

        await interaction.response.send_message(f"✅ Queue `{name}` updated.", ephemeral=True)

    @app_commands.command(name="toggle_queue", description="Enable or disable a queue")
    @app_commands.describe(name="Queue name to toggle")
    async def toggle_queue(self, interaction: Interaction, name: str):
        queue = self.data_store.queues.get(name)
        if not queue:
            await interaction.response.send_message(f"❌ Queue `{name}` not found.", ephemeral=True)
            return
        queue['active'] = not queue['active']
        status = "enabled" if queue['active'] else "disabled"
        await interaction.response.send_message(f"✅ Queue `{name}` is now {status}.", ephemeral=True)

    @app_commands.command(name="delete_queue", description="Remove a queue from the system")
    @app_commands.describe(name="Queue to delete")
    async def delete_queue(self, interaction: Interaction, name: str):
        if name not in self.data_store.queues:
            await interaction.response.send_message(f"❌ Queue `{name}` does not exist.", ephemeral=True)
            return

        del self.data_store.queues[name]
        await interaction.response.send_message(f"🗑️ Queue `{name}` deleted successfully.", ephemeral=True)

    @app_commands.command(name="list_queues", description="List all queues")
    async def list_queues(self, interaction: Interaction):
        queues = self.data_store.queues
        if not queues:
            await interaction.response.send_message("No queues have been created.", ephemeral=True)
            return

        embed = Embed(title="📋 Active Queues", color=discord.Color.blurple())
        for q in queues.values():
            embed.add_field(
                name=q['name'],
                value=f"Players: {len(q['players'])}/{q['size']}\nParties Allowed: {q['allow_parties']}\nCaptain Mode: {q['captain_mode']}",
                inline=False
            )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def cog_check(self, ctx):
        user_id = ctx.author.id
        ban = self.data_store.tempbans.get(user_id)
        if ban and discord.utils.utcnow() < ban:
            await ctx.send("🚫 You are temporarily banned from queues due to leaving during captain selection.", ephemeral=True)
            return False
        elif ban:
            self.data_store.tempbans.pop(user_id, None)
        return True

# This is the setup function for registering the cog
async def setup(bot, data_store):
    await bot.add_cog(QueueManagement(bot, data_store))
