from functools import reduce
import copy
from PtShapeFactory import PtShapeFactory
from PtConsts import *

class PtGrid:
    """The pytris game grid (default/minimum 10x20; maximum 50x50)"""
    
    def __init__(self, width=10, height=20):
        self.bf = PtShapeFactory()

        self.width = min(max(10, width),50)
        self.height = min(max(20, height),50)

        self.active_grid = [[0 for x in range(self.width)] for y in range(self.height)]

        self.next_shape = self.bf.new_shape()
        self.new_shape()
        self.draw_grid = self.superpose_grids()

    def new_shape(self):
        self.curr_shape = self.next_shape
        self.curr_shape.posx = int(self.width/2) - int(self.curr_shape.width/2)
        self.curr_shape.posy = self.height
        self.next_shape = self.bf.new_shape()
        return self.curr_shape

    def move(self, movement):
        if(movement == MV_LEFT):
            # left movement: disallow all overlaps
            self.curr_shape.posx -= 1
            self.draw_grid = self.superpose_grids()
        elif(movement == MV_RIGHT):
            # right movement: disallow all overlaps
            self.curr_shape.posx += 1
            self.draw_grid = self.superpose_grids()
        elif(movement == MV_DOWN):
            # down movement: disallow all overlaps
            #                freeze to grid the second time a movedown fails
            self.curr_shape.posy -= 1
            if self.curr_shape.posy < 0:
                self.curr_shape.posy = 0
                self.active_grid = self.superpose_grids()
                self.draw_grid = self.active_grid
                self.new_shape()
            else:
                self.draw_grid = self.superpose_grids()
        elif(movement == MV_ROTATE):
            # rotation may produce overlaps initially but should try some
            # move-left/move-right to resolve
            None

    def superpose_grids(self):
        # create a new grid with same dimensions as game_grid
        target_grid = copy.deepcopy(self.active_grid)

        # place the contents of shape_grid into game_grid
        shapeheight = len(self.curr_shape.list())
        shapewidth = len(self.curr_shape.list()[0])

        for y in range(shapeheight):
            for x in range(shapewidth):
                if( self.curr_shape.posy+y <= self.height-1 
                        and self.curr_shape.posx+x <= self.width-1
                        and self.curr_shape.list()[y][x]):
                    target_grid[self.curr_shape.posy+y][self.curr_shape.posx+x] = self.curr_shape.list()[y][x]

        return target_grid

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '\n'.join([
            reduce(lambda x,y: x + str(y), x, '') 
                for x in self.grid])


