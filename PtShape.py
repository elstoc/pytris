from functools import reduce
from PtConsts import *
import random

class PtShape:
    """given an initial shape layout, create rotational variants
       and change the rotation when requested"""

    def __init__(self, variants):

        self._variants = variants
        self.rotation = 0
        self.colour = random.randrange(1, len(COLOURS))
        self.width = self.height = len(variants[0][0])
        self.posx = self.posy = 0

    def move(self, movement):
        print(movement)
        if(movement == MV_LEFT):
            self.posx -= 1
        elif(movement == MV_RIGHT):
            self.posx += 1
        elif(movement == MV_DOWN):
            self.posy += 1
        elif(movement == MV_ROTATE):
            """rotate the shape clockwise by angle * 90 degrees"""
            self.rotation = (self.rotation + 1) % 4

    def list(self, rotation = -1):
        # return the array representing the correct rotational variant
        # multiply each array element by color
        if (rotation == -1): rotation = self.rotation
        return [ [ x * self.colour for x in y ] for y in self._variants[rotation] ]

    def __repr__(self):
        """a representation of the shape, O represents the shape position"""
        return '\n'.join([
            reduce(lambda x,y: x + ('O' if y else ' '), x, '') 
                for x in self._variants[self.rotation]])

    def __str__(self):
        return self.__repr__()


