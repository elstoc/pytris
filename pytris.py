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

while 1:

    draw = False

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
            draw = draw or game_grid.move(MV_RIGHT)
        if keyp == K_LEFT:
            draw = draw or game_grid.move(MV_LEFT)
        if keyp == K_UP:
            draw = draw or game_grid.move(MV_ROTATE)

    if K_SPACE in keys_pressed:
        draw = draw or game_grid.move(MV_DROP)
    elif K_DOWN in keys_pressed:
        draw = draw or game_grid.move(MV_DOWN)

    if draw: game_screen.draw(game_grid)

    pygame.time.wait(1)
