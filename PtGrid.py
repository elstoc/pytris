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
        self.sfact = PtShapeFactory()

        self.width = min(max(10, width),50)
        self.height = min(max(20, height),50)

        self.active_grid = [[0 for x in range(self.width)] for y in range(self.height)]

        self.next_shape = self.sfact.new_shape()
        self.new_shape()

    def new_shape(self):
        self.curr_shape = self.next_shape
        self.curr_shape.posx = int(self.width/2) - int(self.curr_shape.width/2)
        self.curr_shape.posy = 1 - self.curr_shape.height
        self.next_shape = self.sfact.new_shape()
        return self.curr_shape

    def freeze_shape(self, shape):
        """freeze shape to grid
           remove completed grid rows
           create new shape"""
        self.active_grid = self.superpose_shape(shape)
        
        for y in range(self.height):
            if (all(self.active_grid[y])):
                    del self.active_grid[y]
                    self.active_grid.insert(0,[0 for x in range(self.width)])

        self.new_shape()

    def move(self, movement):
        """move a shape on the grid
        return True if the grid changed"""
        try_shape = copy.deepcopy(self.curr_shape)
        try_shape.move(movement)
        try:
            self.superpose_shape(try_shape)
        except:
            if (movement == MV_DOWN):
                self.freeze_shape(self.curr_shape)
                return True
            elif(movement == MV_ROTATE):
                # rotation may produce overlaps initially but should try some
                # move-left/move-right to resolve
                # 4x4 shapes may need to move two spaces
                # 3x3 shapes may need to move one space
                # 2x2 shapes are symmetrical so will always pass
                print("can't rotate")
                return False
            else:
                return False
        else:
            self.curr_shape = try_shape
            return True

    def superpose_shape(self, shape):
        """return a matrix that superposes the shape on the game grid
           error if overlaps are found"""
        # create a new grid with same dimensions as game_grid
        target_grid = copy.deepcopy(self.active_grid)
        shape_grid = shape.list()

        # place the contents of shape_grid into game_grid
        shapeheight = len(shape_grid)
        shapewidth = len(shape_grid[0])

        for y in range(shapeheight):
            for x in range(shapewidth):
                if(shape_grid[y][x]):
                    if (shape.posy + y >= self.height):
                        raise PtOffGridBottom
                    elif (shape.posx + x < 0):
                        raise PtOffGridLeft
                    elif (shape.posx + x > self.width - 1):
                        raise PtOffGridRight
                    elif (shape.posy + y > 0
                            and target_grid[shape.posy+y][shape.posx+x]):
                        if (x < shapewidth/2):
                            raise PtOverlapLeft
                        elif (x > shapewidth/2):
                            raise PtOverlapRight
                        else:
                            raise PtOverlapBottom

                    if (shape.posy + y >= 0):
                        target_grid[shape.posy+y][shape.posx+x] = shape_grid[y][x]

        return target_grid

    def list(self):
        """return a matrix representing the current shape
        overlaid on the current game grid"""
        return self.superpose_shape(self.curr_shape)

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return '\n'.join([
            reduce(lambda x,y: x + str(y), x, '') 
                for x in self.list()])


