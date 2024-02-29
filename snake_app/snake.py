import random
from collections import deque
from typing import Literal

from snake_app.cartesian import Point, Slope, Direction
from snake_app.food import Food


class Snake:
    """Snake that exists on the grid."""

    def __init__(self, grid_size: tuple[int, int], start_length: int = 3):
        self.grid_size: tuple[int, int] = grid_size
        self.start_length: int = max(min(start_length, min(self.grid_size) // 2), 3)  #stop initial snake starting with some body outside the grid
        self.direction: Direction
        self.body: deque[Point]
        self.target: Food = Food(self.grid_size)
        self.score: int

    def start_position(self) -> Point:
        """Return a random start position on the grid.
        
        Can't be in squares with size self.length - 1 in the corners.
        """

        start_pos = Point(0,0)
        while ((start_pos.x < self.start_length) and (start_pos.y < self.start_length or start_pos.y > self.grid_size[1] - self.start_length)) or\
              ((start_pos.x > self.grid_size[0] - self.start_length) and (start_pos.y < self.start_length or start_pos.y > self.grid_size[1] - self.start_length)):
            start_pos = Point(random.randint(0, self.grid_size[0] - 1), random.randint(0, self.grid_size[1] - 1))
        return start_pos
    
    def start_direction(self, start_pos: Point) -> Direction:
        """Return the starting direction.
         
        Will be parallel to closest wall, pointing to furthest wall in that direction.
        """

        #get N,E,S,W distance to walls
        N_dist = start_pos.y + 1
        E_dist = self.grid_size[0] - start_pos.x
        S_dist = self.grid_size[1] - start_pos.y
        W_dist = start_pos.x + 1

        if min(N_dist, S_dist) <= min(E_dist, W_dist):
            #direction is east or west
            if E_dist >= W_dist:
                start_dir = Direction.E
            else:
                start_dir = Direction.W
        else:
            #direction is up or down
            if N_dist >= S_dist:
                start_dir = Direction.N
            else:
                start_dir = Direction.S

        return start_dir
    
    def start_state(self) -> None:
        """Get the snake in a state to begin the game.
        
        Gets the starting position, sets the starting direction, populates the body, places the food.
        """
        
        start_position = self.start_position()
        self.direction = self.start_direction(start_position)

        body = []
        for i in range(0, self.start_length):
            body.append(start_position - self.direction.value * i)
        self.body = deque(body)

        self.target.new_position(self.body)
        self.score = 0

    def move(self, move: Literal['forward', 'right', 'left']) -> None:
        """Move the snake, increase length and re-position food if on top of it."""

        #reorient the snake's direction if changed
        match(move):
            case 'right':
                self.direction = Direction(Slope(-self.direction.value.rise, self.direction.value.run))
            case 'left':
                self.direction = Direction(Slope(self.direction.value.rise, -self.direction.value.run))

        #add a new position to the front of the snake
        new_head_position = self.body[0] + self.direction.value
        self.body.appendleft(new_head_position)

        #if we're on top of the food then we're eating it
        if self.target.position == new_head_position:
            self.target.new_position(self.body)
            self.score += 1
        #if we didn't just eat food, remove the end position
        else:
            self.body.pop()

    @property
    def hit_wall(self) -> bool:
        """Return True if snake has hit a wall.
        
        Only have to check head because the body follows the head.
        """

        head_pos = self.body[0]
        return head_pos.x < 0 or head_pos.y < 0 or head_pos.x >= self.grid_size[0] or head_pos.y >= self.grid_size[1]
    
    @property
    def hit_body(self) -> bool:
        """Return True if snake has hit its own body."""

        return self.body.count(self.body[0]) == 2

    @property
    def is_dead(self):
        """Return True if snake has hit a wall or itself."""

        return self.hit_wall or self.hit_body