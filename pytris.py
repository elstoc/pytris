import pygame
from PtGame import PtGame

pygame.init()
pygame.key.set_repeat(200, 150)

game = PtGame()
score = game.play()

print("You scored ", score)
