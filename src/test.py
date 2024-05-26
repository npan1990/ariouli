import pygame
import time

pygame.init()

while True:
	time.sleep(0.5)
	keys = pygame.key.get_pressed()
	print(keys)
