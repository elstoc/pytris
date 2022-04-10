from functools import reduce
import copy
from PtShapeFactory import PtShapeFactory
from PtConsts import *

class PtOffGridRight(Exception):
    pass

class PtOffGridLeft(Exception):
    pass

class PtOffGridBottom(Exception):
    pass

class PtOverlapLeft(Exception):
    pass

class PtOverlapRight(Exception):
    pass

class PtOverlapBottom(Exception):
    pass



class PtGrid:
    """The pytris game grid (default/minimum 10x20; maximum 50x50)"""
    
    def __init__(self, width=10, height=20):
        self.bf = PtShapeFactory()

        self.width = min(max(10, width),50)
        self.height = min(max(20, height),50)

        self.active_grid = [[0 for x in range(self.width)] for y in range(self.height)]

        self.next_shape = self.bf.new_shape()
        self.new_shape()
        self.fail_down = False

    def new_shape(self):
        self.curr_shape = self.next_shape
        self.curr_shape.posx = int(self.width/2) - int(self.curr_shape.width/2)
        self.curr_shape.posy = self.height
        self.next_shape = self.bf.new_shape()
        return self.curr_shape

    def move(self, movement):
        try_shape = copy.deepcopy(self.curr_shape)
        if(movement == MV_LEFT):
            # left movement: disallow all overlaps
            try:
                try_shape.posx -= 1
                self.superpose_shape(try_shape)
            except:
                print("can't move left")
            else:
                self.curr_shape = try_shape
        elif(movement == MV_RIGHT):
            # right movement: disallow all overlaps
            try:
                try_shape.posx += 1
                self.superpose_shape(try_shape)
            except:
                print("can't move right")
            else:
                self.curr_shape = try_shape
        elif(movement == MV_DOWN):
            # down movement: disallow all overlaps
            #                freeze to grid the second time a movedown fails
            try:
                try_shape.posy -= 1
                self.superpose_shape(try_shape)
            except:
                print("can't move down")
                if(self.fail_down):
                    self.active_grid = self.superpose_shape(self.curr_shape)
                    self.new_shape()
                    self.fail_down = False
                else:
                    self.fail_down = True
            else:
                self.curr_shape = try_shape
        elif(movement == MV_ROTATE):
            # rotation may produce overlaps initially but should try some
            # move-left/move-right to resolve
            None

    def superpose_shape(self, shape):
        # create a new grid with same dimensions as game_grid
        target_grid = copy.deepcopy(self.active_grid)
        shape_grid = shape.list()

        # place the contents of shape_grid into game_grid
        shapeheight = len(shape_grid)
        shapewidth = len(shape_grid[0])

        for y in range(shapeheight):
            for x in range(shapewidth):
                if(shape_grid[y][x]):
                    if (shape.posy + y < 0):
                        raise PtOffGridBottom
                    elif (shape.posx + x < 0):
                        raise PtOffGridLeft
                    elif (shape.posx + x > self.width - 1):
                        raise PtOffGridRight
                    elif (shape.posy + y > self.height -1):
                        # not a problem but avoid out-of-range on following line
                        pass
                    elif (target_grid[shape.posy+y][shape.posx+x]):
                        if (x <= shapewidth/2):
                            raise PtOverlapLeft
                        elif (x > shapewidth/2):
                            raise PtOverlapRight
                        else:
                            raise PtOverlapBottom

                    if (shape.posy + y <= self.height -1):
                        target_grid[shape.posy+y][shape.posx+x] = shape_grid[y][x]

        return target_grid

    def list(self):
        return self.superpose_shape(self.curr_shape)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '\n'.join([
            reduce(lambda x,y: x + str(y), x, '') 
                for x in self.grid])


