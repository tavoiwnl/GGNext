# --- cogs/party_system_module.py ---

import discord
from discord.ext import commands
from discord import app_commands, Interaction, Member, Embed

class PartySystem(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store
        self.parties = {}  # party_leader_id -> [member_ids]

    @app_commands.command(name="create_party", description="Create a new party")
    async def create_party(self, interaction: Interaction):
        user_id = interaction.user.id
        if user_id in self.parties:
            await interaction.response.send_message("❗ You already lead a party.", ephemeral=True)
            return
        self.parties[user_id] = [user_id]
        await interaction.response.send_message("✅ Party created! Use `/invite_party` to add members.", ephemeral=True)

    @app_commands.command(name="invite_party", description="Invite a member to your party")
    @app_commands.describe(member="The member to invite")
    async def invite_party(self, interaction: Interaction, member: Member):
        leader_id = interaction.user.id
        if leader_id not in self.parties:
            await interaction.response.send_message("❗ You need to create a party first.", ephemeral=True)
            return

        if any(member.id in party for party in self.parties.values()):
            await interaction.response.send_message("❗ That user is already in a party.", ephemeral=True)
            return

        self.parties[leader_id].append(member.id)
        await interaction.response.send_message(f"✅ {member.mention} added to your party.", ephemeral=True)

    @app_commands.command(name="leave_party", description="Leave your current party")
    async def leave_party(self, interaction: Interaction):
        user_id = interaction.user.id
        for leader, members in list(self.parties.items()):
            if user_id in members:
                members.remove(user_id)
                if leader == user_id or not members:
                    del self.parties[leader]
                    await interaction.response.send_message("👋 You left and disbanded the party.", ephemeral=True)
                    return
                await interaction.response.send_message("👋 You left the party.", ephemeral=True)
                return
        await interaction.response.send_message("❗ You are not in a party.", ephemeral=True)

    @app_commands.command(name="disband_party", description="Disband your party")
    async def disband_party(self, interaction: Interaction):
        leader_id = interaction.user.id
        if leader_id in self.parties:
            del self.parties[leader_id]
            await interaction.response.send_message("🧨 Party disbanded.", ephemeral=True)
        else:
            await interaction.response.send_message("❗ You are not leading any party.", ephemeral=True)

    @app_commands.command(name="party_info", description="View your current party")
    async def party_info(self, interaction: Interaction):
        user_id = interaction.user.id
        for leader, members in self.parties.items():
            if user_id in members:
                embed = Embed(title="🎉 Party Info", color=discord.Color.blue())
                embed.add_field(name="Leader", value=f"<@{leader}>", inline=False)
                member_list = "\n".join([f"<@{m}>" for m in members])
                embed.add_field(name="Members", value=member_list, inline=False)
                await interaction.response.send_message(embed=embed, ephemeral=True)
                return
        await interaction.response.send_message("❗ You are not in any party.", ephemeral=True)

async def setup(bot, data_store):
    await bot.add_cog(PartySystem(bot, data_store))

