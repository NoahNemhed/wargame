"""Unit tests for the Game class & AI logic."""

import unittest
from unittest.mock import patch
from wargame.game import Game
from wargame.card import Card


class TestGame(unittest.TestCase):
    """Test suite for the War Game class."""

    def setUp(self):
        """Set up a game for testing."""
        self.game = Game("Noah", "Computer")
        self.game.start()

     # Regular Game Logic 

    def test_start_deals_cards_evenly(self):
        """Deck should deal 26 cards to each player."""
        self.assertEqual(self.game.player1.card_count(), 26)
        self.assertEqual(self.game.player2.card_count(), 26)

    def test_play_round_changes_hands(self):
        """Playing one round should change hand sizes."""
        before = (self.game.player1.card_count(), self.game.player2.card_count())
        self.game.play_round()
        after = (self.game.player1.card_count(), self.game.player2.card_count())
        self.assertNotEqual(before, after)

    def test_handle_war_results_in_winner(self):
        """War should give cards to one player."""
        # Force war situation manually
        self.game.player1.hand = [Card("5", "♥️")] + [Card("6", "♣️")] * 5
        self.game.player2.hand = [Card("5", "♠️")] + [Card("7", "♦️")] * 5
        result = self.game.play_round()
        self.assertIn("wins", result)

    def test_game_over_detects_winner(self):
        """Game should end when a player has no cards."""
        self.game.player1.hand = []
        msg = self.game.play_round()
        self.assertIn("wins", msg)
        self.assertTrue(self.game.is_game_over())

    def test_get_winner_returns_correct_player(self):
        """Winner should match the game-over message."""
        self.game.player1.hand = []
        self.game.play_round()
        self.assertEqual(self.game.get_winner().name, "Computer")

    def test_str_contains_round_info(self):
        """__str__ should summarize round and card counts."""
        s = str(self.game)
        self.assertIn("Round", s)
        self.assertIn("cards", s)

    def test_handle_war_when_player1_cannot_continue(self):
        """If player1 has too few cards, player2 wins the war."""
        self.game.player1.hand = [Card("5", "♥️")]
        self.game.player2.hand = [Card("7", "♠️")] * 5
        result = self.game.handle_war([], [])
        self.assertIn("cannot continue war", result)
        self.assertEqual(self.game.winner.name, "Computer")

    def test_handle_war_when_player2_cannot_continue(self):
        """If player2 has too few cards, player1 wins the war."""
        self.game.player1.hand = [Card("7", "♠️")] * 5
        self.game.player2.hand = [Card("5", "♥️")]
        result = self.game.handle_war([], [])
        self.assertIn("cannot continue war", result)
        self.assertEqual(self.game.winner.name, "Noah")

    def test_handle_war_draw_case(self):
        """Handle recursive war when both reveal equal cards again."""
        self.game.player1.hand = [Card("9", "♣️")] * 10
        self.game.player2.hand = [Card("9", "♦️")] * 10
        result = self.game.handle_war([], [])
        self.assertIn("war", result)

    def test_play_round_increments_round_count(self):
        """Each round should increment the round counter."""
        initial_round = self.game.round_count
        self.game.play_round()
        self.assertEqual(self.game.round_count, initial_round + 1)
    
     # AI Logic Tests 

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

    def test_hard_mode_can_pick_weaker_card(self):
        """AI in hard mode can sometimes pick the weaker card (20% chance)."""
        self.game.set_difficulty("hard")
        self.game.player2.hand = [Card("3", "♥️"), Card("King", "♠️")]
        self.game.player1.hand = [Card("Queen", "♣️")]

        # Force random.random() to retun below 0.1 so it chooses the top card
        with patch("random.random", return_value=0.9):
            result = self.game.play_round()
        self.assertIn("plays", result)


if __name__ == "__main__":
    unittest.main()
