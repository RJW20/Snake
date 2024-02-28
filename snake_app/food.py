import random
from collections import deque

from cartesian import Point


class Food:
    """Food on the grid."""

    def __init__(self, grid_size: tuple[int, int]) -> None:
        self.available_positions: tuple[int, int] = grid_size
        self.position: Point

    def new_position(self, snake_body: deque[Point]) -> None:
        """Randomize new position on the grid.
        
        Picks position not already in the snake.
        """

        self.position = (random.randint(0, self.available_positions[0] - 1), random.randint(0, self.available_positions[1] - 1))
        while self.position in snake_body:
            self.position = (random.randint(0, self.available_positions[0] - 1), random.randint(0, self.available_positions[1] - 1))
