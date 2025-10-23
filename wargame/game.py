"""Main game logic for the War card game."""

import random
from wargame.deck import Deck
from wargame.player import Player


class Game:
    """Handles setup, rounds, and game logic for War."""

    def __init__(
        self, player1_name="Player 1", player2_name="Computer", difficulty="normal"
    ):
        """Initialize the game with two players and a deck."""
        self.deck = Deck()
        self.is_two_player = False
        self.auto_mode = False
        self.player1 = Player(player1_name)
        self.player2 = Player(player2_name)
        self.difficulty = difficulty.lower()
        self.round_count = 0
        self.winner = None

    def set_difficulty(self, level):
        """Change AI difficulty (normal or hard)."""
        level = level.lower()
        if level not in ["normal", "hard"]:
            raise ValueError("Difficulty must be 'normal' or 'hard'.")
        self.difficulty = level

    def start(self, is_two_player=False):
        """Start a new game: shuffle deck and deal cards evenly."""
        self.is_two_player = is_two_player
        self.deck.reset()
        self.player1.hand.clear()
        self.player2.hand.clear()
        while not self.deck.is_empty():
            self.player1.add_cards(self.deck.draw())
            if not self.deck.is_empty():
                self.player2.add_cards(self.deck.draw())

    def play_round(self):
        """Play one round of the game."""

        # Check if game already has a winner
        if not self.player1.has_cards():
            self.winner = self.player2
            return f"Game Over: {self.player2.name} wins!"

        if not self.player2.has_cards():
            self.winner = self.player1
            return f"Game Over: {self.player1.name} wins!"

        # Two player mode
        if getattr(self, "is_two_player", False):
            if not getattr(self, "auto_mode", False):
                input(f"{self.player1.name}, press Enter to play your card...")
            card1 = self.player1.play_card()

            if not getattr(self, "auto_mode", False):
                input(f"{self.player2.name}, press Enter to play your card...")
            card2 = self.player2.play_card()

        # Single player mode
        else:
            # Player 1 always plays top card
            card1 = self.player1.play_card()

            if self.difficulty == "normal":
                # Normal mode: AI just plays top card
                card2 = self.player2.play_card()

            else:
                # Hard mode: AI looks at both top and bottom card
                top_card = self.player2.hand[0]
                bottom_card = self.player2.hand[-1]
                print(f"TOP CARD : {top_card} : BOTTOM CARD : {bottom_card}")

                # 80% chance to play stronger card
                if random.random() < 0.8:
                    if bottom_card.value > top_card.value:
                        card2 = self.player2.hand.pop(-1)
                    else:
                        card2 = self.player2.hand.pop(0)
                else:
                    # 20% chance: pick the top card anyway
                    card2 = self.player2.hand.pop(0)

        # Determine round winner
        self.round_count += 1
        result = (
            f"Round {self.round_count}: {self.player1.name} plays {card1}, "
            f"{self.player2.name} plays {card2}.\n"
        )

        if card1.value > card2.value:
            self.player1.add_cards([card1, card2])
            result += f"{self.player1.name} wins the round!"
        elif card2.value > card1.value:
            self.player2.add_cards([card1, card2])
            if not getattr(self, "is_two_player", False) and self.difficulty == "hard":
                # Only shuffle for AI after a win
                random.shuffle(self.player2.hand)
            result += f"{self.player2.name} wins the round!"
        else:
            result += self.handle_war([card1], [card2])

        return result

    def handle_war(self, pile1, pile2):
        """Handle a 'war' when players draw cards of equal value."""
        result = (
            "\nWar! Each player draws three face-down cards and one face-up card.\n"
        )

        # Check if players can continue war
        if self.player1.card_count() < 4:
            self.winner = self.player2
            return (
                f"{self.player1.name} cannot continue war. "
                f"{self.player2.name} wins the game!"
            )

        if self.player2.card_count() < 4:
            self.winner = self.player1
            return (
                f"{self.player2.name} cannot continue war. "
                f"{self.player1.name} wins the game!"
            )

        # Each player draws 3 face-down + 1 face-up
        for _ in range(3):
            pile1.append(self.player1.play_card())
            pile2.append(self.player2.play_card())

        card1 = self.player1.play_card()
        card2 = self.player2.play_card()
        pile1.append(card1)
        pile2.append(card2)

        result += (
            f"{self.player1.name} reveals {card1}, "
            f"{self.player2.name} reveals {card2}.\n"
        )

        # Compare the new face-up cards
        if card1.value > card2.value:
            self.player1.add_cards(pile1 + pile2)
            result += f"{self.player1.name} wins the war!"
        elif card2.value > card1.value:
            self.player2.add_cards(pile1 + pile2)
            result += f"{self.player2.name} wins the war!"
        else:
            # Another tie: war continiues
            result += "Another tie! War continues!\n"
            result += self.handle_war(pile1, pile2)

        return result

    def is_game_over(self):
        """Return True if one player has all the cards."""
        return self.winner is not None

    def get_winner(self):
        """Return the winner, if the game is over."""
        return self.winner

    def __str__(self):
        """Return a summary of the current game state."""
        return (
            f"--- Round {self.round_count} ---\n"
            f"{self.player1.name}: {self.player1.card_count()} cards\n"
            f"{self.player2.name}: {self.player2.card_count()} cards\n"
        )
