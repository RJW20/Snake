import numpy as np

class Food:
    """Food on the grid."""

    __slots__ = (
        "available_positions",
        "position",
        "generator",
    )

    def __init__(self, grid_size, snake_body):
        self.available_positions = grid_size
        self.generator = np.random
        self.newPosition(snake_body)

    #randomize a new position on the grid, thats not already in the snake (might blow up in time when snake gets big)
    def newPosition(self, snake_body):
        """Randomize new position on the grid.
        
        Picks position not already in the snake.
        """
        self.position = (self.generator.randint(0, self.available_positions[0]), self.generator.randint(0, self.available_positions[1]))
        while self.position in snake_body:
            self.position = (self.generator.randint(0, self.available_positions[0]), self.generator.randint(0, self.available_positions[1]))