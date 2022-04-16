import sys, pygame
from pygame.locals import *

from PtConsts import *

class PtScreen:
    def __init__(self, board, info_width=6, unit_size_px=20):
        self.unit_size_px = unit_size_px
        self.info_width = info_width

        self.width_px = (board.width+info_width)*unit_size_px
        self.height_px = board.height*unit_size_px
        self.game_width_px = board.width*unit_size_px

        self.font = pygame.font.SysFont('Hack-Regular.ttf', 20)
        self.screen = pygame.display.set_mode((self.width_px, self.height_px))

        self.unit_square = pygame.Surface((self.unit_size_px, self.unit_size_px))

        # define drawing surfaces
        self.screen_surf = pygame.Surface((self.width_px, self.height_px))
        self.board_surf = pygame.Surface((self.game_width_px, self.height_px))
        self.next_shape_surf = pygame.Surface((4*self.unit_size_px, 4*self.unit_size_px))
        self.score_surf = pygame.Surface((self.info_width*self.unit_size_px, self.unit_size_px))
        self.level_surf = pygame.Surface((self.info_width*self.unit_size_px, self.unit_size_px))

    def draw_board(self, board_grid):
        # define a single self.unit_square and fill the game surface with grid self.unit_squares
        self.board_surf.fill(BLACK)
        for x in range(len(board_grid[0])):
            for y in range(len(board_grid)):
                if board_grid[y][x]:
                    self.unit_square.fill(COLOURS[board_grid[y][x]])
                    pygame.draw.rect(self.unit_square, BLACK, self.unit_square.get_rect(), width=1)
                    self.board_surf.blit(self.unit_square, (x*self.unit_size_px, y*self.unit_size_px))

        # draw the board outline
        pygame.draw.rect(self.board_surf, WHITE, self.board_surf.get_rect(), width=1)

    def draw_next_shape(self, next_grid):
        shape_height = len(next_grid)
        shape_width = len(next_grid[0])
        x_offset = int( self.unit_size_px * (4-shape_width)/2 )

        self.next_shape_surf.fill(BLACK)
        for x in range(shape_width):
            for y in range(shape_height):
                self.unit_square.fill(COLOURS[next_grid[y][x]])
                pygame.draw.rect(self.unit_square, BLACK, self.unit_square.get_rect(), width=1)
                self.next_shape_surf.blit(self.unit_square, (x_offset + x*self.unit_size_px, (1+y)*self.unit_size_px))

    def draw_score(self, score):
        self.score_surf.fill(BLACK)
        self.score_text = self.font.render("SCORE: " + str(score), True, WHITE)
        self.score_surf.blit(self.score_text, (int(self.unit_size_px/4),0))

    def draw_level(self, level):
        self.level_surf.fill(BLACK)
        self.level_text  = self.font.render("LEVEL: " + str(level), True, WHITE)
        self.level_surf.blit(self.level_text, (int(self.unit_size_px/4),0))

    def draw(self, game):
        self.draw_board(game.board.list())
        next_grid = game.board.next_shape.base_form
        self.draw_next_shape(next_grid)
        self.draw_score(game.score)
        self.draw_level(game.level)

        # now blit everything to the screen surface
        self.screen_surf.fill(BLACK)
        self.screen_surf.blit(self.score_surf, (0, self.height_px - self.unit_size_px))
        self.screen_surf.blit(self.level_surf, (0, self.height_px - 2*self.unit_size_px))
        self.screen_surf.blit(self.board_surf, (self.info_width*self.unit_size_px,0))
        self.screen_surf.blit(self.next_shape_surf, (self.unit_size_px,0))

        self.screen.blit(self.screen_surf, self.screen_surf.get_rect())

        # show the updated screen
        pygame.display.flip()

