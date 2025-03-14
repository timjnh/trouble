# Trouble

Implements the board game trouble

# Setup

    poetry install

# Execution

The following will provide help information on running individual commands:

    poetry run python trouble.py [generate|train|evaluate] -h

- `generate` - Plays games and optionally persists them to mongo
- `train` - Trains neural networks on generated data. Networks can be persisted to disk
- `evaluate` - Evaluates persisted networks against specific example states

# Tests

    PYTHONPATH=$(pwd) poetry pytest

# Type checking

    pyright -p pyrightconfig.json

# Concepts

- Track - The playing board with respect to a single color. Each color has their own track with position 0 being the first position on the board for that color and position 31 being the final four "home" positions for that color.
- Peg - A single playing piece. Has a color and a position representing the current location on that color's track.
- On deck peg - A peg that has not been moved on to the board proper. A 6 must be rolled in order to bring the player out onto the board
- Track position - A peg's position relative to its own track
- Board position - A peg's position relative to the entire board. The "start" of the board is Red's starting position and proceeds in the order Red, Green, Yellow, Blue.
