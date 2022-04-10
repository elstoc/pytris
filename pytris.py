import sys, pygame
from pygame.locals import *
import random

from PtBlockFactory import PtBlockFactory
from PtGrid import PtGrid
from PtColours import colours

import sys, pygame
pygame.init()

unit_size = 20
game_grid = PtGrid()

screen_width = game_grid.width*unit_size
screen_height = game_grid.height*unit_size

screen = pygame.display.set_mode((screen_width,screen_height))

unit_square = pygame.Surface((unit_size,unit_size))
counter = 1
speed = 20 # lower is faster

while 1:
    # quit gracefully
    draw = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        if event.type == pygame.KEYUP:
            if event.key == K_LEFT:
                game_grid.move_left()
                draw = True
                break
            elif event.key == K_RIGHT:
                game_grid.move_right()
                draw = True
                break
            elif event.key == K_DOWN:
                game_grid.move_down()
                draw = True

    if not counter % speed:
        # move down and create a new block if hitting the bottom
        game_grid.move_down()
        draw = True

    if draw:
        # get the game grid to be drawn this iteration
        # and draw it
        grid_to_draw = game_grid.draw_grid
        grid_surf = pygame.Surface((screen_width,screen_height))
        grid_surf.fill((50,50,50))

        # define a single unit_square and fill the game surface with grid unit_squares
        for x in range(len(grid_to_draw[0])):
            for y in range(len(grid_to_draw)):
                if grid_to_draw[y][x]:
                    unit_square.fill(colours[grid_to_draw[y][x]])
                    grid_surf.blit(unit_square, (x*unit_size, y*unit_size))

        # draw the grid and then flip it because we use inverted coords
        screen.blit(grid_surf, grid_surf.get_rect())
        display_surface = pygame.display.get_surface()
        display_surface.blit(pygame.transform.flip(display_surface, False, True), dest=(0, 0))

        # show the updated screen
        pygame.display.flip()

    pygame.time.wait(10)
    counter += 1

