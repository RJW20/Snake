import numpy as np
from collections import deque

from food import Food
from vision import Vision


class Snake:
    """Snake that exists on the grid."""

    __slots__ = (
        "grid_size"
        "body",
        "length",
        "direction",
        "target",
        "vision",
    )

    def __init__(self, grid_size, length = 3):
        self.grid_size = grid_size

        #stop initial snake starting with some body outside the grid
        self.length = min(length, min(self.grid_size) // 2)

        self.target = Food(self.grid_size)
        self.vision = Vision()
        self.set_starting_state()

    def get_start(self) -> tuple:
        """Get a random start position on the grid.
        
        Can't be in squares with size self.length-1 in the corners.
        """

        start = (0,0)
        while ((start[0] < self.length) and (start[1] < self.length or start[1] > self.grid_size[1] - self.length)) or\
              ((start[0] > self.grid_size[0] - self.length) and (start[1] < self.length or start[1] > self.grid_size[1] - self.length)):
            start = (np.random.randint(0, self.grid_size[0] - 1), np.random.randint(0, self.grid_size[1] - 1))
        return start
    
    def set_direction(self):
        """Set initial direction parallel to closest wall, pointing to furthest wall in that direction."""

        self.direction = (0,-1)
        if min(self.vision.walls.f, self.vision.walls.b) <= min(self.vision.walls.l, self.vision.walls.r):
            #direction is right or left
            if self.vision.walls.r >= self.vision.walls.l:
                self.direction = (1,0)
                self.vision.walls.turn_right()
            else:
                self.direction = (-1,0)
                self.vision.walls.turn_left()
        else:
            #direction is up or down
            if self.vision.walls.f >= self.vision.walls.b:
                self.direction = (0,-1)
            else:
                self.direction = (0,1)
                self.vision.walls.turn_right()
                self.vision.walls.turn_right()
    
    def set_starting_state(self):
        """Get the snake in a state to begin the game.
        
        Gets the starting position, initializes vision.walls, sets the starting direction, populates the body, places the food.
        """

        start_position = self.get_start()
        self.vision.walls.seek(start_position, self.grid_size)
        self.set_direction(self)

        body = []
        for i in range(0, self.length):
            body.append(tuple(np.subtract(np.array(start_position), np.multiply(np.array(self.direction), i))))
        self.body = deque(body)

        self.target.new_position(self.body)

        #step the walls vision back one as the first thing we do is look which advances it
        self.vision.walls.f += 1
        self.vision.walls.b -= 1
        self.vision.walls.set_ordinals()

    def look(self):
        """Set the snakes vision."""

        #walls
        self.vision.walls.f -= 1
        self.vision.walls.b += 1
        self.vision.walls.set_ordinals()

        #search valid directions for food and body, using matrix transfomation to rotate around
        aim = self.direction
        ordinal_aim = (aim[0] - aim[1], aim[0] + aim[1])
        food_found = False
        for d, distance in vars(self.vision.walls).items():
            match(d):
                case 'f' | 'r' | 'b' | 'l':
                    food_found, dist_to_food, dist_to_body = self.lookInDirection(aim, False, getattr(self.vision.walls, d), self.target.position, food_found, self.body)
                    setattr(self.vision.food, d, dist_to_food)
                    setattr(self.vision.body, d, dist_to_body)
                    aim = (-aim[1], aim[0])
                case 'fr' | 'br' | 'bl' | 'fl':
                    food_found, dist_to_food, dist_to_body = self.lookInDirection(ordinal_aim, True, getattr(self.vision.walls, d), self.target.position, food_found, self.body)
                    setattr(self.vision.food, d, dist_to_food)
                    setattr(self.vision.body, d, dist_to_body)
                    ordinal_aim = (-ordinal_aim[1], ordinal_aim[0])

    def move(self):

    @property
    def dead(self):