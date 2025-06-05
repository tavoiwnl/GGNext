# --- premium_module.py ---

from discord.ext import commands
from discord import app_commands, Interaction, Embed
import discord

class PremiumFeatures(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store

    @app_commands.command(name="premium_status", description="Check if your server has premium features enabled")
    async def premium_status(self, interaction: Interaction):
        is_premium = await self.data_store.is_premium_server(interaction.guild.id)
        embed = Embed(
            title="💎 Premium Status",
            description="This server **has access** to premium features!" if is_premium else "This server **does not** have premium features enabled.",
            color=discord.Color.gold() if is_premium else discord.Color.red()
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @app_commands.command(name="redeem_code", description="Redeem a premium code for your server")
    @app_commands.describe(code="The premium code to redeem")
    async def redeem_code(self, interaction: Interaction, code: str):
        success = await self.data_store.redeem_premium_code(interaction.guild.id, code)
        if success:
            await interaction.response.send_message("✅ Premium code redeemed successfully! Your server now has access to premium features.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Invalid or already used code.", ephemeral=True)

    @app_commands.command(name="premium_benefits", description="List all premium features available")
    async def premium_benefits(self, interaction: Interaction):
        embed = Embed(
            title="💎 Premium Benefits",
            description="Here are the perks your server receives with premium:",
            color=discord.Color.gold()
        )
        embed.add_field(name="⭐ Extended Stats & Leaderboards", value="Track up to 1000 users in detailed stat breakdowns", inline=False)
        embed.add_field(name="🖼️ Profile Cards", value="Access to custom profile card generation with premium visuals", inline=False)
        embed.add_field(name="🎨 UI Skins", value="Customize embeds with themes/colors", inline=False)
        embed.add_field(name="🧠 Smart Matchmaking", value="Improved MMR predictions and smarter balancing algorithms", inline=False)
        embed.add_field(name="🚀 Priority Queue Placement", value="Allow VIP users faster queue access (optional)", inline=False)
        embed.add_field(name="🔄 Faster Auto-refresh", value="Leaderboards refresh faster for live updates", inline=False)
        await interaction.response.send_message(embed=embed, ephemeral=True)

# premium_module.py
async def setup(bot, data_store):
    await bot.add_cog(PremiumModule(bot, data_store))

