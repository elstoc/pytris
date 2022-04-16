import sys, pygame
from pygame.locals import *

from PtConsts import *

class PtScreen:
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
        """given two dimensions in units,
        return the same dimensions as a tuple converted to px"""
        return (int(self.unit_size_px * units_x), int(self.unit_size_px * units_y))

    def update_board(self, board):
        """define a single self.unit_square 
        fill the game surface with grid self.unit_squares"""

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
        """render the shape in a 4x4 unit square"""
        # define offset so that shape is centred horizontally
        x_offset = (4-shape.width)/2

        self.shape_surf.fill(BLACK)
        for x in range(shape.width):
            for y in range(shape.base_form_height):
                self.unit_square.fill(COLOURS[shape.base_form[y][x]])
                pygame.draw.rect(self.unit_square, BLACK, self.unit_square.get_rect(), width=1)
                self.shape_surf.blit(self.unit_square, self.to_px(x + x_offset, y + 1))

    def update_score(self, score):
        """render the current score in a rect"""
        self.score_surf.fill(BLACK)
        self.score_text = self.font.render("SCORE: " + str(score), True, WHITE)
        self.score_surf.blit(self.score_text, self.to_px(0.25,0))

    def update_level(self, level):
        """render the current level in a rect"""
        self.level_surf.fill(BLACK)
        self.level_text  = self.font.render("LEVEL: " + str(level), True, WHITE)
        self.level_surf.blit(self.level_text, self.to_px(0.25,0))

    def update_game(self, game):
        """render all game elements"""
        self.update_board(game.board)
        self.update_shape(game.board.next_shape)
        self.update_score(game.score)
        self.update_level(game.level)

    def draw_game(self, game):
        """draw all elements onto the display"""

        # blit everything to the screen surface
        self.screen.blit(self.score_surf, self.to_px(0, game.board.height- 1))
        self.screen.blit(self.level_surf, self.to_px(0, game.board.height - 2))
        self.screen.blit(self.board_surf, self.to_px(self.info_width,0))
        self.screen.blit(self.shape_surf, self.to_px(1,0))

        # show the updated screen
        pygame.display.flip()

