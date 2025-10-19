"""Represents a player in the War card game."""

from wargame.card import Card


class Player:
    """A player who holds cards and plays rounds in the War game."""

    def __init__(self, name: str):
        """Initialize a player with a name and an empty hand."""
        if not name or not isinstance(name, str):
            raise ValueError("Player name must be a non-empty string.")
        self.name = name
        self.hand = []

    def add_cards(self, cards):
        """Add one or more cards to the player's hand."""
        if isinstance(cards, Card):
            self.hand.append(cards)
        elif isinstance(cards, list):
            for card in cards:
                if not isinstance(card, Card):
                    raise TypeError("All elements in the list must be Card objects.")
            self.hand.extend(cards)
        else:
            raise TypeError("Must add a Card or a list of Card objects.")

    def play_card(self):
        """Play (remove and return) the top card from the player's hand."""
        if not self.hand:
            raise ValueError(f"{self.name} has no cards left to play.")
        return self.hand.pop(0)

    def has_cards(self):
        """Return True if the player still has cards."""
        return len(self.hand) > 0

    def card_count(self):
        """Return the number of cards left in the player's hand."""
        return len(self.hand)

    def __str__(self):
        """Return a string representation of the player."""
        return f"{self.name} ({len(self.hand)} cards)"
