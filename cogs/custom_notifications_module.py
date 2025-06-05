# --- custom_notifications_module.py ---

import discord
from discord.ext import commands, tasks
from discord import app_commands, Interaction, Embed
from datetime import datetime, timedelta

class CustomNotifications(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store
        self.reminder_loop.start()

    def cog_unload(self):
        self.reminder_loop.cancel()

    @app_commands.command(name="add_reminder", description="Add a custom reminder notification")
    @app_commands.describe(message="Message to send", minutes_from_now="Time in minutes from now to send the reminder")
    async def add_reminder(self, interaction: Interaction, message: str, minutes_from_now: int):
        reminder_time = datetime.utcnow() + timedelta(minutes=minutes_from_now)
        await self.data_store.add_reminder({
            "guild_id": interaction.guild_id,
            "channel_id": interaction.channel_id,
            "message": message,
            "time": reminder_time.timestamp()
        })
        await interaction.response.send_message(f"⏰ Reminder set for {minutes_from_now} minutes from now.", ephemeral=True)

    @app_commands.command(name="view_reminders", description="View upcoming scheduled reminders")
    async def view_reminders(self, interaction: Interaction):
        reminders = await self.data_store.get_reminders(guild_id=interaction.guild_id)
        if not reminders:
            await interaction.response.send_message("📭 No reminders scheduled.", ephemeral=True)
            return

        embed = Embed(title="⏰ Scheduled Reminders", color=discord.Color.green())
        for reminder in reminders:
            time_left = int(reminder['time'] - datetime.utcnow().timestamp())
            embed.add_field(
                name=f"In {time_left // 60}m {time_left % 60}s",
                value=reminder['message'],
                inline=False
            )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tasks.loop(seconds=30)
    async def reminder_loop(self):
        now = datetime.utcnow().timestamp()
        due_reminders = await self.data_store.get_due_reminders(now)
        for reminder in due_reminders:
            channel = self.bot.get_channel(reminder['channel_id'])
            if channel:
                try:
                    await channel.send(f"🔔 Reminder: {reminder['message']}")
                except Exception:
                    continue
            await self.data_store.mark_reminder_sent(reminder)

# custom_notifications_module.py
async def setup(bot, data_store):
    await bot.add_cog(CustomNotifications(bot, data_store))


