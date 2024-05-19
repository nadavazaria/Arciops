import pygame
import constants



class Player:
    def __init__(self,x,y,health,mob_animations,char_type):
        self.char_type = char_type
        self.animation_list = mob_animations[self.char_type]
        self.action = "idle"
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.health = health
        self.alive = True
        self.image = self.animation_list[0][self.frame_index]
        self.rect = pygame.Rect(0,0,constants.TILE_SIZE,constants.TILE_SIZE) 
        self.rect.center = (x,y)
        self.flip = False
        self.coins = 0

    def update(self): 
        """am i alive ?"""
        if self.health <= 0:
            self.health = 0
            self.alive = False

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
        if self.char_type == constants.ELF:
            surface.blit(fliped_image,(self.rect.x,self.rect.y - 40))
        else:    
            surface.blit(fliped_image,self.rect)

        pygame.draw.rect(surface,constants.PINK,self.rect,1)

    def update_action(self,new_action):
        if self.action != new_action:
            self.action = new_action 
            self.frame_index = 0

    def enemy_movement(self,screen_scroll):
        """move mobs reletive to camra"""
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

    def move(self,dx,dy):
        screen_scroll = [0,0]
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

        """scroll update relevent only for the player"""
        if self.char_type == constants.ELF:

            if self.rect.right > constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD:
                screen_scroll[0] = constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD - self.rect.right
                self.rect.right = constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD
            if self.rect.left < constants.SCROLL_THRESHOLD:
                screen_scroll[0] = constants.SCROLL_THRESHOLD - self.rect.left
                self.rect.left = constants.SCROLL_THRESHOLD

                
            """fix this it sucks !!"""
            
            if self.rect.top <   constants.SCROLL_THRESHOLD:
                screen_scroll[1] =  constants.SCROLL_THRESHOLD - self.rect.top
                self.rect.top = constants.SCROLL_THRESHOLD 
            if self.rect.bottom > constants.SCREEN_HEIGHT - constants.SCROLL_THRESHOLD :
                screen_scroll[1] = constants.SCREEN_HEIGHT - constants.SCROLL_THRESHOLD - self.rect.bottom
                self.rect.bottom = constants.SCREEN_HEIGHT - constants.SCROLL_THRESHOLD   

            # print(screen_scroll)

        return screen_scroll
    

    # def killed(self):
    #     if self.char_type != constants.ELF:
            