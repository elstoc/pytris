"""
Basic implementation of tetris using python and pygame

Controls:
    Left/Right:     move shape left/right
    Down:           move shape down faster
    Up:             rotate shape
    Space:          drop shape
    p:              pause
    q:              quit
"""

from functools import reduce
import random
import copy

import pygame
from pygame.locals import *

pygame.init()
pygame.key.set_repeat(200, 150)

COLOURS = [
        (0,0,0),
        (255,0,0),
        (0,255,0),
        (0,0,255),
        (255,255,0),
        (255,0,255),
        (0,255,255),
        ]

WHITE = (255,255,255)
BLACK = (0,0,0)

QUIT = -2
PAUSE = -1
TICK = 0
MV_DOWN = 1
MV_LEFT = 2
MV_RIGHT = 3
MV_ROTATE = 4
MV_DROP = 5

KEY_EVENTS = { K_q: QUIT,
               K_p: PAUSE,
               K_RIGHT: MV_RIGHT,
               K_LEFT: MV_LEFT,
               K_DOWN: MV_DOWN,
               K_UP: MV_ROTATE,
               K_SPACE: MV_DROP }

class PtOffGridRight(Exception):
    """Movement caused the shape to leave the grid (right)"""

class PtOffGridLeft(Exception):
    """Movement caused the shape to leave the grid (left)"""

class PtOffGridBottom(Exception):
    """Movement caused the shape to leave the grid (bottom)"""

class PtOverlapLeft(Exception):
    """Movement caused shaps to overlap (left)"""

class PtOverlapRight(Exception):
    """Movement caused shaps to overlap (right)"""

class PtOverlapBottom(Exception):
    """Movement caused shaps to overlap (bottom)"""

class PtGameOver(Exception):
    """An error raised to indicate end of game"""


class PtShape:
    """
    Given an initial shape layout, create rotational variants
    and change the rotation when requested
    """

    def __init__(self, variants):
        self._variants = variants
        self.rotation = 0
        self.colour = random.randrange(1, len(COLOURS))
        self.width = self.height = len(variants[0][0])
        self.posx = self.posy = 0

        # strip empty rows from zero-rotation variant for display
        self.base_form = [ x for x in self.list(0) if any(x) ]
        self.base_form_height = len(self.base_form)

    def move(self, movement):
        """Change the position or rotation of the shape"""
        if movement == MV_LEFT:
            self.posx -= 1
        elif movement == MV_RIGHT:
            self.posx += 1
        elif movement == MV_DOWN:
            self.posy += 1
        elif movement == MV_ROTATE:
            # rotate the shape clockwise by angle * 90 degrees
            self.rotation = (self.rotation + 1) % 4

    def list(self, rotation = -1):
        """
        Return the array representing the correct rotational variant
        multiply each array element by color
        """
        if rotation == -1:
            rotation = self.rotation
        return [ [ x * self.colour for x in y ] for y in self._variants[rotation] ]

    def __repr__(self):
        """A representation of the shape, O represents the shape position"""
        return '\n'.join([
            reduce(lambda x,y: x + ('O' if y else ' '), x, '')
                for x in self._variants[self.rotation]])

    def __str__(self):
        return self.__repr__()


class PtShapeFactory:
    """
    Store all possible shape formations/rotations and
    deliver new PtShape objects to the game when requested
    """

    def __init__(self):
        """
        Store four rotational variants for each shape
        designed so the bottom row always represents
        the bottom of the shape
        """

        # first define all the basic forms
        self._shapes = []

        shape0 = [[1,1],
                  [1,1]]

        self._shapes.append([shape0, shape0, shape0, shape0])

        shape0 = [[0,0,0],
                  [1,1,1],
                  [0,1,0]]

        shape1 = [[0,1,0],
                  [1,1,0],
                  [0,1,0]]

        shape2 = [[0,0,0],
                  [0,1,0],
                  [1,1,1]]

        shape3 = [[0,1,0],
                  [0,1,1],
                  [0,1,0]]

        self._shapes.append([shape0, shape1, shape2, shape3])

        shape0 = [[0,0,0],
                  [1,1,0],
                  [0,1,1]]

        shape1 = [[0,1,0],
                  [1,1,0],
                  [1,0,0]]

        shape3 = [[0,0,1],
                  [0,1,1],
                  [0,1,0]]

        self._shapes.append([shape0, shape1, shape0, shape3])

        shape0 = [[0,0,0],
                  [0,1,1],
                  [1,1,0]]

        shape1 = [[1,0,0],
                  [1,1,0],
                  [0,1,0]]

        shape3 = [[0,1,0],
                  [0,1,1],
                  [0,0,1]]

        self._shapes.append([shape0, shape1, shape0, shape3])

        shape0 = [[0,0,0,0],
                  [0,0,0,0],
                  [0,0,0,0],
                  [1,1,1,1]]

        shape1 = [[0,1,0,0],
                  [0,1,0,0],
                  [0,1,0,0],
                  [0,1,0,0]]

        shape3 = [[0,0,1,0],
                  [0,0,1,0],
                  [0,0,1,0],
                  [0,0,1,0]]

        self._shapes.append([shape0, shape1, shape0, shape3])

        shape0 = [[0,0,0,0],
                  [0,1,0,0],
                  [0,1,0,0],
                  [0,1,1,0]]

        shape1 = [[0,0,0,0],
                  [0,0,0,0],
                  [0,1,1,1],
                  [0,1,0,0]]

        shape2 = [[0,0,0,0],
                  [0,1,1,0],
                  [0,0,1,0],
                  [0,0,1,0]]

        shape3 = [[0,0,0,0],
                  [0,0,0,0],
                  [0,0,1,0],
                  [1,1,1,0]]

        self._shapes.append([shape0, shape1, shape2, shape3])

        shape0 = [[0,0,0,0],
                  [0,0,1,0],
                  [0,0,1,0],
                  [0,1,1,0]]

        shape1 = [[0,0,0,0],
                  [0,0,0,0],
                  [0,1,0,0],
                  [0,1,1,1]]

        shape2 = [[0,0,0,0],
                  [0,1,1,0],
                  [0,1,0,0],
                  [0,1,0,0]]

        shape3 = [[0,0,0,0],
                  [0,0,0,0],
                  [1,1,1,0],
                  [0,0,1,0]]

        self._shapes.append([shape0, shape1, shape2, shape3])

        self._num_shapes = len(self._shapes)

        # initialise the form history
        # avoid the "S" and "Z" shapes to start
        self._shape_hist = [2,3,2,3]

    def new_shape(self):
        """
        Return a pseudo-random shape to the caller
        attempting to avoid runs and droughts
        4 piece history with 4 rolls
        see https://simon.lc/the-history-of-tetris-randomizers
        """
        shape_no = 0
        for i in range(4):
            # four attempts to choose a shape that doesn't appear in the history
            # if the first three attempts fail always choose the fourth shape
            shape_no = random.randrange(self._num_shapes)
            if shape_no not in self._shape_hist:
                break
        del self._shape_hist[0]
        self._shape_hist.append(shape_no)

        return PtShape(self._shapes[shape_no])


class PtGameBoard:
    """The pytris game board (default/minimum 10x20; maximum 50x50)"""

    def __init__(self, width=10, height=20):
        self.sfact = PtShapeFactory()

        self.width = min(max(10, width),50)
        self.height = min(max(20, height),50)

        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]

        self.curr_shape = self.next_shape = self.sfact.new_shape()
        self.new_shape()

    def new_shape(self):
        """Create a new shape and position it in the top-centre of the board"""
        self.curr_shape = self.next_shape
        self.curr_shape.posx = int(self.width/2) - int(self.curr_shape.width/2)
        self.curr_shape.posy = 1 - self.curr_shape.height
        self.next_shape = self.sfact.new_shape()

    def freeze_shape(self):
        """Freeze current shape to grid"""
        self.grid = self.superpose_shape(self.curr_shape)

    def remove_rows(self):
        """Remove completed rows and return the number removed"""
        removed_rows = 0
        for y in range(self.height):
            if all(self.grid[y]):
                removed_rows +=1
                del self.grid[y]
                self.grid.insert(0,[0 for x in range(self.width)])

        return removed_rows

    def move_shape(self, req_movement):
        """
        Move a shape on the grid
        return True if the last move succeeded
        """
        extra_move = extra_move_count = 0
        num_moves = 0
        try_shape = copy.deepcopy(self.curr_shape)

        # the movement passed to the shape will never be MV_DROP
        # but merely repeated MV_DOWNs
        shape_move = MV_DOWN if req_movement == MV_DROP else req_movement

        while True:
            try:
                try_shape.move(extra_move if extra_move else shape_move)
                self.superpose_shape(try_shape)
            except Exception as e:
                if req_movement == MV_ROTATE:
                    # if shape initially overlaps on the left/right after rotation
                    # then allow movements to the right/left to counteract
                    # don't allow movements of more than half the shape width
                    if not extra_move:
                        # this is the first rotation failure
                        # define allowed additional movements
                        extra_move_count = int(try_shape.width/2)
                        if type(e).__name__ in ("PtOverlapLeft", "PtOffGridLeft"):
                            extra_move = MV_RIGHT
                        elif type(e).__name__ in ("PtOverlapRight", "PtOffGridRight"):
                            extra_move = MV_LEFT
                        else:
                            return num_moves
                    elif extra_move_count:
                        # decrement extra movements allowed until none left
                        extra_move_count -= 1
                    else:
                        # we've tried everything, shape could not rotate
                        return num_moves
                else:
                    return num_moves
            else:
                self.curr_shape = try_shape
                if req_movement == MV_DROP:
                    # for MV_DROP, keep repeating down moves
                    # only returning on the final (failing) movement
                    try_shape = copy.deepcopy(self.curr_shape)
                    num_moves += 1
                else:
                    return num_moves + 1

    def superpose_shape(self, shape):
        """
        Return a matrix that superposes the shape on the game grid
        error if overlaps are found
        """
        # create a new grid with same dimensions as game_grid
        grid_out = copy.deepcopy(self.grid)

        # attempt to place the shape on the grid
        # error if shape overlaps a populated square or is off grid
        for y in range(shape.height):
            for x in range(shape.width):
                if shape.list()[y][x]:
                    if shape.posy + y >= self.height:
                        raise PtOffGridBottom
                    if shape.posx + x < 0:
                        raise PtOffGridLeft
                    if shape.posx + x > self.width - 1:
                        raise PtOffGridRight
                    if (shape.posy + y >= 0
                            and grid_out[shape.posy+y][shape.posx+x]):
                        if x < shape.width/2:
                            raise PtOverlapLeft
                        if x > shape.width/2:
                            raise PtOverlapRight
                        raise PtOverlapBottom

                    if shape.posy + y >= 0:   # ignore squares above the top of the grid
                        grid_out[shape.posy+y][shape.posx+x] = shape.list()[y][x]

        return grid_out

    def list(self):
        """
        Return a matrix representing the current shape
        overlaid on the current game grid
        """
        return self.superpose_shape(self.curr_shape)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '\n'.join([
            reduce(lambda x,y: x + str(y), x, '')
                for x in self.list()])


class PtScreen:
    """Manage the rendering of the game on the screen"""

    def __init__(self, board, info_width=6, unit_size_px=20):
        self.unit_size_px = unit_size_px
        self.info_width = info_width

        self.font = pygame.font.SysFont('Hack-Regular.ttf', 20)

        self.unit_square = pygame.Surface(self.to_px(1, 1))

        self.screen = pygame.display.set_mode(self.to_px(board.width+info_width, board.height))

        # define drawing surfaces
        self.board_surf = pygame.Surface(self.to_px(board.width, board.height))
        self.shape_surf = pygame.Surface(self.to_px(4, 4))
        self.score_surf = pygame.Surface(self.to_px(info_width, 1))
        self.level_surf = pygame.Surface(self.to_px(info_width, 1))

    def to_px(self, units_x, units_y):
        """
        Given two dimensions in units,
        return the same dimensions as a tuple converted to px
        """
        return (int(self.unit_size_px * units_x), int(self.unit_size_px * units_y))

    def update_board(self, board):
        """
        Define a single self.unit_square
        fill the game surface with grid self.unit_squares
        """
        self.board_surf.fill(BLACK)
        for x in range(board.width):
            for y in range(board.height):
                if board.list()[y][x]:
                    self.unit_square.fill(COLOURS[board.list()[y][x]])
                    pygame.draw.rect(self.unit_square, BLACK, self.unit_square.get_rect(), width=1)
                    self.board_surf.blit(self.unit_square, self.to_px(x, y))

        # draw the board outline
        pygame.draw.rect(self.board_surf, WHITE, self.board_surf.get_rect(), width=1)

    def update_shape(self, shape):
        """Render the shape in a 4x4 unit square"""
        # define offset so that shape is centred horizontally
        x_offset = (4-shape.width)/2

        self.shape_surf.fill(BLACK)
        for x in range(shape.width):
            for y in range(shape.base_form_height):
                self.unit_square.fill(COLOURS[shape.base_form[y][x]])
                pygame.draw.rect(self.unit_square, BLACK, self.unit_square.get_rect(), width=1)
                self.shape_surf.blit(self.unit_square, self.to_px(x + x_offset, y + 1))

    def update_score(self, score):
        """Render the current score in a rect"""
        self.score_surf.fill(BLACK)
        score_text = self.font.render("SCORE: " + str(score), True, WHITE)
        self.score_surf.blit(score_text, self.to_px(0.25,0))

    def update_level(self, level):
        """Render the current level in a rect"""
        self.level_surf.fill(BLACK)
        level_text  = self.font.render("LEVEL: " + str(level), True, WHITE)
        self.level_surf.blit(level_text, self.to_px(0.25,0))

    def update_game(self, game):
        """Render all game elements"""
        self.update_board(game.board)
        self.update_shape(game.board.next_shape)
        self.update_score(game.score)
        self.update_level(game.level)

    def draw_paused(self, game):
        """Render the text '--PAUSED--' in the middle of the game board"""
        paused_surf = pygame.Surface(self.to_px(self.info_width, 1))
        paused_surf.fill(BLACK)
        paused_text = self.font.render("-- PAUSED --", True, WHITE)
        paused_surf.blit(paused_text, self.to_px(0.25,0))

        self.screen.blit(paused_surf,
                self.to_px(self.info_width+game.board.width/4, game.board.height/2))

        pygame.display.flip()

    def draw_game(self, game):
        """Draw all elements onto the display"""
        self.screen.fill(BLACK)
        self.screen.blit(self.score_surf, self.to_px(0, game.board.height- 1))
        self.screen.blit(self.level_surf, self.to_px(0, game.board.height - 2))
        self.screen.blit(self.board_surf, self.to_px(self.info_width,0))
        self.screen.blit(self.shape_surf, self.to_px(1,0))

        # show the updated screen
        pygame.display.flip()


class PtGame:
    """Play the game and handle events"""

    def __init__(self):
        self.board = PtGameBoard()
        self.screen = PtScreen(self.board)
        self.score = 0
        self.level = 1
        self.row_removals = 0
        self.game_tick = pygame.USEREVENT + 0

    def set_tick(self):
        """Set the game tick timer event (how often shapes fall)"""
        pygame.time.set_timer(self.game_tick, 400 - self.level*15)
        # remove any exiting events from the queue
        pygame.event.get(eventtype=self.game_tick)

    def update_stats(self, rows_removed, num_down_moves):
        """Update score and level"""
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
        """Handle pygame events and convert to pytris events"""
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
        """The main loop for a single game of pytris"""
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
                moved = 0
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
                            moved += self.board.move_shape(event)

                    if moved:
                        self.screen.update_board(self.board)
                        self.screen.draw_game(self)

                    moved = 0

                    if MV_DROP in game_events and allow_drop:
                        moved = self.board.move_shape(MV_DROP)
                        failed_down_moves +=2
                        allow_drop = False
                    elif MV_DOWN in game_events:
                        moved = self.board.move_shape(MV_DOWN)
                        if moved:
                            failed_down_moves = 0
                        else:
                            failed_down_moves +=1
                        self.set_tick()

                    if moved:
                        try:
                            self.screen.update_board(self.board)
                            self.screen.draw_game(self)
                        except:
                            raise PtGameOver

                    if failed_down_moves > 1:
                        failed_down_moves = 0
                        self.board.freeze_shape()
                        rows_removed = self.board.remove_rows()
                        self.update_stats(rows_removed, moved)
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

                pygame.time.wait(10)

        except PtGameOver:
            return self.score

if __name__ == '__main__':
    game = PtGame()
    score = game.play()

    print("You scored ", score)
