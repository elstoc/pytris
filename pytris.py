import sys, pygame
from pygame.locals import *

from PtShapeFactory import PtShapeFactory
from PtGrid import PtGrid
from PtScreen import PtScreen
from PtConsts import *

import sys, pygame
pygame.init()

game_grid = PtGrid()

game_screen = PtScreen(game_grid)

speed = 50 # lower is faster
pygame.key.set_repeat(200, 150)

game_tick = pygame.USEREVENT + 0
pygame.time.set_timer(game_tick, 400)

game_screen.draw(game_grid)

class PtGameOver(Exception):
    pass

while 1:

    moved = False

    keys_pressed = []
    for event in pygame.event.get():
        if (event.type == pygame.QUIT 
                or (event.type == pygame.KEYDOWN and event.key == K_q)): 
            sys.exit()
        elif (event.type == pygame.KEYDOWN and event.key in (K_RIGHT, K_LEFT, K_DOWN, K_UP, K_SPACE)):
            keys_pressed.append(event.key)
        elif (event.type == game_tick):
            keys_pressed.append(K_DOWN)

    for keyp in keys_pressed:
        if keyp == K_RIGHT:
            moved = moved or game_grid.move(MV_RIGHT)
        if keyp == K_LEFT:
            moved = moved or game_grid.move(MV_LEFT)
        if keyp == K_UP:
            moved = moved or game_grid.move(MV_ROTATE)

    if moved: game_screen.draw(game_grid)

    moved = False
    freeze = False
    if K_SPACE in keys_pressed:
        moved = True
        freeze = True
        game_grid.move(MV_DROP)
    elif K_DOWN in keys_pressed:
        moved = game_grid.move(MV_DOWN)
        if not moved: 
            freeze = True

    if moved or freeze:
        game_screen.draw(game_grid)

    if freeze:
        game_grid.freeze_shape()
        game_grid.new_shape()
        rows_removed = game_grid.remove_rows()
        if(rows_removed):
            pygame.time.wait(400)
            try:
                # check if new shape initially fits on grid
                # by attempting to list the new grid
                game_grid.list()
            except:
                raise PtGameOver

            game_screen.draw(game_grid)

            # clear the event queue
            pygame.event.get()

    pygame.time.wait(1)
