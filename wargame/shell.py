#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""User-friendly command-line interface for the War card game."""

import cmd
from wargame.game import Game
from wargame.scoreboard import Scoreboard


class WarShell(cmd.Cmd):
    """Interactive shell to play the War card game."""

    intro = (
        "\n🎴 Welcome to the War card game! 🎴\n"
        "\nCommands:"
        "\n  start [name1] [name2]   -> Start a new game "
        "(Defaults to 'Player 1' vs 'Computer' if no names given)"
        "\n  set_name (<p1> or <p2>) <new_name> -> Change name of player1 "
        "(<p1>) or player2 (<p2>)"
        "\n  set_ai (<normal> or <hard> -> Changes AI difficulty (default normal)"
        "\n  show_scoreboard         -> Shows the current scoreboard"
        "\n  play_one_round          -> Play a single round"
        "\n  auto_play [num_rounds]  -> Auto-play N rounds "
        "(defaults to 5 if no number given)"
        "\n  show_status             -> Show current card counts"
        "\n  show_rules              -> Display the rules of War"
        "\n  restart_game            -> Restart the same game"
        "\n  cheat                   -> Fast-forward to the end"
        "\n  exit                    -> Exit the game"
        "\n\nType 'help' for more info on each command.\n"
    )
    prompt = "(war) "

    def __init__(self):
        """Initialize the shell with no active game."""
        super().__init__()
        self.game = None
        self.scoreboard = Scoreboard()

    # -----------------------------------------------------
    # Game control commands
    # -----------------------------------------------------

    def do_start(self, arg):
        """
        Start a new game. Usage: start [player1] [player2].

        If no names are given, defaults to 'Player 1' vs 'Computer'.
        """
        args = arg.split()
        if len(args) == 2:
            p1, p2 = args
            self.game = Game(p1, p2)
            self.game.start(is_two_player=True)
        elif len(args) == 1:
            p1 = args[0]
            self.game = Game(p1, "Computer")
            self.game.start(is_two_player=False)
        else:
            self.game = Game()
            self.game.start(is_two_player=False)

        print(self.game)

    def do_set_name(self, arg):
        """Change a player's name. Usage: set_name (<p1> or <p2>) <new_name>."""
        if not self._check_game_started():
            return

        parts = arg.split(maxsplit=1)
        if len(parts) != 2:
            print("Usage: set_name <p1|p2> <new_name>")
            return

        who, new_name = parts[0].lower(), parts[1].strip()
        if not new_name:
            print("Name cannot be empty.")
            return

        if who == "p1":
            old_name = self.game.player1.name
            self.game.player1.name = new_name
        elif who == "p2":
            old_name = self.game.player2.name
            self.game.player2.name = new_name
        else:
            print("First argument must be 'p1' or 'p2'.")
            return

        print(f"Name changed: {old_name} -> {new_name}")

    def do_play_one_round(self, _):
        """Play one round manually."""
        if not self._check_game_started():
            return
        print(self.game.play_round())
        print(self.game)

    def do_auto_play(self, arg):
        """
        Play multiple rounds automatically.

        Usage: auto_play [num_rounds]
        If no number is given, defaults to 5 rounds.
        """
        if not self._check_game_started():
            return
        try:
            rounds = int(arg) if arg else 5
        except ValueError:
            print("Invalid number of rounds. Usage: auto_play [num_rounds]")
            return

        self.game.auto_mode = True

        for _ in range(rounds):
            if self.game.is_game_over():
                break
            print(self.game.play_round())
            print(self.game)

        self.game.auto_mode = False

    def do_show_status(self, _):
        """Display the current card counts."""
        if not self._check_game_started():
            return
        print(self.game)

    def do_show_rules(self, _):
        """Display the rules of War."""
        print(
            "\n--- RULES OF WAR ---\n"
            "• Each player starts with half the deck (26 cards).\n"
            "• Both players flip the top card the one with higher card wins.\n"
            "• If the cards are equal, it's WAR:\n"
            "  - Each player lays down 3 face-down + 1 face-up card.\n"
            "  - Higher face-up card wins all cards in the pile.\n"
            "• The game continues until one player has all 52 cards.\n"
        )

    def do_restart_game(self, _):
        """Restart the game with the same players."""
        if not self._check_game_started():
            return
        name1 = self.game.player1.name
        name2 = self.game.player2.name
        self.game = Game(name1, name2)
        self.game.start()
        print(f"\nGame restarted between {name1} and {name2}!\n")
        print(self.game)

    def do_cheat(self, _):
        """Fast-forward the game until there is a winner (or we reach 1000 rounds)."""
        if not self._check_game_started():
            return

        print("Cheating... fast-forwarding to the end!\n")
        self.game.auto_mode = True

        max_rounds = 1000  # Max rounds
        rounds = 0

        while not self.game.is_game_over() and rounds < max_rounds:
            self.game.play_round()
            rounds += 1

        if not self.game.is_game_over():
            # No official winner (max rounds reached) -> decide by card count
            p1_cards = self.game.player1.card_count()
            p2_cards = self.game.player2.card_count()
            if p1_cards > p2_cards:
                self.game.winner = self.game.player1
            elif p2_cards > p1_cards:
                self.game.winner = self.game.player2
            else:
                print("\nIt's a draw after 1000 rounds!\n")
                return
        winner = self.game.get_winner()
        self.game.auto_mode = False
        print(f"\n🏆 Winner: {winner.name}\n")

        # Saves winner & loser to scoreboard.json
        if winner:
            loser = (
                self.game.player1.name
                if winner == self.game.player2
                else self.game.player2.name
            )
            self.scoreboard.record_result(winner.name, loser)

    def do_exit(self, _):
        """Exit the game."""
        print("Thanks for playing War! Goodbye")
        return True

    def _check_game_started(self):
        """Ensure a game is started before running commands."""
        if not self.game:
            print("Start a new game first using 'start'.")
            return False
        return True

    def do_set_ai(self, level):
        """
        Change AI difficulty.

        'Normal' is default. 'Hard' changes so AI will pick a card from both the top and
        bottom of the deck and has an 80% chance to play the strongest card.

        Usage: set_ai (<normal> or <hard>)
        """
        if not self._check_game_started():
            return
        if level.lower() not in ["normal", "hard"]:
            print("Invalid option. Usage: set_ai (<normal> or <hard>)")
            return
        self.game.set_difficulty(level.lower())
        print(f"AI difficulty set to: {level.capitalize()}")

    def do_show_scoreboard(self, arg):
        """Show the scoreboard with all player statistics."""
        print(self.scoreboard.show())
