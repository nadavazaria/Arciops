import pygame

pygame.init()
"""the font """
font = pygame.font.Font("assets/fonts/AtariClassic.ttf",20)


class DamageText(pygame.sprite.Sprite):
    def __init__(self,x,y,damage,color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage,True,color)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.float_speed = - 3
        self.self_destruct = 200
        self.time_of_birth = pygame.time.get_ticks()

    def update(self,screen_scroll):
    
        self.rect.centery += self.float_speed
        

        if  pygame.time.get_ticks() - self.time_of_birth >= self.self_destruct:
            self.kill()

    