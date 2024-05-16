import pygame
import constants



class Player:
    def __init__(self,x,y,animation_list):
        self.animation_list = animation_list
        self.frame_index = 0
        self.action = "idle"
        self.update_time = pygame.time.get_ticks()
        self.image = animation_list[0][self.frame_index]
        self.rect = pygame.Rect(0,0,40,40) 
        self.rect.center = (x,y)
        self.flip = False

    def update(self): 
       
        animation_cooldown = 70
        is_runing = 0
        if self.action == "idle":
            is_runing = 0 
        if self.action == "runing":
            is_runing = 1

        self.image = self.animation_list[is_runing][self.frame_index]
        
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[is_runing]):
            self.frame_index = 0

    def draw(self,surface):
        fliped_image = pygame.transform.flip(self.image,self.flip,False)

        surface.blit(fliped_image,self.rect)

        pygame.draw.rect(surface,constants.PINK,self.rect,1)

    def update_action(self,new_action):
        if self.action != new_action:
            self.action = new_action 
            self.frame_index = 0


    def move(self,dx,dy):
        if (dx == 0 and dy == 0):
            self.action = "idle" 
        else:
            self.action = "runing"
        self.update_action(self.action)

        if (dx > 0):
            self.flip = False

        if (dx < 0):
            self.flip = True
        if (dx != 0 & dy != 0):
            dx = dx * 0.71  
            dy = dy * 0.71  
        self.rect.x += dx
        self.rect.y += dy