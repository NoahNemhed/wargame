"""Unit tests for the Deck class."""

import unittest
from wargame.deck import Deck
from wargame.card import Card


class TestDeck(unittest.TestCase):
    """Test suite for the Deck class."""

    def setUp(self):
        """Create a new deck before each test."""
        self.deck = Deck()

    def test_deck_starts_with_52_cards(self):
        """Deck should contain 52 cards initially."""
        self.assertEqual(self.deck.size(), 52)

    def test_all_cards_unique(self):
        """Deck should not contain duplicate cards."""
        unique_cards = set(str(card) for card in self.deck.cards)
        self.assertEqual(len(unique_cards), 52)

    def test_draw_returns_card(self):
        """Drawing a card should return a Card instance."""
        card = self.deck.draw()
        self.assertIsInstance(card, Card)

    def test_draw_reduces_deck_size(self):
        """Drawing should reduce deck size by one."""
        before = self.deck.size()
        self.deck.draw()
        self.assertEqual(self.deck.size(), before - 1)

    def test_draw_empty_deck_raises(self):
        """Drawing from an empty deck should raise ValueError."""
        for _ in range(52):
            self.deck.draw()
        with self.assertRaises(ValueError):
            self.deck.draw()

    def test_shuffle_changes_order(self):
        """Shuffling should change the order of cards (most of the time)."""
        before = [str(card) for card in self.deck.cards]
        self.deck.shuffle()
        after = [str(card) for card in self.deck.cards]
        self.assertNotEqual(before, after)

    def test_reset_restores_full_deck(self):
        """Reset should bring the deck back to 52 cards."""
        for _ in range(10):
            self.deck.draw()
        self.deck.reset()
        self.assertEqual(self.deck.size(), 52)

    def test_str_representation(self):
        """__str__ method should return a readable deck description (len of cards)."""
        s = str(self.deck)
        self.assertIn("Deck", s)
        self.assertIn("cards", s)


if __name__ == "__main__":
    unittest.main()
