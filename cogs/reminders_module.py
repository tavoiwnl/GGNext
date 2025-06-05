# --- reminders_module.py ---

import discord
from discord.ext import commands, tasks
from discord import app_commands, Interaction
from datetime import datetime, timedelta
import asyncio

class Reminders(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store
        self.reminder_loop.start()

    def cog_unload(self):
        self.reminder_loop.cancel()

    @app_commands.command(name="reminder_add", description="Add a scheduled reminder")
    @app_commands.describe(time="Time from now in minutes", message="Reminder message")
    async def reminder_add(self, interaction: Interaction, time: int, message: str):
        trigger_time = datetime.utcnow() + timedelta(minutes=time)
        await self.data_store.add_reminder({
            "user_id": interaction.user.id,
            "channel_id": interaction.channel.id,
            "message": message,
            "time": trigger_time.timestamp()
        })
        await interaction.response.send_message(f"⏰ Reminder set for {time} minutes from now!", ephemeral=True)

    @app_commands.command(name="reminder_list", description="View your pending reminders")
    async def reminder_list(self, interaction: Interaction):
        reminders = await self.data_store.get_user_reminders(interaction.user.id)
        if not reminders:
            await interaction.response.send_message("📭 You have no upcoming reminders.", ephemeral=True)
            return

        embed = discord.Embed(title="📌 Your Reminders", color=discord.Color.orange())
        for r in reminders:
            timestamp = datetime.utcfromtimestamp(r["time"]).strftime("%Y-%m-%d %H:%M UTC")
            embed.add_field(name=timestamp, value=r["message"], inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @tasks.loop(seconds=30)
    async def reminder_loop(self):
        now = datetime.utcnow().timestamp()
        reminders = await self.data_store.get_due_reminders(now)
        for r in reminders:
            user = self.bot.get_user(r["user_id"])
            channel = self.bot.get_channel(r["channel_id"])
            if user and channel:
                try:
                    await channel.send(f"🔔 Reminder for {user.mention}: {r['message']}")
                except:
                    pass
            await self.data_store.delete_reminder(r)

async def setup(bot, extras):
    data_store = extras["data_store"]
    await bot.add_cog(YourCogClass(bot, data_store))

