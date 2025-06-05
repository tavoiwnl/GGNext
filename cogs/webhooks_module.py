# --- cogs/webhooks.py ---

import discord
from discord.ext import commands
from discord import app_commands, Interaction, Webhook, Embed

class Webhooks(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store

    @app_commands.command(name="create_webhook", description="Create a webhook in a specified channel")
    @app_commands.describe(channel="Channel to create the webhook in", name="Name of the webhook")
    async def create_webhook(self, interaction: Interaction, channel: discord.TextChannel, name: str):
        if not interaction.user.guild_permissions.manage_webhooks:
            await interaction.response.send_message("❌ You need `Manage Webhooks` permission to use this.", ephemeral=True)
            return

        webhook = await channel.create_webhook(name=name)
        await interaction.response.send_message(f"✅ Webhook created: {webhook.url}", ephemeral=True)

    @app_commands.command(name="delete_webhooks", description="Delete all webhooks from a specified channel")
    @app_commands.describe(channel="Channel to delete webhooks from")
    async def delete_webhooks(self, interaction: Interaction, channel: discord.TextChannel):
        if not interaction.user.guild_permissions.manage_webhooks:
            await interaction.response.send_message("❌ You need `Manage Webhooks` permission to use this.", ephemeral=True)
            return

        webhooks = await channel.webhooks()
        for hook in webhooks:
            await hook.delete()

        await interaction.response.send_message(f"🗑️ Deleted {len(webhooks)} webhook(s) in {channel.mention}", ephemeral=True)

    @app_commands.command(name="send_webhook", description="Send a custom message using a webhook")
    @app_commands.describe(webhook_url="Webhook URL to use", content="Message to send")
    async def send_webhook(self, interaction: Interaction, webhook_url: str, content: str):
        try:
            webhook = Webhook.from_url(webhook_url, client=self.bot, adapter=discord.AsyncWebhookAdapter(self.bot.http._HTTPClient__session))
            await webhook.send(content, username="WebhookBot")
            await interaction.response.send_message("✅ Message sent via webhook.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Failed to send message: {str(e)}", ephemeral=True)

# webhooks_module.py
async def setup(bot, data_store):
    await bot.add_cog(Webhooks(bot, data_store))

