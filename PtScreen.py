import sys, pygame
from pygame.locals import *

from PtGrid import PtGrid
from PtConsts import *

class PtScreen:
    def __init__(self, game_grid, info_width=8, unit_size=20):
        self.unit_size = unit_size
        self.info_width = info_width

        self.screen_width = (game_grid.width+info_width)*unit_size
        self.screen_height = game_grid.height*unit_size
        self.game_width = game_grid.width*unit_size
        self.game_height = self.screen_height

        self.screen = pygame.display.set_mode((self.screen_width,self.screen_height))


    def draw(self, game_grid):
        # get the game grid to be drawn this iteration
        # and draw it
        grid_to_draw = game_grid.list()
        grid_surf = pygame.Surface((self.game_width,self.game_height))
        unit_square = pygame.Surface((self.unit_size,self.unit_size))

        # define a single unit_square and fill the game surface with grid unit_squares
        for x in range(len(grid_to_draw[0])):
            for y in range(len(grid_to_draw)):
                if grid_to_draw[y][x]:
                    unit_square.fill(COLOURS[grid_to_draw[y][x]])
                    pygame.draw.rect(unit_square, COLOURS[0], unit_square.get_rect(), width=1)
                    grid_surf.blit(unit_square, (x*self.unit_size, y*self.unit_size))

        # draw the outline
        pygame.draw.rect(grid_surf, (255,255,255),grid_surf.get_rect(), width=1)

        next_surf = pygame.Surface((4*self.unit_size, 4*self.unit_size))
        next_matrix = game_grid.next_shape.list(0)
        for x in range(len(next_matrix[0])):
            for y in range(len(next_matrix)):
                unit_square.fill(COLOURS[next_matrix[y][x]])
                pygame.draw.rect(unit_square, COLOURS[0], unit_square.get_rect(), width=1)
                next_surf.blit(unit_square, (x*self.unit_size, y*self.unit_size))

        screen_surf = pygame.Surface((self.screen_width, self.screen_height))
        screen_surf.blit(grid_surf, (self.info_width*self.unit_size,0))
        screen_surf.blit(next_surf, (int(self.unit_size * (self.info_width - len(next_matrix[0]))/2),self.unit_size))

        # draw the grid and then flip it because we use inverted coords
        self.screen.blit(screen_surf, screen_surf.get_rect())

        # show the updated screen
        pygame.display.flip()

