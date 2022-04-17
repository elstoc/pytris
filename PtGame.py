"""The PtGame class, used to control the execution of the pytris game"""

import pygame

from PtGameBoard import PtGameBoard
from PtScreen import PtScreen
from PtConsts import *

class PtGameOver(Exception):
    """An error raised to indicate end of game"""

class PtGame:

    def __init__(self):
        self.board = PtGameBoard()
        self.screen = PtScreen(self.board)
        self.score = 0
        self.level = 1
        self.row_removals = 0
        self.game_tick = pygame.USEREVENT + 0

    def set_tick(self):
        """set the game tick timer event (how often shapes fall)"""
        pygame.time.set_timer(self.game_tick, 400 - self.level*15)

    def update_stats(self, rows_removed, num_down_moves):
        """update score and level"""
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

    def handle_events(self):
        """handle pygame events and convert to pytris events"""
        game_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_events.append(QUIT)
            elif event.type == self.game_tick:
                game_events.append(TICK)
                game_events.append(MV_DOWN)
            elif (event.type == pygame.KEYDOWN
                    and event.key in KEY_EVENTS):
                game_events.append(KEY_EVENTS[event.key])

        return game_events

    def play(self):
        """the main loop for a single game of pytris"""
        self.screen.update_game(self)
        self.screen.draw_game(self)
        self.set_tick()

        # used to prevent a pair of drop movements in a row without
        # an intervening game tick
        allow_drop = True
        paused = False
        failed_down_moves = 0

        try:
            while 1:
                moves = 0
                game_events = self.handle_events()

                if QUIT in game_events:
                    raise PtGameOver
                if PAUSE in game_events:
                    paused = not paused
                if paused:
                    self.screen.draw_paused(self)
                else:
                    self.screen.update_game(self)
                    self.screen.draw_game(self)

                    if TICK in game_events:
                        allow_drop = True

                    for event in game_events:
                        if event in (MV_RIGHT, MV_LEFT, MV_ROTATE):
                            moves += self.board.move_shape(event)

                    if moves:
                        self.screen.update_board(self.board)
                        self.screen.draw_game(self)

                    moves = 0

                    if MV_DROP in game_events and allow_drop:
                        moves = self.board.move_shape(MV_DROP)
                        failed_down_moves +=2
                        allow_drop = False
                    elif MV_DOWN in game_events:
                        moves = self.board.move_shape(MV_DOWN)
                        if moves:
                            failed_down_moves = 0
                        else:
                            failed_down_moves +=1

                    if moves:
                        try:
                            self.screen.update_board(self.board)
                            self.screen.draw_game(self)
                        except:
                            raise PtGameOver

                    if failed_down_moves > 1:
                        failed_down_moves = 0
                        self.board.freeze_shape()
                        rows_removed = self.board.remove_rows()
                        self.update_stats(rows_removed, moves)
                        self.board.new_shape()
                        if rows_removed:
                            pygame.time.wait(150)
                        try:
                            self.screen.update_game(self)
                            self.screen.draw_game(self)
                        except:
                            raise PtGameOver

                        # reset the timer for the new shape
                        self.set_tick()
                        # clear the event queue
                        pygame.event.get()

                pygame.time.wait(1)

        except PtGameOver:
            return self.score
