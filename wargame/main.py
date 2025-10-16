#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Entry point for the War card game."""

import shell


def main():
    """Run the War game shell."""
    print("Welcome to the War card game!")
    shell.Shell().cmdloop()


if __name__ == "__main__":
    main()
