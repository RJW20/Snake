import numpy as np

from food import Food

class Snake:
    """Snake that exists on the grid."""

    __slots__ = (
        "grid_size"
        "body",
        "length",
        "direction",
        "target",
        "vision,"
    )

    def __init__(self, grid_size, length = 3):
        self.grid_size = grid_size

        #stop initial snake starting with some body outside the grid
        self.length = min(length, min(grid_size) // 2)

        #set initial starting point and direction to prepare for moving
        self.prepare()

        #generate the snakes target (the food)
        self.target = Food(self.grid_size, self.body)

    def get_start(self) -> tuple:
        """Get a random start position on the grid.
        
        Can't be in squares with size self.length-1 in the corners.
        """

        start = (0,0)
        while ((start[0] < self.length) and (start[1] < self.length or start[1] > self.grid_size[1] - self.length)) or\
              ((start[0] > self.grid_size[0] - self.length) and (start[1] < self.length or start[1] > self.grid_size[1] - self.length)):
            start = (np.random.randint(0, self.grid_size[0] - 1), np.random.randint(0, self.grid_size[1] - 1))
        return start
    