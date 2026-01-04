"""
Sungka - Traditional Filipino Mancala Game

The game board consists of:
- 2 rows of 7 small pits (houses) for each player
- 2 large pits (stores/heads) at each end for collecting stones

Board layout:
    P2_STORE  [6][5][4][3][2][1][0]  (Player 2's side)
              [0][1][2][3][4][5][6]  P1_STORE (Player 1's side)

Player 1 plays from indices 0-6, stores in index 7
Player 2 plays from indices 8-14, stores in index 15
"""


class SungkaGame:
    """Sungka game implementation."""
    
    PITS_PER_SIDE = 7
    INITIAL_STONES = 7
    
    def __init__(self):
        """Initialize a new Sungka game."""
        # Board has 16 positions: 7 pits + 1 store for each player
        # Indices 0-6: Player 1's pits
        # Index 7: Player 1's store
        # Indices 8-14: Player 2's pits
        # Index 15: Player 2's store
        self.board = [self.INITIAL_STONES] * self.PITS_PER_SIDE + [0] + \
                     [self.INITIAL_STONES] * self.PITS_PER_SIDE + [0]
        self.current_player = 1
        self.game_over = False
        
    def get_board_state(self):
        """Return the current board state."""
        return self.board.copy()
    
    def get_current_player(self):
        """Return the current player (1 or 2)."""
        return self.current_player
    
    def is_game_over(self):
        """Check if the game is over."""
        return self.game_over
    
    def get_valid_moves(self):
        """Return list of valid pit indices for current player."""
        if self.game_over:
            return []
        
        if self.current_player == 1:
            # Player 1 can choose from pits 0-6
            return [i for i in range(7) if self.board[i] > 0]
        else:
            # Player 2 can choose from pits 8-14
            return [i for i in range(8, 15) if self.board[i] > 0]
    
    def make_move(self, pit_index):
        """
        Make a move by picking stones from the specified pit.
        
        Args:
            pit_index: The index of the pit to pick stones from
            
        Returns:
            bool: True if move was successful, False otherwise
        """
        # Validate move
        if pit_index not in self.get_valid_moves():
            return False
        
        # Pick up all stones from the chosen pit
        stones = self.board[pit_index]
        self.board[pit_index] = 0
        
        # Distribute stones counter-clockwise
        current_pos = pit_index
        while stones > 0:
            current_pos = (current_pos + 1) % 16
            
            # Skip opponent's store
            if self.current_player == 1 and current_pos == 15:
                continue
            if self.current_player == 2 and current_pos == 7:
                continue
            
            self.board[current_pos] += 1
            stones -= 1
        
        # Check for capture
        last_pos = current_pos
        player_store = 7 if self.current_player == 1 else 15
        player_pits = range(7) if self.current_player == 1 else range(8, 15)
        
        # Capture: last stone lands in empty pit on player's side with opposite pit having stones
        if last_pos in player_pits and self.board[last_pos] == 1:
            opposite_pos = 14 - last_pos
            if self.board[opposite_pos] > 0:
                # Capture stones from both pits
                captured = self.board[last_pos] + self.board[opposite_pos]
                self.board[last_pos] = 0
                self.board[opposite_pos] = 0
                self.board[player_store] += captured
        
        # Check if player gets another turn (last stone in own store)
        if last_pos != player_store:
            # Switch player
            self.current_player = 3 - self.current_player
        
        # Check if game is over
        self._check_game_over()
        
        return True
    
    def _check_game_over(self):
        """Check if the game is over and collect remaining stones."""
        # Game is over if one side has no stones left
        player1_has_stones = any(self.board[i] > 0 for i in range(7))
        player2_has_stones = any(self.board[i] > 0 for i in range(8, 15))
        
        if not player1_has_stones or not player2_has_stones:
            self.game_over = True
            
            # Collect remaining stones to respective stores
            for i in range(7):
                self.board[7] += self.board[i]
                self.board[i] = 0
            
            for i in range(8, 15):
                self.board[15] += self.board[i]
                self.board[i] = 0
    
    def get_scores(self):
        """Return scores for both players."""
        return {
            'player1': self.board[7],
            'player2': self.board[15]
        }
    
    def get_winner(self):
        """
        Return the winner of the game.
        
        Returns:
            int: 1 or 2 for the winning player, 0 for tie, None if game not over
        """
        if not self.game_over:
            return None
        
        scores = self.get_scores()
        if scores['player1'] > scores['player2']:
            return 1
        elif scores['player2'] > scores['player1']:
            return 2
        else:
            return 0
    
    def display_board(self):
        """Display the board in a readable format."""
        board = self.board
        
        print("\n" + "=" * 60)
        print("SUNGKA GAME")
        print("=" * 60)
        
        # Player 2's side (top row, reversed)
        print(f"\nPlayer 2's side:")
        print(f"     [{board[14]:2d}] [{board[13]:2d}] [{board[12]:2d}] [{board[11]:2d}] [{board[10]:2d}] [{board[9]:2d}] [{board[8]:2d}]")
        print(f"[{board[15]:2d}]                                     [{board[7]:2d}]")
        
        # Player 1's side (bottom row)
        print(f"     [{board[0]:2d}] [{board[1]:2d}] [{board[2]:2d}] [{board[3]:2d}] [{board[4]:2d}] [{board[5]:2d}] [{board[6]:2d}]")
        print(f"Player 1's side:")
        print()
        
        # Show current player
        if not self.game_over:
            print(f"Current player: Player {self.current_player}")
            valid_moves = self.get_valid_moves()
            if valid_moves:
                print(f"Valid moves: {valid_moves}")
        
        # Show scores
        scores = self.get_scores()
        print(f"\nScores - Player 1: {scores['player1']}, Player 2: {scores['player2']}")
        
        if self.game_over:
            winner = self.get_winner()
            if winner == 0:
                print("\nGame Over - It's a TIE!")
            else:
                print(f"\nGame Over - Player {winner} WINS!")
        
        print("=" * 60 + "\n")


def main():
    """Run a command-line game of Sungka."""
    game = SungkaGame()
    
    print("Welcome to SUNGKA!")
    print("\nRules:")
    print("- Pick a pit from your side with stones")
    print("- Stones are distributed counter-clockwise")
    print("- If your last stone lands in your store, you get another turn")
    print("- If your last stone lands in an empty pit on your side,")
    print("  you capture that stone plus all stones in the opposite pit")
    print("- Game ends when one side has no stones")
    print("- Player with most stones in their store wins")
    
    game.display_board()
    
    while not game.is_game_over():
        current_player = game.get_current_player()
        valid_moves = game.get_valid_moves()
        
        if not valid_moves:
            print(f"Player {current_player} has no valid moves!")
            break
        
        # Get player input
        while True:
            try:
                pit = int(input(f"Player {current_player}, choose a pit: "))
                if game.make_move(pit):
                    break
                else:
                    print(f"Invalid move! Valid moves: {valid_moves}")
            except (ValueError, KeyboardInterrupt):
                print("\nInvalid input. Please enter a pit number.")
                continue
            except Exception as e:
                print(f"Error: {e}")
                continue
        
        game.display_board()
    
    print("\nThanks for playing Sungka!")


if __name__ == "__main__":
    main()
