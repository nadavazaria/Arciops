import pygame
import constants
from images import btn_green_1,btn_red_1,background_image
from button import Button
import random
pygame.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))
run = True 

button_pos = ()



def merchent(player,level):
    coins = player.coins
    cost_modifier = level*1.5//1 
    roll = random.random()
    
    while run:
        screen.blit()
        if roll > 0.2:
            pass
        elif roll >= 0.4:
            pass
        elif roll >= 0.6:
            pass
        else:

        # pygame.display.update()
