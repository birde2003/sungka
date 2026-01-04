# Sungka

A Python implementation of Sungka, a traditional Filipino mancala game.

## About Sungka

Sungka is a two-player board game popular in the Philippines. It belongs to the mancala family of count-and-capture games.

### Game Components

- **Board**: 2 rows of 7 small pits (houses) plus 2 large pits (stores/heads) at each end
- **Stones**: 98 shells or stones (7 in each of the 14 small pits at the start)
- **Players**: 2 players

### Game Rules

1. **Setup**: Each small pit starts with 7 stones. The stores start empty.

2. **Gameplay**: Players take turns picking up all stones from one of their pits and distributing them counter-clockwise, one stone per pit.

3. **Special Rules**:
   - **Extra Turn**: If the last stone lands in the player's own store, they get another turn.
   - **Capture**: If the last stone lands in an empty pit on the player's side and the opposite pit has stones, the player captures all stones from both pits and places them in their store.
   - **Skip Opponent's Store**: Stones never go into the opponent's store.

4. **End Game**: The game ends when one side has no stones left in their pits. All remaining stones are collected into the respective player's store.

5. **Winner**: The player with the most stones in their store wins.

## Installation

No external dependencies required! Just Python 3.6 or higher.

```bash
git clone https://github.com/birde2003/sungka.git
cd sungka
```

## Usage

### Play the Game

Run the command-line interface:

```bash
python sungka.py
```

### Run Tests

```bash
python -m unittest test_sungka
```

## Code Structure

- `sungka.py` - Main game implementation with CLI interface
- `test_sungka.py` - Comprehensive test suite

### Example Usage

```python
from sungka import SungkaGame

# Create a new game
game = SungkaGame()

# Make a move (pick from pit 0)
game.make_move(0)

# Check game state
print(f"Current player: {game.get_current_player()}")
print(f"Scores: {game.get_scores()}")
print(f"Game over: {game.is_game_over()}")

# Display the board
game.display_board()
```

## Board Layout

```
    P2_STORE  [6][5][4][3][2][1][0]  (Player 2's side)
              [0][1][2][3][4][5][6]  P1_STORE (Player 1's side)
```

- Player 1 controls pits 0-6 and stores in pit 7
- Player 2 controls pits 8-14 and stores in pit 15

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.