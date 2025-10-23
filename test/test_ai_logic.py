import unittest
from wargame.game import Game
from wargame.card import Card
from unittest.mock import patch


class TestAIDifficulty(unittest.TestCase):
    """Tests for AI difficulty behavior in the War game."""

    def setUp(self):
        self.game = Game("Player 1", "Computer")

    def test_default_difficulty_is_normal(self):
        """Game should start with normal difficulty."""
        self.assertEqual(self.game.difficulty, "normal")

    def test_set_difficulty_valid(self):
        """set_difficulty should update difficulty when given valid input."""
        self.game.set_difficulty("hard")
        self.assertEqual(self.game.difficulty, "hard")

    def test_set_difficulty_invalid_raises(self):
        """Invalid difficulty level should raise ValueError."""
        with self.assertRaises(ValueError):
            self.game.set_difficulty("extreme")

    def test_normal_mode_plays_top_card(self):
        """AI in normal mode should always play the top card."""
        self.game.set_difficulty("normal")
        self.game.player2.hand = [Card("2", "♥️"), Card("Ace", "♣️")]
        top_card = self.game.player2.hand[0]
        self.game.player1.hand = [Card("3", "♠️")]
        self.game.play_round()
        self.assertNotIn(
            top_card, self.game.player2.hand, "Top card should have been played"
        )

    def test_hard_mode_prefers_stronger_card(self):
        """AI in hard mode should pick the stronger card (top vs bottom). But its 80% chance to pick the top card instead of the strongest, so we use unittest.mock.patch to force random to return 0.1"""
        self.game.set_difficulty("hard")
        # Top is weak, bottom is strong
        self.game.player2.hand = [Card("3", "♥️"), Card("King", "♠️")]
        self.game.player1.hand = [Card("4", "♣️")]

        # Force random.random() to return 0.1 so it chooses the best card
        with patch("random.random", return_value=0.1):
            result = self.game.play_round()

        # Verify that bottom card (King) was played
        self.assertIn("King", result)
