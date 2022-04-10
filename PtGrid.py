from functools import reduce
import copy
from PtBlockFactory import PtBlockFactory

class PtGrid:
    """The pytris game grid (default/minimum 10x20; maximum 50x50)"""
    
    def __init__(self, width=10, height=20):
        self.bf = PtBlockFactory()

        self.width = min(max(10, width),50)
        self.height = min(max(20, height),50)

        self.active_grid = [[0 for x in range(self.width)] for y in range(self.height)]

        self.next_block = self.bf.new_block()
        self.new_block()
        self.draw_grid = self.superpose_grids()

    def new_block(self):
        self.curr_block = self.next_block
        self.posx = int(self.width/2) - int(self.curr_block.width/2)
        self.posy = self.height
        self.next_block = self.bf.new_block()
        return self.curr_block

    def move_left(self):
        self.posx -= 1
        self.draw_grid = self.superpose_grids()

    def move_right(self):
        self.posx += 1
        self.draw_grid = self.superpose_grids()

    def move_down(self):
        self.posy -= 1
        if self.posy < 0:
            self.posy = 0
            self.active_grid = self.superpose_grids()
            self.draw_grid = self.active_grid
            self.new_block()
        else:
            self.draw_grid = self.superpose_grids()

    def superpose_grids(self):
        # create a new grid with same dimensions as game_grid
        target_grid = copy.deepcopy(self.active_grid)

        # place the contents of shape_grid into game_grid
        blockheight = len(self.curr_block.get_block_array())
        blockwidth = len(self.curr_block.get_block_array()[0])

        for y in range(blockheight):
            for x in range(blockwidth):
                if( self.posy+y <= self.height-1 
                        and self.posx+x <= self.width-1
                        and self.curr_block.get_block_array()[y][x]):
                    target_grid[self.posy+y][self.posx+x] = self.curr_block.get_block_array()[y][x]

        return target_grid

    def get_grid_array(self):
        return self.active_grid

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '\n'.join([
            reduce(lambda x,y: x + str(y), x, '') 
                for x in self.grid])


