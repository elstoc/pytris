from PtShape import PtShape
from functools import reduce
import random
import numpy as np

class PtShapeFactory:
    """store all possible shape formations/rotations and 
       deliver new PtShape objects to the game when requested"""

    def __init__(self):
        """store all possible _base_forms in an array
           each within different sized squares for a reasonable
           centre of rotation"""

        # first define all the basic forms
        self._base_forms = []

        self._base_forms.append([[1,1],
                                 [1,1]])

        self._base_forms.append([[0,0,0],
                                 [1,1,1],
                                 [0,1,0]])

        self._base_forms.append([[0,0,0],
                                 [1,1,0],
                                 [0,1,1]])

        self._base_forms.append([[0,0,0],
                                 [0,1,1],
                                 [1,1,0]])

        self._base_forms.append([[0,0,0,0],
                                 [1,1,1,1],
                                 [0,0,0,0],
                                 [0,0,0,0]])

        self._base_forms.append([[0,0,0,0],
                                 [0,1,1,0],
                                 [0,1,0,0],
                                 [0,1,0,0]])

        self._base_forms.append([[0,0,0,0],
                                 [0,1,1,0],
                                 [0,1,0,0],
                                 [0,1,0,0]])

        self._shape_variants = []

        # now create a list of all rotational shape variants
        # increment rotation to rotate by 90deg clockwise
        for form in self._base_forms:
            variants = []
            for i in range(4):
                #rotate the form
                variant = np.rot90(form, i).tolist()

                # remove any empty rows
                for j in reversed(range(len(variant))):
                    if not any(variant[j]):
                        del variant[j]

                variants.append(variant)

            self._shape_variants.append(variants)

        # initialise the form history
        # avoid the "S" and "Z" shapes to start
        self._form_hist = [2,3,2,3]

    def new_shape(self):
        """return a pseudo-random shape to the caller
           4 piece history with 4 rolls
           see https://simon.lc/the-history-of-tetris-randomizers"""
        form = 0
        for i in range(4):
            # four attempts to choose a shape that doesn't appear in the history
            # if the first three attempts fail always choose the fourth shape
            form = random.randrange(len(self._base_forms))
            if form not in self._form_hist: break
        del self._form_hist[0]
        self._form_hist.append(form)

        shape =  PtShape(self._shape_variants[form])
        return shape

