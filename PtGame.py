import pygame
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
        self.screen = PtScreen(self.board)
        self.score = 0
        self.level = 1
        self.row_removals = 0
        self.freeze_time = 400
        self.game_tick = pygame.USEREVENT + 0
        self.freeze_event = pygame.USEREVENT + 1

    def set_tick(self):
        pygame.time.set_timer(self.game_tick, 400 - self.level*15)

    def set_freeze_timer(self):
        pygame.time.set_timer(self.freeze_event, 200, 1)

    def update_stats(self, rows_removed, num_down_moves):
        self.row_removals += rows_removed

        # increase score by level * multiplier
        rows_multiplier = [0, 100, 300, 500, 800]
        self.score += self.level * rows_multiplier[rows_removed]

        # for hard-drops add 2 points per cell dropped
        if num_down_moves > 1:
            self.score += 2 * num_down_moves

        # level starts at 1 and increases every 10 clearances
        # maxes out at level 20
        # but can be initiated at a higher level
        self.level = min(20, max(self.level, (self.row_removals+10) // 10))

    def play(self):
        self.screen.update_game(self)
        self.screen.draw_game(self)
        self.set_tick()

        # used to prevent a pair of drop movements in a row without
        # an intervening game tick
        allow_drop = True
        # used to indicate that a shape is waiting to freeze to the board
        freezing = False
        paused = False

        try:
            while 1:
                moves = 0
                freeze = False
                keys_pressed = []

                for event in pygame.event.get():
                    if (event.type == pygame.QUIT 
                            or (event.type == pygame.KEYDOWN and event.key == K_q)): 
                        raise PtGameOver
                    elif (event.type == pygame.KEYDOWN and event.key == K_p): 
                        paused = not paused
                        if paused:
                            self.screen.draw_paused(self)
                        else:
                            self.screen.update_game(self)
                            self.screen.draw_game(self)
                    elif (event.type == pygame.KEYDOWN and event.key in (K_RIGHT, K_LEFT, K_DOWN, K_UP, K_SPACE)):
                        keys_pressed.append(event.key)
                    elif (event.type == self.game_tick):
                        keys_pressed.append(K_DOWN)
                        allow_drop = True
                    elif (event.type == self.freeze_event):
                        freeze = True

                if not paused:
                    for keyp in keys_pressed:
                        if keyp == K_RIGHT:
                            moves += self.board.move_shape(MV_RIGHT)
                        if keyp == K_LEFT:
                            moves += self.board.move_shape(MV_LEFT)
                        if keyp == K_UP:
                            moves += self.board.move_shape(MV_ROTATE)

                    if moves: 
                        self.screen.update_board(self.board)
                        self.screen.draw_game(self)

                    moves = 0

                    if K_SPACE in keys_pressed and allow_drop:
                        freeze = True
                        moves = self.board.move_shape(MV_DROP)
                        allow_drop = False
                    elif K_DOWN in keys_pressed:
                        moves = self.board.move_shape(MV_DOWN)
                        if not moves and not freezing:
                            freezing = True
                            self.set_freeze_timer()

                    if moves or freeze:
                        try:
                            self.screen.update_board(self.board)
                            self.screen.draw_game(self)
                        except:
                            raise PtGameOver

                    if freeze:
                        self.board.freeze_shape()
                        rows_removed = self.board.remove_rows()
                        self.update_stats(rows_removed, moves)
                        self.board.new_shape()
                        if(rows_removed):
                            pygame.time.wait(200)
                        try:
                            self.screen.update_game(self)
                            self.screen.draw_game(self)
                        except:
                            raise PtGameOver

                        # reset the timer for the new shape
                        self.set_tick()
                        # clear the event queue
                        pygame.event.get()
                        freezing = False

                pygame.time.wait(1)

        except PtGameOver:
            return self.score
