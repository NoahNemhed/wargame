"""Unit tests for the Card class."""

import unittest
from wargame.card import Card


class TestCard(unittest.TestCase):
    """Test suite for Card class."""

    def setUp(self):
        """Set up before each test."""
        self.card = Card("Ace", "Hearts")

    def test_card_creation(self):
        """Card should be created with valid rank and suit."""
        self.assertEqual(self.card.rank, "Ace")
        self.assertEqual(self.card.suit, "Hearts")
        self.assertEqual(self.card.value, 14)

    def test_invalid_rank_raises(self):
        """Invalid rank should raise ValueError."""
        with self.assertRaises(ValueError):
            Card("One", "Spades")

    def test_invalid_suit_raises(self):
        """Invalid suit should raise ValueError."""
        with self.assertRaises(ValueError):
            Card("Ace", "Stars")

    def test_str_representation(self):
        """String conversion should return 'Rank of Suit'."""
        card = Card("10", "Diamonds")
        self.assertEqual(str(card), "10 of Diamonds")

    def test_comparison(self):
        """Test card comparison operators."""
        low = Card("2", "Hearts")
        high = Card("King", "Spades")
        self.assertTrue(low < high)
        self.assertTrue(high > low)
        self.assertTrue(Card("Queen", "Clubs") == Card("Queen", "Diamonds"))


if __name__ == "__main__":
    unittest.main()
