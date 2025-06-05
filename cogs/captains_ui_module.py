# --- cogs/captains.py ---

from discord.ext import commands
from discord import app_commands, Interaction, Member, Embed, ButtonStyle, ui
import discord
import random
import asyncio
import time

class CaptainUI(commands.Cog):
    def __init__(self, bot, data_store):
        self.bot = bot
        self.data_store = data_store
        self.ongoing_matches = {}  # match_id -> match data
        self.mvp_votes = {}  # match_id -> user_id list

    class CaptainPickView(ui.View):
        def __init__(self, match_id, players, team_a, team_b, current_captain_id, pick_callback):
            super().__init__(timeout=None)
            self.match_id = match_id
            self.players = players
            self.team_a = team_a
            self.team_b = team_b
            self.current_captain_id = current_captain_id
            self.pick_callback = pick_callback

            for player in players:
                if player.id not in team_a and player.id not in team_b:
                    self.add_item(self.PickButton(player))

        class PickButton(ui.Button):
            def __init__(self, player):
                super().__init__(label=f"{player.display_name} 🎯", style=ButtonStyle.primary, custom_id=str(player.id))
                self.player = player

            async def callback(self, interaction: Interaction):
                view: CaptainUI.CaptainPickView = self.view
                for child in view.children:
                    if isinstance(child, ui.Button) and child.custom_id == self.custom_id:
                        child.disabled = True
                await interaction.response.edit_message(view=view)
                await view.pick_callback(interaction, self.player)

    class RerollView(ui.View):
        def __init__(self, initiator, match_id, on_reroll):
            super().__init__(timeout=60)
            self.initiator = initiator
            self.votes = set()
            self.match_id = match_id
            self.on_reroll = on_reroll

        @ui.button(label="Vote to Reroll Captains", style=ButtonStyle.danger, emoji="🔁")
        async def vote(self, interaction: Interaction, button: ui.Button):
            self.votes.add(interaction.user.id)
            await interaction.response.send_message(f"✅ Vote recorded. {len(self.votes)}/6 votes.", ephemeral=True)
            if len(self.votes) >= 6:
                await self.on_reroll(interaction, self.match_id)
                self.stop()

    class MVPVoteView(ui.View):
        def __init__(self, players, on_vote):
            super().__init__(timeout=60)
            for player in players:
                self.add_item(self.MVPButton(player, on_vote))

        class MVPButton(ui.Button):
            def __init__(self, player, on_vote):
                super().__init__(label=player.display_name, style=ButtonStyle.secondary, emoji="🌟")
                self.player = player
                self.on_vote = on_vote

            async def callback(self, interaction: Interaction):
                await self.on_vote(interaction, self.player)
                self.disabled = True
                await interaction.response.edit_message(content=f"🌟 Thanks for voting for {self.player.display_name}!", view=self.view)

    async def finalize_teams(self, channel, match):
        embed_a = Embed(title="🔴 Team A", description="\n".join([f"<@{uid}>" for uid in match['team_a']]), color=discord.Color.red())
        embed_b = Embed(title="🔵 Team B", description="\n".join([f"<@{uid}>" for uid in match['team_b']]), color=discord.Color.blue())
        embed_a.set_footer(text="Team A Roster")
        embed_b.set_footer(text="Team B Roster")
        await channel.send("✅ **Teams are locked in!**", embeds=[embed_a, embed_b])

        guild = self.bot.get_guild(match['guild_id'])
        category = discord.utils.get(guild.categories, name="Matches")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
        }

        for pid in match['team_a'] + match['team_b']:
            member = guild.get_member(pid)
            if member:
                overwrites[member] = discord.PermissionOverwrite(read_messages=True, send_messages=True, connect=True, speak=True)

        text_channel = await guild.create_text_channel(
            name=f"match-{match['id']}",
            category=category,
            overwrites=overwrites
        )

        voice_channel = await guild.create_voice_channel(
            name=f"Match VC {match['id']}",
            category=category,
            user_limit=10,
            overwrites=overwrites
        )

        match['text_channel_id'] = text_channel.id
        match['voice_channel_id'] = voice_channel.id
        match['start_time'] = time.time()

        await text_channel.send(embed=Embed(
            title="📸 Screenshot Required",
            description="Please post your screenshot of the match results here.",
            color=discord.Color.orange()
        ))

        await text_channel.send(embed=Embed(
            title="🏅 MVP Voting",
            description="Vote for the MVP of the match!",
            color=discord.Color.gold()
        ), view=self.MVPVoteView(match['players'], lambda i, p: self.record_mvp_vote(i, match['id'], p)))

        await text_channel.send(embed=Embed(
            title="🔄 Rematch?",
            description="React below to vote for a rematch.",
            color=discord.Color.blurple()
        ), view=await self.create_rematch_view(text_channel, match['players']))

        await self.log_match_summary(guild, match)

    async def record_mvp_vote(self, interaction: Interaction, match_id, player):
        if match_id not in self.mvp_votes:
            self.mvp_votes[match_id] = {}
        self.mvp_votes[match_id][interaction.user.id] = player.id

    async def create_rematch_view(self, text_channel, players):
        view = ui.View(timeout=60)
        rematch_votes = set()

        @ui.button(label="Rematch?", style=ButtonStyle.success, emoji="🔄")
        async def vote_rematch(interaction: Interaction, button: ui.Button):
            rematch_votes.add(interaction.user.id)
            await interaction.response.send_message(f"🔄 Rematch vote recorded: {len(rematch_votes)}/6", ephemeral=True)
            if len(rematch_votes) >= 6:
                await text_channel.send("🔁 **Rematch starting!**")
                # Restart captain draft logic goes here

        view.add_item(vote_rematch)
        return view

    async def log_match_summary(self, guild, match):
        log_channel = discord.utils.get(guild.text_channels, name="match-logs")
        if not log_channel:
            return
        duration = int(time.time() - match.get('start_time', time.time()))
        minutes = duration // 60
        seconds = duration % 60

        embed = Embed(title="📊 Match Summary", color=discord.Color.teal())
        embed.add_field(name="Match ID", value=str(match['id']), inline=True)
        embed.add_field(name="Queue", value=match.get('queue', 'N/A'), inline=True)
        embed.add_field(name="Captains", value=f"<@{match['captain1']}> vs <@{match['captain2']}>", inline=False)
        embed.add_field(name="Duration", value=f"{minutes}m {seconds}s", inline=True)
        embed.set_footer(text="Match log recorded.")

        await log_channel.send(embed=embed)

async def setup(bot, extras):
    data_store = extras["data_store"]
    await bot.add_cog(YourCogClass(bot, data_store))

