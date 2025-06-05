# data_store_module.py

import json
import os
from datetime import datetime

class DataStore:
    def __init__(self):
        self.players = {}
        self.matches = {}
        self.reports = []
        self.challenges = []
        self.paused_challenges = False
        self.match_history = {}
        self.seasons = {}
        self.languages = {}

    # --- Player Management ---

    def get_player_stats(self, user_id):
        return self.players.get(user_id)

    def get_leaderboard(self, limit=10, queue=None):
        sorted_players = sorted(self.players.values(), key=lambda p: p['elo'], reverse=True)
        return sorted_players[:limit]

    async def set_ign(self, user_id, ign):
        if user_id in self.players:
            self.players[user_id]['name'] = ign

    async def get_ign(self, user_id):
        return self.players.get(user_id, {}).get('name')

    # --- Match Reporting ---

    async def get_match(self, match_id):
        return self.matches.get(match_id)

    async def log_report(self, report_data):
        self.reports.append(report_data)

    async def get_reports(self):
        return self.reports[-20:]

    # --- Match History ---

    async def get_user_match_history(self, user_id, limit=5):
        return self.match_history.get(user_id, [])[-limit:]

    async def save_match_to_history(self, user_id, match):
        self.match_history.setdefault(user_id, []).append(match)

    # --- Challenge System ---

    async def get_all_challenges(self):
        return self.challenges

    async def get_challenge_progress(self, user_id):
        return self.players[user_id].get("challenges", []) if user_id in self.players else []

    async def reset_all_challenges(self):
        for player in self.players.values():
            player["challenges"] = []

    async def toggle_challenge_pause(self):
        self.paused_challenges = not self.paused_challenges
        return self.paused_challenges

    # --- Season Management ---

    async def start_season(self, season):
        self.seasons[season] = {
            "start_date": datetime.utcnow().strftime("%Y-%m-%d"),
            "status": "active"
        }

    async def end_season(self, season):
        if season in self.seasons:
            self.seasons[season]["end_date"] = datetime.utcnow().strftime("%Y-%m-%d")
            self.seasons[season]["status"] = "ended"

    async def get_season_info(self, season):
        return self.seasons.get(season)

    # --- Language ---

    async def get_user_language(self, user_id):
        return self.languages.get(user_id, "en")

    async def set_user_language(self, user_id, lang):
        self.languages[user_id] = lang

async def setup(bot, extras):
    data_store = extras["data_store"]
    await bot.add_cog(YourCogClass(bot, data_store))

