import numpy as np


class Food:
    """Food on the grid."""

    __slots__ = (
        "available_positions",
        "position",
    )

    def __init__(self, grid_size):
        self.available_positions = grid_size

    def new_position(self, snake_body):
        """Randomize new position on the grid.
        
        Picks position not already in the snake.
        """

        self.position = (np.random.randint(0, self.available_positions[0]), np.random.randint(0, self.available_positions[1]))
        while self.position in snake_body:
            self.position = (np.random.randint(0, self.available_positions[0]), np.random.randint(0, self.available_positions[1]))
