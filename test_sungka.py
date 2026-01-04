"""
Tests for Sungka game implementation.
"""

import unittest
from sungka import SungkaGame


class TestSungkaGame(unittest.TestCase):
    """Test cases for Sungka game."""
    
    def setUp(self):
        """Set up a new game before each test."""
        self.game = SungkaGame()
    
    def test_initial_board_setup(self):
        """Test that the board is initialized correctly."""
        board = self.game.get_board_state()
        
        # Check Player 1's pits (0-6)
        for i in range(7):
            self.assertEqual(board[i], 7, f"Player 1's pit {i} should have 7 stones")
        
        # Check Player 1's store (7)
        self.assertEqual(board[7], 0, "Player 1's store should be empty")
        
        # Check Player 2's pits (8-14)
        for i in range(8, 15):
            self.assertEqual(board[i], 7, f"Player 2's pit {i} should have 7 stones")
        
        # Check Player 2's store (15)
        self.assertEqual(board[15], 0, "Player 2's store should be empty")
    
    def test_initial_player(self):
        """Test that Player 1 starts the game."""
        self.assertEqual(self.game.get_current_player(), 1)
    
    def test_initial_game_not_over(self):
        """Test that game is not over at start."""
        self.assertFalse(self.game.is_game_over())
    
    def test_valid_moves_player1(self):
        """Test valid moves for Player 1."""
        valid_moves = self.game.get_valid_moves()
        self.assertEqual(valid_moves, [0, 1, 2, 3, 4, 5, 6])
    
    def test_valid_moves_player2(self):
        """Test valid moves for Player 2."""
        # Make a move that switches to Player 2
        # Use pit 0 with only 6 stones so it doesn't land in store
        self.game.board[0] = 6
        self.game.make_move(0)
        valid_moves = self.game.get_valid_moves()
        self.assertEqual(valid_moves, [8, 9, 10, 11, 12, 13, 14])
    
    def test_invalid_move_wrong_player(self):
        """Test that players cannot move opponent's pieces."""
        # Player 1 tries to move from Player 2's side
        result = self.game.make_move(8)
        self.assertFalse(result)
    
    def test_invalid_move_empty_pit(self):
        """Test that players cannot move from empty pit."""
        # Empty a pit
        self.game.board[0] = 0
        result = self.game.make_move(0)
        self.assertFalse(result)
    
    def test_basic_move(self):
        """Test a basic move distributes stones correctly."""
        # Player 1 picks from pit 0 (has 7 stones)
        self.game.make_move(0)
        board = self.game.get_board_state()
        
        # Pit 0 should be empty
        self.assertEqual(board[0], 0)
        
        # Pits 1-7 should each have one more stone
        self.assertEqual(board[1], 8)
        self.assertEqual(board[2], 8)
        self.assertEqual(board[3], 8)
        self.assertEqual(board[4], 8)
        self.assertEqual(board[5], 8)
        self.assertEqual(board[6], 8)
        self.assertEqual(board[7], 1)  # Store gets one
    
    def test_extra_turn_when_landing_in_store(self):
        """Test that player gets extra turn when last stone lands in store."""
        # Set up a scenario where last stone lands in store
        self.game.board = [0, 0, 0, 0, 0, 0, 1] + [0] + [7] * 7 + [0]
        self.game.current_player = 1
        
        # Player 1 picks from pit 6 (1 stone, will land in store at 7)
        self.game.make_move(6)
        
        # Player should still be Player 1
        self.assertEqual(self.game.get_current_player(), 1)
    
    def test_switch_player_when_not_landing_in_store(self):
        """Test that player switches when last stone doesn't land in store."""
        # Set up so last stone doesn't land in store
        # Player 1 picks from pit 0 with 6 stones (will end at pit 6, not store)
        self.game.board[0] = 6
        self.game.make_move(0)
        
        # Player should switch to Player 2
        self.assertEqual(self.game.get_current_player(), 2)
    
    def test_skip_opponent_store(self):
        """Test that stones skip opponent's store."""
        # Set up board so stones will pass opponent's store
        self.game.board = [0, 0, 0, 0, 0, 0, 10] + [0] + [0] * 7 + [0]
        self.game.current_player = 1
        
        # Player 1 picks from pit 6 (10 stones)
        self.game.make_move(6)
        board = self.game.get_board_state()
        
        # Player 2's store (15) should still be 0
        self.assertEqual(board[15], 0)
        
        # Player 1's store should have 3 stones (1 from distribution + 2 from capture)
        # Last stone lands at pit 1 (empty), opposite pit 13 has 1 stone, so capture occurs
        self.assertEqual(board[7], 3)
    
    def test_capture_stones(self):
        """Test capturing stones from opposite pit."""
        # Set up scenario for capture:
        # Player 1 has 1 stone in pit 0, which lands in empty pit 1
        # Pit 13 (opposite of pit 1) has stones
        self.game.board = [1, 0, 7, 7, 7, 7, 7, 0, 7, 7, 7, 7, 7, 5, 7, 0]
        self.game.current_player = 1
        
        # Player 1 picks from pit 0
        self.game.make_move(0)
        board = self.game.get_board_state()
        
        # Pit 1 should be empty (captured)
        self.assertEqual(board[1], 0)
        
        # Pit 13 (opposite) should be empty (captured)
        self.assertEqual(board[13], 0)
        
        # Player 1's store should have 1 + 5 = 6 stones
        self.assertEqual(board[7], 6)
    
    def test_no_capture_in_opponent_pit(self):
        """Test that capture doesn't happen in opponent's pit."""
        # Set up so stone lands in opponent's empty pit
        self.game.board = [8, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 0]
        self.game.current_player = 1
        
        # Player 1 picks from pit 0
        self.game.make_move(0)
        board = self.game.get_board_state()
        
        # No capture should occur
        # Pit 8 should have 1 stone
        self.assertEqual(board[8], 1)
    
    def test_game_over_condition(self):
        """Test that game ends when one side is empty."""
        # Set up board where Player 1's side is empty except one pit
        self.game.board = [1, 0, 0, 0, 0, 0, 0, 20, 7, 7, 7, 7, 7, 7, 7, 10]
        self.game.current_player = 1
        
        # Player 1 makes final move
        self.game.make_move(0)
        
        # Game should be over
        self.assertTrue(self.game.is_game_over())
    
    def test_collect_remaining_stones(self):
        """Test that remaining stones are collected when game ends."""
        # Set up board where Player 1's side will be empty after move
        self.game.board = [1, 0, 0, 0, 0, 0, 0, 20, 3, 3, 3, 3, 3, 3, 3, 10]
        self.game.current_player = 1
        
        # Player 1 makes final move - stone from pit 0 lands in pit 1
        # This triggers a capture: pit 1 (1 stone) + pit 13 (3 stones) = 4 captured
        self.game.make_move(0)
        board = self.game.get_board_state()
        
        # All pits should be empty
        for i in range(7):
            self.assertEqual(board[i], 0)
        for i in range(8, 15):
            self.assertEqual(board[i], 0)
        
        # Stores should have all stones
        # Player 2 had 21 stones, but 3 were captured from pit 13
        # So remaining: 21 - 3 = 18 stones collected
        self.assertEqual(board[15], 10 + 18)
    
    def test_get_winner(self):
        """Test determining the winner."""
        # Set up a finished game
        self.game.board = [0] * 7 + [50] + [0] * 7 + [48]
        self.game.game_over = True
        
        winner = self.game.get_winner()
        self.assertEqual(winner, 1)
    
    def test_get_winner_tie(self):
        """Test tie game."""
        self.game.board = [0] * 7 + [49] + [0] * 7 + [49]
        self.game.game_over = True
        
        winner = self.game.get_winner()
        self.assertEqual(winner, 0)
    
    def test_get_winner_game_not_over(self):
        """Test that winner is None when game is not over."""
        winner = self.game.get_winner()
        self.assertIsNone(winner)
    
    def test_get_scores(self):
        """Test getting current scores."""
        self.game.board[7] = 15
        self.game.board[15] = 20
        
        scores = self.game.get_scores()
        self.assertEqual(scores['player1'], 15)
        self.assertEqual(scores['player2'], 20)
    
    def test_full_game_scenario(self):
        """Test a simple full game scenario."""
        game = SungkaGame()
        
        # Modify pits to control the flow
        game.board[0] = 5  # Will end at pit 5
        game.board[8] = 6  # Will end at pit 14
        
        # Play some moves
        # Move 0: Player 1 picks pit 0 (5 stones, ends at pit 5, switches to P2)
        result = game.make_move(0)
        self.assertTrue(result, "Move 0 should be valid")
        self.assertEqual(game.get_current_player(), 2)
        
        # Move 8: Player 2 picks pit 8 (6 stones, ends at pit 14, switches to P1)
        result = game.make_move(8)
        self.assertTrue(result, "Move 8 should be valid")
        self.assertEqual(game.get_current_player(), 1)
        
        # Game should still be ongoing
        self.assertFalse(game.is_game_over())
    
    def test_no_valid_moves_ends_game(self):
        """Test that game handles no valid moves correctly."""
        # Create scenario where current player has no moves
        self.game.board = [0] * 7 + [40] + [7] * 7 + [10]
        self.game.current_player = 1
        
        valid_moves = self.game.get_valid_moves()
        self.assertEqual(valid_moves, [])


class TestSungkaEdgeCases(unittest.TestCase):
    """Test edge cases for Sungka game."""
    
    def test_wraparound_distribution(self):
        """Test that stones wrap around the board correctly."""
        game = SungkaGame()
        # Set up a pit with many stones
        game.board = [0, 0, 0, 0, 0, 0, 20] + [0] + [0] * 7 + [0]
        game.current_player = 1
        
        # Player 1 picks from pit 6
        game.make_move(6)
        board = game.get_board_state()
        
        # Verify distribution wrapped around
        # Should have stones in store 7, then pits 8-14, then wrap to 0-5
        self.assertGreater(board[7], 0)
        self.assertGreater(board[8], 0)
    
    def test_multiple_captures(self):
        """Test game with multiple captures."""
        game = SungkaGame()
        
        # Set up for capture
        game.board = [1, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 5, 7, 0]
        game.current_player = 1
        
        initial_store = game.board[7]
        game.make_move(0)
        
        # Should have captured
        self.assertGreater(game.board[7], initial_store)


if __name__ == '__main__':
    unittest.main()
