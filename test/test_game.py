import unittest
from wargame.game import Game
from wargame.card import Card


class TestGame(unittest.TestCase):
    """Test suite for the War Game class."""

    def setUp(self):
        """Set up a game for testing."""
        self.game = Game("Noah", "Erik")
        self.game.start()

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
        self.game.player1.hand = [Card("5", "Hearts")] + [Card("6", "Clubs")] * 5
        self.game.player2.hand = [Card("5", "Spades")] + [Card("7", "Diamonds")] * 5
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
        self.assertEqual(self.game.get_winner().name, "Erik")

    def test_str_contains_round_info(self):
        """__str__ should summarize round and card counts."""
        s = str(self.game)
        self.assertIn("Round", s)
        self.assertIn("cards", s)


if __name__ == "__main__":
    unittest.main()