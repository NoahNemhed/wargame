#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""main entry point for the War card game."""

from wargame.shell import WarShell


def main():
    """Run the War command-line shell."""
    print(
        "\nWelcome to the WAR card game!\n"
        "Type 'help' or '?' for available commands.\n"
    )
    WarShell().cmdloop()


if __name__ == "__main__":
    main()
