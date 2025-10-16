"""Represents a single playing card in the War game."""

class Card:
    """A single playing card with rank, suit, and value."""

    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10",
             "Jack", "Queen", "King", "Ace"]

    def __init__(self, rank: str, suit: str):
        """Initialize a card with a rank and a suit."""
        if rank not in Card.ranks:
            raise ValueError(f"Invalid rank: {rank}")
        if suit not in Card.suits:
            raise ValueError(f"Invalid suit: {suit}")

        self.rank = rank
        self.suit = suit
        self.value = Card.ranks.index(rank) + 2  # 2–14 (Ace high)

    def __str__(self):
        """Returns a readable string of the card."""
        return f"{self.rank} of {self.suit}"

    def __lt__(self, other):
        """Less-than comparison based on card value."""
        return self.value < other.value

    def __gt__(self, other):
        """Greater-than comparison based on card value."""
        return self.value > other.value

    def __eq__(self, other):
        """Equality comparison based on value."""
        return self.value == other.value
