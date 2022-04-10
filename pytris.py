import sys, pygame
from pygame.locals import *
import random

from PtShapeFactory import PtShapeFactory
from PtGrid import PtGrid
from PtConsts import *

import sys, pygame
pygame.init()

unit_size = 20
grid_width = 10
grid_height = 20
info_width = 8
game_grid = PtGrid(grid_width, grid_height)

screen_width = (grid_width+info_width)*unit_size
screen_height = grid_height*unit_size
game_width = grid_width*unit_size
game_height = screen_height

screen = pygame.display.set_mode((screen_width,screen_height))

unit_square = pygame.Surface((unit_size,unit_size))
counter = 1
speed = 50 # lower is faster

while 1:
    # quit gracefully
    draw = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            sys.exit()
        elif event.type == pygame.KEYUP:
            # handle a single key event per loop (break when handled)
            if event.key == K_q:
                sys.exit()
            elif event.key == K_LEFT:
                draw = game_grid.move(MV_LEFT)
                break
            elif event.key == K_RIGHT:
                draw = game_grid.move(MV_RIGHT)
                break
            elif event.key == K_DOWN:
                draw = game_grid.move(MV_DOWN)
                break
            elif event.key == K_SPACE:
                draw = game_grid.move(MV_ROTATE)
                break

    if not counter % speed:
        # move down and create a new shape if hitting the bottom
        draw = game_grid.move(MV_DOWN)

    if draw:
        # get the game grid to be drawn this iteration
        # and draw it
        grid_to_draw = game_grid.list()
        grid_surf = pygame.Surface((game_width,game_height))
        grid_surf.fill((50,50,50))

        # define a single unit_square and fill the game surface with grid unit_squares
        for x in range(len(grid_to_draw[0])):
            for y in range(len(grid_to_draw)):
                if grid_to_draw[y][x]:
                    unit_square.fill(COLOURS[grid_to_draw[y][x]])
                    grid_surf.blit(unit_square, (x*unit_size, y*unit_size))

        next_surf = pygame.Surface((4*unit_size, 4*unit_size))
        next_matrix = game_grid.next_shape.list()
        for x in range(len(next_matrix[0])):
            for y in range(len(next_matrix)):
                unit_square.fill(COLOURS[next_matrix[y][x]])
                next_surf.blit(unit_square, (x*unit_size, y*unit_size))


        screen_surf = pygame.Surface((screen_width, screen_height))
        screen_surf.blit(grid_surf, (info_width*unit_size,0))
        screen_surf.blit(next_surf, (2*unit_size,(grid_height-4)*unit_size))
        # draw the grid and then flip it because we use inverted coords
        screen.blit(screen_surf, screen_surf.get_rect())
        display_surface = pygame.display.get_surface()
        display_surface.blit(pygame.transform.flip(display_surface, False, True), dest=(0, 0))

        # show the updated screen
        pygame.display.flip()

    pygame.time.wait(10)
    counter += 1

