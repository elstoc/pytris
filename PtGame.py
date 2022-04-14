import sys, pygame
from pygame.locals import *

from PtShapeFactory import PtShapeFactory
from PtGrid import PtGrid
from PtScreen import PtScreen
from PtConsts import *

class PtGameOver(Exception):
    pass

class PtGame:

    def __init__(self):
        self.game_grid = PtGrid()
        self.game_screen = PtScreen(self.game_grid)
        self.speed = 50 # lower is faster
        self.score = 0

    def set_tick(self):
        self.game_tick = pygame.USEREVENT + 0
        pygame.time.set_timer(self.game_tick, self.speed * 8)

    def play(self):
        self.game_screen.draw(self.game_grid)
        self.set_tick()

        # used to prevent a pair of drop movements in a row without
        # an intervening game tick
        allow_drop = True

        try:
            while 1:
                moves = 0
                keys_pressed = []

                for event in pygame.event.get():
                    if (event.type == pygame.QUIT 
                            or (event.type == pygame.KEYDOWN and event.key == K_q)): 
                        sys.exit()
                    elif (event.type == pygame.KEYDOWN and event.key in (K_RIGHT, K_LEFT, K_DOWN, K_UP, K_SPACE)):
                        keys_pressed.append(event.key)
                    elif (event.type == self.game_tick):
                        keys_pressed.append(K_DOWN)
                        allow_drop = True

                for keyp in keys_pressed:
                    if keyp == K_RIGHT:
                        moves += self.game_grid.move(MV_RIGHT)
                    if keyp == K_LEFT:
                        moves += self.game_grid.move(MV_LEFT)
                    if keyp == K_UP:
                        moves += self.game_grid.move(MV_ROTATE)

                if moves: 
                    self.game_screen.draw(self.game_grid)

                moves = 0
                freeze = False

                if K_SPACE in keys_pressed and allow_drop:
                    freeze = True
                    moves = self.game_grid.move(MV_DROP)
                    allow_drop = False
                elif K_DOWN in keys_pressed:
                    moves = self.game_grid.move(MV_DOWN)
                    if not moves: 
                        freeze = True

                if moves or freeze:
                    try:
                        self.game_screen.draw(self.game_grid)
                    except:
                        raise PtGameOver

                if freeze:
                    self.game_grid.freeze_shape()
                    self.game_grid.new_shape()
                    rows_removed = self.game_grid.remove_rows()
                    self.score += rows_removed
                    if(rows_removed):
                        pygame.time.wait(400)
                    try:
                        self.game_screen.draw(self.game_grid)
                    except:
                        raise PtGameOver

                    # reset the timer for the new shape
                    self.set_tick()
                    # clear the event queue
                    pygame.event.get()

                pygame.time.wait(1)

        except PtGameOver:
            return self.score
