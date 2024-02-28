from typing import Literal

import pygame

from snake_app import Grid, Snake
from snake_app.cartesian import Direction
from settings import settings


def arrow_to_move(direction: Direction, key: pygame.key) -> Literal['forward', 'right', 'left']:
    """Convert pressed arrow key to direction the snake needs to turn in.
    
    Can only stay moving forward or turn left or turn right.
    """

    move = 'forward'

    if key == pygame.K_UP:
        match(direction):
            case Direction.W:
                move = 'right'
            case Direction.E:
                move = 'left'
    elif key == pygame.K_DOWN:
        match(direction):
            case Direction.E:
                move = 'right'
            case Direction.W:
                move = 'left'
    elif key == pygame.K_RIGHT:
        match(direction):
            case Direction.N:
                move = 'right'
            case Direction.S:
                move = 'left'
    elif key == pygame.K_LEFT:
        match(direction):
            case Direction.S:
                move = 'right'
            case Direction.N:
                move = 'left'

    return move


def main():
    
    #initialize the grid the game will be modelled from
    grid = Grid(settings['grid_size'], settings['block_width'], settings['block_padding'])

    #pygame setup
    screen = pygame.display.set_mode(grid.screen_size)
    pygame.display.set_caption("Snake")
    clock = pygame.time.Clock()
    running = True

    #initialize the snake
    snake = Snake(settings['grid_size'], settings['length'])
    snake.start_state()
    speed = grid.size[0] / 4    #limit the fps in such a way that it takes 4s to cross the board horizontally

    while running:

        #stops from pressing twice in one frame and then moving in forbidden directions
        key_pressed = False
        move = 'forward'

        for event in pygame.event.get():
            #so can quit
            if event.type == pygame.QUIT: 
                running = False
                break
            
            #change direction (in allowed directions)
            if event.type == pygame.KEYDOWN:
                if not key_pressed:
                    key_pressed = True
                    move = arrow_to_move(snake.direction, event.key)
            
        #move in the chosen direction
        snake.move(move)

        #check if we've died
        if snake.is_dead:
            running = False
            break

        #fill the screen to wipe last frame
        screen.fill((40,40,40))

        #visualize the snake and food on the screen
        pygame.draw.rect(screen, 'red', pygame.Rect(grid.gridpoint_to_coordinates(snake.target.position), (grid.block_width, grid.block_width)))
        for pos in snake.body:
            pygame.draw.rect(screen, 'green', pygame.Rect(grid.gridpoint_to_coordinates(pos), (grid.block_width, grid.block_width)))

        #display the changes
        pygame.display.flip()
        clock.tick(speed)

    pygame.quit()