from PtShape import PtShape
from functools import reduce
import random

class PtShapeFactory:
    """store all possible shape formations/rotations and 
       deliver new PtShape objects to the game when requested"""

    def __init__(self):
        """store four rotational variants for each shape
           designed so the bottom row always represents
           the bottom of the shape"""

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
        """return a pseudo-random shape to the caller
           4 piece history with 4 rolls
           see https://simon.lc/the-history-of-tetris-randomizers"""
        shape_no = 0
        for i in range(4):
            # four attempts to choose a shape that doesn't appear in the history
            # if the first three attempts fail always choose the fourth shape
            shape_no = random.randrange(self._num_shapes)
            if shape_no not in self._shape_hist: break
        del self._shape_hist[0]
        self._shape_hist.append(shape_no)

        return PtShape(self._shapes[shape_no])

