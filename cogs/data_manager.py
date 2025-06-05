# utils/data_manager.py

class DataManager:
    def __init__(self):
        self.players = {}
        self.matches = {}
        self.reports = []
        self.igns = {}
        self.seasons = {}
        self.languages = {}

    async def get_player_stats(self, user_id):
        return self.players.get(user_id)

    async def get_leaderboard(self, limit=10, queue=None):
        players = list(self.players.values())
        if queue:
            players = [p for p in players if p.get("queue") == queue]
        return sorted(players, key=lambda p: p.get("elo", 100), reverse=True)[:limit]

    async def get_leaderboard_by_role(self, role_id):
        return [p for p in self.players.values() if p.get("role_id") == role_id]

    async def get_leaderboard_by_season(self, season):
        return [p for p in self.players.values() if p.get("season") == season]

    async def set_ign(self, user_id, ign):
        self.igns[user_id] = ign

    async def get_ign(self, user_id):
        return self.igns.get(user_id)

    async def get_timed_stats(self, user_id, days):
        return self.players.get(user_id)  # Simplified for demo

    async def log_report(self, report):
        self.reports.append(report)

    async def get_reports(self):
        return self.reports

    async def start_season(self, season):
        self.seasons[season] = {"start_date": str(datetime.utcnow()), "status": "active"}

    async def end_season(self, season):
        if season in self.seasons:
            self.seasons[season]["end_date"] = str(datetime.utcnow())
            self.seasons[season]["status"] = "ended"

    async def get_season_info(self, season):
        return self.seasons.get(season)

    async def set_user_language(self, user_id, lang):
        self.languages[user_id] = lang

    async def get_user_language(self, user_id):
        return self.languages.get(user_id, "en")