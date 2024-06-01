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

    def update(self,screen_scroll,player,heal_fx,coin_fx):
        """move reletive to camra"""
        if not self.dummy_item:
            self.rect.x += screen_scroll[0]
            self.rect.y += screen_scroll[1]
        
        """check if colected by the player"""
        
        if self.rect.colliderect(player.rect):
             """check what was collected"""
             if self.item_type == constants.COIN:
                coin_fx.play()
                player.coins += 1
                self.kill()
                                
             elif self.item_type == constants.POTION_RED:
                heal_fx.play()
                player.health += 50 
                if player.health > player.max_health:
                    player.health = player.max_health
                self.kill()

             elif self.item_type == constants.POTION_BLUE:
                heal_fx.play()
                player.mana += 50 
                if player.mana > player.max_mana:
                    player.mana = player.max_mana
                self.kill()
                
             elif self.item_type == constants.POTION_YELLOW:
                heal_fx.play()
                player.exp += 20 
                self.kill()
                
             elif self.item_type == constants.POTION_YELLOW_BIG:
                heal_fx.play()
                player.exp += 50             
                self.kill()
                
             elif self.item_type == constants.KEY:
                coin_fx.play()
                player.keys += 1             
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



class Door():
    def __init__(self,x,y,door_image):
        self.images = door_image
        self.open = False
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = (x -24,y-24)

    def update(self,screen_scroll,player):
        """move reletive to camra"""
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
    
        """check if colected by the player"""
        
        if self.rect.colliderect(player.rect):
            if not self.open:
                if player.keys > 0:    
                    self.open = True
                    player.keys -= 1
                    self.image = self.images[1]
                else:
                    """the door is very dumb and only bounces the player down"""
                    print("collision")
                    player.rect.top = self.rect.bottom 

             
        

    def draw(self,surface):
        surface.blit(self.image,self.rect.center)