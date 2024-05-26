import pygame
from damage_text import font
import constants

class Button():
    def __init__(self,pos,image,text_pos,text,scale_image):
        self.image = [scale_image(image[0],0.743),scale_image(image[1],0.743)]
        self.scale = scale_image
        self.rect = self.image[0].get_rect()
        self.rect.center = pos
        self.text_image = font.render(text,True,constants.BLACK)
        self.text_rect = self.text_image.get_rect() 
        self.text_rect.center = text_pos
        self.hover = False

    def draw(self,surface):
        action = False
        pos = pygame.mouse.get_pos()

        self.hover = False
        if self.rect.collidepoint(pos):
            self.hover = True
            surface.blit(self.image[0],self.rect)   
            surface.blit(self.text_image,self.text_rect)   
        else:
            surface.blit(self.image[1],self.rect)
            surface.blit(self.text_image,self.text_rect)   
        
        if self.hover and pygame.mouse.get_pressed()[0]:
            if  pygame.mouse.get_rel()[0]:
                action = True
        return action


class NoTextButton():
    def __init__(self,pos,image,scale_image,scale):
        self.image = [scale_image(image[0],scale),scale_image(image[1],scale)]
        self.scale = scale_image
        self.rect = self.image[0].get_rect()
        self.rect.center = pos
        self.hover = False
        self.last_clicked = pygame.time.get_ticks()

    def draw(self,surface):
        action = False
        pos = pygame.mouse.get_pos()

        self.hover = False
        if self.rect.collidepoint(pos):
            self.hover = True
            surface.blit(self.image[0],self.rect)   
        else:
            surface.blit(self.image[1],self.rect)
        
        if self.hover and pygame.mouse.get_pressed()[0]:
            action = True
            return action