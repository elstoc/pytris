import sys, pygame
from pygame.locals import *

from PtShapeFactory import PtShapeFactory
from PtGameBoard import PtGameBoard
from PtScreen import PtScreen
from PtConsts import *

class PtGameOver(Exception):
    pass

class PtGame:

    def __init__(self):
        self.board = PtGameBoard()
        self.game_screen = PtScreen(self.board)
        self.score = 0
        self.level = 1
        self.row_removals = 0

    def set_tick(self):
        self.game_tick = pygame.USEREVENT + 0
        pygame.time.set_timer(self.game_tick, 400 - self.level*15)

    def update_level(self):
        # level starts at 1 and increases every 10 clearances
        # maxes out at level 20
        # but can be initiated at a higher level
        old_level = self.level
        self.level = min(20, max(self.level, (self.row_removals+10) // 10))

    def play(self):
        self.game_screen.draw(self)
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
                        moves += self.board.move_shape(MV_RIGHT)
                    if keyp == K_LEFT:
                        moves += self.board.move_shape(MV_LEFT)
                    if keyp == K_UP:
                        moves += self.board.move_shape(MV_ROTATE)

                if moves: 
                    self.game_screen.draw(self)

                moves = 0
                freeze = False

                if K_SPACE in keys_pressed and allow_drop:
                    freeze = True
                    moves = self.board.move_shape(MV_DROP)
                    allow_drop = False
                elif K_DOWN in keys_pressed:
                    moves = self.board.move_shape(MV_DOWN)
                    if not moves: 
                        freeze = True

                if moves or freeze:
                    try:
                        self.game_screen.draw(self)
                    except:
                        raise PtGameOver

                if freeze:
                    self.board.freeze_shape()
                    self.board.new_shape()
                    rows_removed = self.board.remove_rows()
                    self.score += rows_removed
                    self.row_removals += rows_removed
                    self.update_level()
                    if(rows_removed):
                        pygame.time.wait(400)
                    try:
                        self.game_screen.draw(self)
                    except:
                        raise PtGameOver

                    # reset the timer for the new shape
                    self.set_tick()
                    # clear the event queue
                    pygame.event.get()

                pygame.time.wait(1)

        except PtGameOver:
            return self.score
