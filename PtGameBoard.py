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

class PtGameBoard:
    """The pytris game grid (default/minimum 10x20; maximum 50x50)"""
    
    def __init__(self, width=10, height=20):
        self.sfact = PtShapeFactory()

        self.width = min(max(10, width),50)
        self.height = min(max(20, height),50)

        self.grid = [[0 for x in range(self.width)] for y in range(self.height)]

        self.next_shape = self.sfact.new_shape()
        self.new_shape()

    def new_shape(self):
        self.curr_shape = self.next_shape
        self.curr_shape.posx = int(self.width/2) - int(self.curr_shape.width/2)
        self.curr_shape.posy = 1 - self.curr_shape.height
        self.next_shape = self.sfact.new_shape()

    def freeze_shape(self):
        """freeze shape to grid"""
        self.grid = self.superpose_shape(self.curr_shape)
        
    def remove_rows(self):
        """remove completed rows"""
        removed_rows = 0
        for y in range(self.height):
            if (all(self.grid[y])):
                    removed_rows +=1
                    del self.grid[y]
                    self.grid.insert(0,[0 for x in range(self.width)])

        return removed_rows

    def move_shape(self, req_movement):
        """move a shape on the grid
        return True if the last move succeeded"""
        extra_move = extra_move_count = 0
        num_moves = 0

        # the movement passed to the shape will never be MV_DROP
        # but merely repeated MV_DOWNs
        shape_move = MV_DOWN if req_movement == MV_DROP else req_movement

        try_shape = copy.deepcopy(self.curr_shape)
        while True:
            try:
                try_shape.move(extra_move if extra_move else shape_move)
                self.superpose_shape(try_shape)
            except Exception as e:
                if (req_movement == MV_ROTATE):
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
                if(req_movement == MV_DROP):
                    # for MV_DROP, keep repeating down moves
                    # only returning on the final (failing) movement
                    try_shape = copy.deepcopy(self.curr_shape)
                    num_moves += 1
                else:
                    return num_moves + 1

    def superpose_shape(self, shape):
        """return a matrix that superposes the shape on the game grid
           error if overlaps are found"""
        # create a new grid with same dimensions as game_grid
        grid_out = copy.deepcopy(self.grid)

        # attempt to place the shape on the grid
        # error if shape overlaps a populated square or is off grid
        for y in range(shape.height):
            for x in range(shape.width):
                if(shape.list()[y][x]):
                    if (shape.posy + y >= self.height):
                        raise PtOffGridBottom
                    elif (shape.posx + x < 0):
                        raise PtOffGridLeft
                    elif (shape.posx + x > self.width - 1):
                        raise PtOffGridRight
                    elif (shape.posy + y >= 0
                            and grid_out[shape.posy+y][shape.posx+x]):
                        if (x < shape.width/2):
                            raise PtOverlapLeft
                        elif (x > shape.width/2):
                            raise PtOverlapRight
                        else:
                            raise PtOverlapBottom

                    if (shape.posy + y >= 0):   # ignore squares above the top of the grid
                        grid_out[shape.posy+y][shape.posx+x] = shape.list()[y][x]

        return grid_out

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


