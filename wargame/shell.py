#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Command shell for the War card game."""

import cmd
import game


class Shell(cmd.Cmd):
    """Interactive shell for playing the War game."""

    intro = "Welcome to the War game! Type help or ? to list commands.\n"
    prompt = "(war) "

    def __init__(self):
        """Initialize the shell."""
        super().__init__()
        self.game = game.Game()

    def do_start(self, _):
        """Start a new War game (placeholder)."""
        print("Starting a new game... (not yet implemented)")

    def do_exit(self, _):
        """Exit the game."""
        print("Goodbye, commander!")
        return True

    def do_quit(self, arg):
        """Alias for exit."""
        return self.do_exit(arg)

    def do_EOF(self, arg):
        """Exit with Ctrl+D."""
        return self.do_exit(arg)
