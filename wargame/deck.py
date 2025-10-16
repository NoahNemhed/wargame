"""Represents a standard 52-card deck"""

import random
from wargame.card import Card


class Deck:
    """A deck containing 52 unique playing cards."""

    def __init__(self):
        """Creates a new deck and shuffles it."""
        self.cards = []
        self.reset()

    def reset(self):
        """Reset the deck to contain all 52 cards and shuffle them."""
        self.cards = [Card(rank, suit)
                      for suit in Card.suits
                      for rank in Card.ranks]
        self.shuffle()

    def shuffle(self):
        """Shuffle the deck in place."""
        random.shuffle(self.cards)

    def draw(self):
        """Draws one card from the top of the deck."""
        if not self.cards:
            raise ValueError("No more cards left in the deck.")
        return self.cards.pop(0)

    def size(self):
        """Return the number of cards remaining in the deck."""
        return len(self.cards)

    def is_empty(self):
        """Return True if the deck has no cards left."""
        return not self.cards

    def __str__(self):
        """Return a short string representation of the deck."""
        return f"Deck with {len(self.cards)} cards remaining."
