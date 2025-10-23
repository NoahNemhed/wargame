"""Unit tests for the Player class."""

import unittest
from wargame.player import Player
from wargame.card import Card


class TestPlayer(unittest.TestCase):
    """Test suite for Player class."""

    def setUp(self):
        """Set up a player for testing."""
        self.player = Player("Noah")

    def test_player_initialization(self):
        """Player should be created with a name and empty hand."""
        self.assertEqual(self.player.name, "Noah")
        self.assertEqual(self.player.hand, [])

    def test_invalid_name_raises(self):
        """Empty or invalid name should raise ValueError."""
        with self.assertRaises(ValueError):
            Player("")
        with self.assertRaises(ValueError):
            Player(123)

    def test_add_single_card(self):
        """Adding a single Card should work."""
        card = Card("Ace", "♥️")
        self.player.add_cards(card)
        self.assertEqual(self.player.card_count(), 1)

    def test_add_multiple_cards(self):
        """Adding multiple cards should extend the hand."""
        cards = [Card("2", "♥️"), Card("3", "♣️")]
        self.player.add_cards(cards)
        self.assertEqual(self.player.card_count(), 2)

    def test_add_invalid_object_raises(self):
        """Adding non-card should raise TypeError."""
        with self.assertRaises(TypeError):
            self.player.add_cards("Not a card")

    def test_play_card_removes_from_hand(self):
        """Playing a card should remove it from the hand."""
        card = Card("Ace", "♠️")
        self.player.add_cards(card)
        played = self.player.play_card()
        self.assertEqual(played.rank, "Ace")
        self.assertEqual(self.player.card_count(), 0)

    def test_play_card_empty_hand_raises(self):
        """Playing with no cards should raise ValueError."""
        with self.assertRaises(ValueError):
            self.player.play_card()

    def test_has_cards(self):
        """Check has_cards() returns correct boolean."""
        self.assertFalse(self.player.has_cards())
        self.player.add_cards(Card("King", "♥️"))
        self.assertTrue(self.player.has_cards())

    def test_string_representation(self):
        """__str__ should show player name and card count."""
        self.assertEqual(str(self.player), "Noah (0 cards)")
        self.player.add_cards(Card("5", "♣️"))
        self.assertIn("1 cards", str(self.player))


if __name__ == "__main__":
    unittest.main()
