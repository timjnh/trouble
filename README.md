# Trouble

Implements the board game trouble

# Setup

    source .venv/bin/activate
    pip install -r requirements.txt

# Tests

    PYTHONPATH=$(pwd) wexec pytest

# Concepts

- Track - The playing board with respect to a single color. Each color has their own track with position 0 being the first position on the board for that color and position 31 being the final four "home" positions for that color.
- Peg - A single playing piece. Has a color and a position representing the current location on that color's track.
- On deck peg - A peg that has not been moved on to the board proper. A 6 must be rolled in order to bring the player out onto the board
