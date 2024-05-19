import constants
import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self,x,y,item_type,animation_list,dummy_item=False):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = animation_list
        self.item_type = item_type #it is numbers starting from 0
        self.timer = pygame.time.get_ticks()
        self.frame_index = 0
        self.image = animation_list[self.item_type][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.dummy_item = dummy_item

    def update(self,screen_scroll,player):
        """move reletive to camra"""
        if not self.dummy_item:
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]
        
        """check if colected by the player"""
        
        if self.rect.colliderect(player.rect):
             """check what was collected"""
             if self.item_type == constants.COIN:
                player.coins += 1
                self.kill()
                                
             elif self.item_type == constants.POTION_RED:
                player.health += 50 
                if player.health > 100:
                    player.health = 100
                self.kill()
                
                
        
        animation_cooldown = 150
        if self.frame_index >= (len(self.animation_list[self.item_type])-1):
            self.frame_index = 0
            
        self.image = self.animation_list[self.item_type][self.frame_index]

        if pygame.time.get_ticks() - self.timer > animation_cooldown:
                self.frame_index += 1
                self.timer = pygame.time.get_ticks()
    def draw(self,surface):
        surface.blit(self.image,self.rect.center)