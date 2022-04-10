from functools import reduce
from PtConsts import *
import random

class PtBlock:
    """given an initial block layout, create rotational variants
       and change the rotation when requested"""

    def __init__(self, variants):

        self._variants = variants
        self.rotation = random.randrange(4)
        self.colour = random.randrange(1, len(COLOURS))
        self.width = len(variants[0][0])
        self.posx = self.posy = 0

    def rotate(self, angle=1):
        """rotate the block clockwise by angle * 90 degrees"""
        self.rotation = (self._rotation + angle) % 4

    def list(self):
        # return the array representing the correct rotational variant
        # multiply each array element by color
        return [ [ x * self.colour for x in y ] for y in self._variants[self.rotation] ]

    def __repr__(self):
        """a representation of the shape, O represents the shape position"""
        return '\n'.join([
            reduce(lambda x,y: x + ('O' if y else ' '), x, '') 
                for x in self._variants[self.rotation]])

    def __str__(self):
        return self.__repr__()


