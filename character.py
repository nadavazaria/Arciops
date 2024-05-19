import pygame
import constants
import math


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
        self.flip = False
        self.coins = 0
        if char_type == constants.BIG_DEMON:
            self.rect = pygame.Rect(0,0,constants.TILE_SIZE*2,constants.TILE_SIZE*2) 
        else:
            self.rect = pygame.Rect(0,0,constants.TILE_SIZE*0.9,constants.TILE_SIZE*0.9) 
        self.rect.center = (x,y)

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

    def enemy_movement(self,player,obstacle_tiles,screen_scroll):
        self.mob_dx =0
        self.mob_dy =0

        """move mobs reletive to camra"""
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        if self.rect.centerx > player.rect.centerx and self.health > 0:
            self.mob_dx = -constants.ENEMY_SPEED
        if self.rect.centerx < player.rect.centerx and self.health > 0:
            self.mob_dx = constants.ENEMY_SPEED
        
        if self.rect.centery > player.rect.centery and self.health > 0:
            self.mob_dy = -constants.ENEMY_SPEED
        if self.rect.centery < player.rect.centery and self.health > 0:
            self.mob_dy = constants.ENEMY_SPEED
        
        
        self.move(self.mob_dx,self.mob_dy,obstacle_tiles)


    def move(self,dx,dy,obstacle_tiles):
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
            dx = dx * math.sqrt(2)/2  
            dy = dy * math.sqrt(2)/2  

        """check for collision with walls in x axis"""
        
        self.rect.x += dx
        for wall in obstacle_tiles:
            if wall[1].colliderect(self.rect):
                """chack where the player is moving"""
                if  dx > 0:
                    self.rect.right = wall[1].left
                if dx < 0:
                    self.rect.left = wall[1].right

        self.rect.y += dy
        for wall in obstacle_tiles:
            if wall[1].colliderect(self.rect):
                """chack where the player is moving"""
                if  dy > 0:
                    self.rect.bottom = wall[1].top
                if dy < 0:
                    self.rect.top = wall[1].bottom



        """scroll update relevent only for the player"""
        if self.char_type == constants.ELF:

            if self.rect.right > constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD:
                screen_scroll[0] = constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD - self.rect.right
                self.rect.right = constants.SCREEN_WIDTH - constants.SCROLL_THRESHOLD
            if self.rect.left < constants.SCROLL_THRESHOLD:
                screen_scroll[0] = constants.SCROLL_THRESHOLD - self.rect.left
                self.rect.left = constants.SCROLL_THRESHOLD

                
            """scroll up and down """
            
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
            