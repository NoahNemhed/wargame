"""Handles saving, loading, and displaying player statistics for the War game."""

import json
import os


class Scoreboard:
    """Keeps track of player statistics and persists them between sessions."""

    FILE_PATH = os.path.join(os.path.dirname(__file__), "data", "scoreboard.json")

    def __init__(self):
        """Initialize scoreboard and load existing data if available."""
        os.makedirs(os.path.dirname(self.FILE_PATH), exist_ok=True)
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r", encoding="utf-8") as f:
                self.scores = json.load(f)
        else:
            self.scores = {}

    def _ensure_player(self, name):
        """Make sure player entry exists in scoreboard."""
        if name not in self.scores:
            self.scores[name] = {"games_played": 0, "games_won": 0, "games_lost": 0}
        return self.scores[name]

    def record_result(self, winner_name, loser_name):
        """Record the result of a finished game."""
        winner = self._ensure_player(winner_name)
        loser = self._ensure_player(loser_name)

        winner["games_played"] += 1
        winner["games_won"] += 1
        loser["games_played"] += 1
        loser["games_lost"] += 1

        self._save()

    def _save(self):
        """Persist current scoreboard to JSON file."""
        with open(self.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(self.scores, f, indent=4)

    def show(self):
        """Return a formatted string of all player statistics."""
        if not self.scores:
            return "No games have been played yet."

        lines = ["SCOREBOARD"]
        for name, data in sorted(self.scores.items(), key=lambda x: x[1]["games_won"], reverse=True):
            games = data["games_played"]
            rate = (data["games_won"] / games * 100) if games > 0 else 0
            lines.append(
                f"{name:<15} | "
                f"Wins: {data['games_won']:<3} | "
                f"Losses: {data['games_lost']:<3} | "
                f"Win rate: {rate:5.1f}%"
            )
        return "\n".join(lines)
