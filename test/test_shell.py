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
        self.assertEqual(self.shell.game.player2.name, "Computer")

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
        self.shell.do_cheat(
            ""
        )  # Should not raise any errors and not stuck in a infinite loop

    def test_restart_game_creates_new_instance(self):
        """restart_game should create a new Game instance."""
        self.shell.do_start("")
        old_id = id(self.shell.game)
        self.shell.do_restart_game("")
        new_id = id(self.shell.game)
        self.assertNotEqual(old_id, new_id)

    def test_show_scoreboard_runs(self):
        """show_scoreboard should run without crashing."""
        self.shell.do_start("")
        self.shell.do_show_scoreboard("")  

    def test_set_ai_normal_and_hard(self):
        """set_ai should accept 'normal' and 'hard' as valid inputs."""
        self.shell.do_start("")
        self.shell.do_set_ai("normal")
        self.assertEqual(self.shell.game.difficulty, "normal")

        self.shell.do_set_ai("hard")
        self.assertEqual(self.shell.game.difficulty, "hard")

    def test_set_ai_normal_and_hard_modes(self):
        """Switch between AI modes should update game difficulty."""
        self.shell.do_start("")
        self.shell.do_set_ai("normal")
        self.assertEqual(self.shell.game.difficulty, "normal")

        self.shell.do_set_ai("hard")
        self.assertEqual(self.shell.game.difficulty, "hard")

    def test_set_ai_invalid_value(self):
        """set_ai should handle invalid difficulty gracefully."""
        self.shell.do_start("")
        # Below should not make it crash
        self.shell.do_set_ai("extreme")

    def test_show_rules_runs(self):
        """show_rules should print rules without crashing."""
        self.shell.do_show_rules("")

    def test_play_one_round_runs(self):
        """play_one_round should execute without error after starting a game."""
        self.shell.do_start("")
        self.shell.do_play_one_round("")  

    def test_show_status_runs(self):
        """show_status should display counts without crashing."""
        self.shell.do_start("")
        self.shell.do_show_status("")

    def test_restart_game_without_active_game(self):
        """Restarting with no active game should not crash."""
        self.shell.do_restart_game("")
    
    def test_start_with_one_name_uses_computer_as_opponent(self):
        """Starting with one name should default to Computer."""
        self.shell.do_start("Noah")
        self.assertEqual(self.shell.game.player1.name, "Noah")
        self.assertEqual(self.shell.game.player2.name, "Computer")
        
    def test_start_with_two_names_sets_both_players(self):
        """Starting with two names should set both player names."""
        self.shell.do_start("Noah Erik")
        self.assertEqual(self.shell.game.player1.name, "Noah")
        self.assertEqual(self.shell.game.player2.name, "Erik")
    
    def test_invalid_command_does_not_crash(self):
        """Invalid command should not raise exceptions."""
        self.shell.onecmd("not_a_command")

    def test_set_name_usage_message(self):
        """set_name with missing args should display usage message (Usage: set_name <p1|p2> <new_name>)."""
        self.shell.do_start("")
        self.shell.do_set_name("") 
