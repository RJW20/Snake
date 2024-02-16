import numpy as np
from collections import deque

from .food import Food
from .vision import Vision


class Snake:
    """Snake that exists on the grid."""

    __slots__ = (
        "grid_size",
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
        self.start_state()

    def start_position(self) -> tuple:
        """Return a random start position on the grid.
        
        Can't be in squares with size self.length-1 in the corners.
        """

        start_pos = (0,0)
        while ((start_pos[0] < self.length) and (start_pos[1] < self.length or start_pos[1] > self.grid_size[1] - self.length)) or\
              ((start_pos[0] > self.grid_size[0] - self.length) and (start_pos[1] < self.length or start_pos[1] > self.grid_size[1] - self.length)):
            start_pos = (np.random.randint(0, self.grid_size[0] - 1), np.random.randint(0, self.grid_size[1] - 1))
        return start_pos
    
    def start_direction(self):
        """Return the direction parallel to closest wall, pointing to furthest wall in that direction.
        
        Also reorients vision.walls.
        """

        start_dir = (0,-1)
        if min(self.vision.walls.f, self.vision.walls.b) <= min(self.vision.walls.l, self.vision.walls.r):
            #direction is right or left
            if self.vision.walls.r >= self.vision.walls.l:
                start_dir = (1,0)
                self.vision.walls.turn_right()
            else:
                start_dir = (-1,0)
                self.vision.walls.turn_left()
        else:
            #direction is up or down
            if self.vision.walls.f >= self.vision.walls.b:
                start_dir = (0,-1)
            else:
                start_dir = (0,1)
                self.vision.walls.turn_right()
                self.vision.walls.turn_right()

        return start_dir
    
    def start_state(self):
        """Get the snake in a state to begin the game.
        
        Gets the starting position, initializes vision.walls, sets the starting direction, populates the body, places the food.
        """

        start_position = self.start_position()
        self.vision.walls.seek(start_position, self.grid_size)
        self.direction = self.start_direction()

        body = []
        for i in range(0, self.length):
            body.append(tuple(np.subtract(np.array(start_position), np.multiply(np.array(self.direction), i))))
        self.body = deque(body)

        self.target.new_position(self.body)

        #step the walls vision back one as the first thing we do is look which advances it
        self.vision.walls.f += 1
        self.vision.walls.b -= 1
        self.vision.walls.set_ordinals()

    def look_in_direction(self, search_direction: tuple[int,int], ordinal: bool, max_sight: int, food_position: tuple[int,int], food_found: bool, body: deque[tuple[int,int]]) -> tuple[bool,float,float]:
        """Return the distance to food, to self, and whether or not the food was found so we know to stop looking for it."""

        dist_to_food = np.inf
        dist_to_body = np.inf
        body_found = False
        search_position = self.body[0]

        #can't start by looking at the head
        search_position = tuple(np.add(np.array(search_position), np.array(search_direction)))
        distance = 1

        #observe food in space next to food in direction the snake is heading, this allows the snake to track down food on diagonals (only do it in ordinals)  
        if ordinal: phantom_food_position = tuple(np.add(np.array(food_position), np.array(self.direction)))

        #look until at the wall
        while distance < max_sight:
            if not food_found:
                if search_position == food_position or (ordinal and search_position == phantom_food_position):  
                    dist_to_food = distance
                    food_found = True
            if not body_found and search_position in body:
                dist_to_body = distance
                body_found = True
            
            search_position = tuple(np.add(np.array(search_position), np.array(search_direction)))
            distance += 1

        return (food_found, dist_to_food, dist_to_body)

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
                    food_found, dist_to_food, dist_to_body = self.look_in_direction(aim, False, distance, self.target.position, food_found, self.body)
                    setattr(self.vision.food, d, dist_to_food)
                    setattr(self.vision.body, d, dist_to_body)
                    aim = (-aim[1], aim[0])
                case 'fr' | 'br' | 'bl' | 'fl':
                    food_found, dist_to_food, dist_to_body = self.look_in_direction(ordinal_aim, True, distance, self.target.position, food_found, self.body)
                    setattr(self.vision.food, d, dist_to_food)
                    setattr(self.vision.body, d, dist_to_body)
                    ordinal_aim = (-ordinal_aim[1], ordinal_aim[0])

    def move(self, move: str):
        """Move the snake, increase length and re-position food if on top of it."""

        #reorient the snake's direction if changed
        match(move):
            case 'right':
                self.vision.walls.turn_right()
                self.direction = (-self.direction[1], self.direction[0])
            case 'left':
                self.vision.walls.turn_left()
                self.direction = (self.direction[1], -self.direction[0])

        #add a new position to the front of the snake
        new_head_position = tuple(np.add(np.array(self.body[0]), np.array(self.direction)))
        self.body.appendleft(new_head_position)

        #if we're on top of the food then we're eating it
        if self.target.position == new_head_position:
            self.target.new_position(self.body)
            self.length += 1
        #if we didn't just eat food, remove the end position
        else:
            self.body.pop()

    @property
    def is_dead(self):
        if self.vision.walls.f == 1: return True    #if hit a wall
        if self.body.count(self.body[0]) == 2: return True     #if hit own body 