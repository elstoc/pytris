from PtBlock import PtBlock
from functools import reduce
import random
import numpy as np

class PtBlockFactory:
    """store all possible block formations/rotations and 
       deliver new PtBlock objects to the game when requested"""

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

        self._base_forms.append([[0,1,0,0],
                                 [0,1,0,0],
                                 [0,1,0,0],
                                 [0,1,0,0]])

        self._base_forms.append([[0,0,0,0],
                                 [0,1,1,0],
                                 [0,1,0,0],
                                 [0,1,0,0]])

        self._base_forms.append([[0,0,0,0],
                                 [0,1,1,0],
                                 [0,0,1,0],
                                 [0,0,1,0]])

        self._block_variants = []

        # now create a list of all rotational block variants
        # increment rotation to rotate by 90deg clockwise
        for form in self._base_forms:
            variants = []
            for i in range(4):
                #rotate the form
                variant = np.rot90(form, 3-i).tolist()

                # remove any empty rows
                for j in reversed(range(len(variant))):
                    if not any(variant[j]):
                        del variant[j]

                variants.append(variant)

            self._block_variants.append(variants)

    def new_block(self):
        """return a random block to the caller"""
        num_forms = len(self._base_forms)
        form = random.randrange(num_forms)
        block =  PtBlock(self._block_variants[form])
        return block

