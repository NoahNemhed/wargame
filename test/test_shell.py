import unittest
from wargame.shell import WarShell


class TestShell(unittest.TestCase):
    """Unit tests for the WarShell class."""

    def setUp(self):
        self.shell = WarShell()

    def test_shell_initialization(self):
        """Shell should initialize with no game started."""
        self.assertIsNone(self.shell.game)

    def test_check_game_not_started(self):
        """_check_game_started should return False before a game starts."""
        self.assertFalse(self.shell._check_game_started())

    def test_do_start_creates_game(self):
        """do_start should initialize a Game object."""
        self.shell.do_start("")
        self.assertIsNotNone(self.shell.game)
        self.assertEqual(self.shell.game.player1.name, "Player 1")
        self.assertEqual(self.shell.game.player2.name, "Player 2")

    def test_do_exit_returns_true(self):
        """do_exit should return True."""
        result = self.shell.do_exit("")
        self.assertTrue(result)

    def test_set_name_changes_player_name(self):
        """set_name should update player1 or player2 name."""
        self.shell.do_start("")
        self.shell.do_set_name("p1 Noah")
        self.assertEqual(self.shell.game.player1.name, "Noah")
        self.shell.do_set_name("p2 Erik")
        self.assertEqual(self.shell.game.player2.name, "Erik")

    def test_set_name_invalid_target(self):
        """set_name should handle invalid target without crashing."""
        self.shell.do_start("")
        # This should just print an error without crashing app
        self.shell.do_set_name("p3 Test")

    def test_auto_play_invalid_number(self):
        """auto_play with invalid number should not crash."""
        self.shell.do_start("")
        self.shell.do_auto_play("abc")  # Should handle invalid input without crash

    def test_cheat_runs_without_crash(self):
        """cheat should complete without crashing (win or draw)."""
        self.shell.do_start("")
        self.shell.do_cheat("")  # Should not raise any errors and not stuck in a infinite loop

    def test_restart_game_creates_new_instance(self):
        """restart_game should create a new Game instance."""
        self.shell.do_start("")
        old_id = id(self.shell.game)
        self.shell.do_restart_game("")
        new_id = id(self.shell.game)
        self.assertNotEqual(old_id, new_id)
