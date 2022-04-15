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

    def draw(self, game):
        # get the board grid to be drawn this iteration
        # and draw it
        board_grid = game.board.list()
        board_grid_surf = pygame.Surface((self.game_width_px, self.height_px))

        # define a single self.unit_square and fill the game surface with grid self.unit_squares
        for x in range(len(board_grid[0])):
            for y in range(len(board_grid)):
                if board_grid[y][x]:
                    self.unit_square.fill(COLOURS[board_grid[y][x]])
                    pygame.draw.rect(self.unit_square, BLACK, self.unit_square.get_rect(), width=1)
                    board_grid_surf.blit(self.unit_square, (x*self.unit_size_px, y*self.unit_size_px))

        # draw the board outline
        pygame.draw.rect(board_grid_surf, WHITE, board_grid_surf.get_rect(), width=1)

        # draw the next shape
        next_surf = pygame.Surface((4*self.unit_size_px, 4*self.unit_size_px))
        next_matrix = game.board.next_shape.base_form
        for x in range(len(next_matrix[0])):
            for y in range(len(next_matrix)):
                self.unit_square.fill(COLOURS[next_matrix[y][x]])
                pygame.draw.rect(self.unit_square, BLACK, self.unit_square.get_rect(), width=1)
                next_surf.blit(self.unit_square, (x*self.unit_size_px, y*self.unit_size_px))

        # draw the current score
        self.score_no = self.font.render("score: " + str(game.score), True, WHITE)

        # now blit everything to the screen surface
        screen_surf = pygame.Surface((self.width_px, self.height_px))
        screen_surf.blit(board_grid_surf, (self.info_width*self.unit_size_px,0))
        screen_surf.blit(next_surf, (int(self.unit_size_px * (self.info_width - len(next_matrix[0]))/2),self.unit_size_px))
        screen_surf.blit(self.score_no, (int(self.unit_size_px/4),self.height_px - self.unit_size_px))

        self.screen.blit(screen_surf, screen_surf.get_rect())

        # show the updated screen
        pygame.display.flip()

