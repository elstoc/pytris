"""constants for use in the pytris game"""
from pygame.locals import *

COLOURS = [
        (0,0,0),
        (255,0,0),
        (0,255,0),
        (0,0,255),
        (255,255,0),
        (255,0,255),
        (0,255,255),
        ]

WHITE = (255,255,255)
BLACK = (0,0,0)

QUIT = -2
PAUSE = -1
TICK = 0
MV_DOWN = 1
MV_LEFT = 2
MV_RIGHT = 3
MV_ROTATE = 4
MV_DROP = 5

KEY_EVENTS = { K_q: QUIT,
               K_p: PAUSE,
               K_RIGHT: MV_RIGHT,
               K_LEFT: MV_LEFT,
               K_DOWN: MV_DOWN,
               K_UP: MV_ROTATE,
               K_SPACE: MV_DROP }
