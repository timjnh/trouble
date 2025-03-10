# Trouble

Implements the board game trouble

# Setup

    poetry install

# Execution

    poetry run python trouble.py
    poetry run python trouble.py -h # for help

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
