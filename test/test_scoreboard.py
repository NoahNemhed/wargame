import unittest
import os
import json
from wargame.scoreboard import Scoreboard


class TestScoreboard(unittest.TestCase):
    """Unit tests for the Scoreboard system."""

    TEST_FILE = os.path.join(os.path.dirname(__file__), "temp_scoreboard.json")

    def setUp(self):
        """Set up a clean scoreboard for testing."""
        # Create a scoreboard that writes to a temporary test file
        self.scoreboard = Scoreboard()
        self.scoreboard.FILE_PATH = self.TEST_FILE
        self.scoreboard.scores = {}
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def tearDown(self):
        """Remove test file after tests."""
        if os.path.exists(self.TEST_FILE):
            os.remove(self.TEST_FILE)

    def test_ensure_player_creates_entry(self):
        """_ensure_player should create a new player entry if missing."""
        player_data = self.scoreboard._ensure_player("noah")
        self.assertIn("noah", self.scoreboard.scores)
        self.assertEqual(player_data["games_played"], 0)

    def test_record_result_updates_scores(self):
        """record_result should increment wins/losses correctly."""
        self.scoreboard.record_result("noah", "erik")

        noah = self.scoreboard.scores["noah"]
        erik = self.scoreboard.scores["erik"]

        self.assertEqual(noah["games_won"], 1)
        self.assertEqual(noah["games_played"], 1)
        self.assertEqual(erik["games_lost"], 1)
        self.assertEqual(erik["games_played"], 1)

    def test_persistence_saves_and_loads(self):
        """Scoreboard should save to and load from JSON file."""
        self.scoreboard.record_result("adam", "erik")
        self.assertTrue(os.path.exists(self.TEST_FILE))

        # Load file manually
        with open(self.TEST_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.assertIn("adam", data)

        # Create new instance to test loading
        new_board = Scoreboard()
        new_board.FILE_PATH = self.TEST_FILE
        with open(self.TEST_FILE, "r", encoding="utf-8") as f:
            new_board.scores = json.load(f)
        self.assertIn("adam", new_board.scores)

    def test_show_empty_scoreboard_message(self):
        """show() should return friendly message if empty."""
        self.scoreboard.scores = {}
        self.assertIn("No games", self.scoreboard.show())

    def test_show_returns_formatted_string(self):
        """show() should return formatted output when players exist."""
        self.scoreboard.record_result("noah", "erik")
        output = self.scoreboard.show()
        self.assertIn("SCOREBOARD", output)
        self.assertIn("noah", output)
        self.assertIn("Wins:", output)
