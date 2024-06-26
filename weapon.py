import constants
import random
import pygame
import math
from damage_text import font,DamageText
from sound_fx import shot_fx ,fire_fx

class Weapon:
    def __init__(self,image,arrow_image,lightning_animation,player) :
        self.original_image = image
        self.arrow_image =  arrow_image
        self.lightning_animation = lightning_animation
        self.last_shot_fired = pygame.time.get_ticks()
        self.rate_of_fire = 300
        self.angle = 0
        self.shot_fx = shot_fx
        self.damage = 25
        self.image = pygame.transform.rotate(self.original_image,self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        
        self.player = player

      
    def update(self,player):
        
        arrow = None
        lightning = None
        self.rect.center = player.rect.center
        dist_x = -(player.rect.centerx - pygame.mouse.get_pos()[0])
        dist_y = (player.rect.centery -pygame.mouse.get_pos()[1]) # in pygame the y cords are fliped
        radian = math.atan2(dist_y,dist_x)
        angle = math.degrees(radian)
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image,self.angle )
        
        if pygame.mouse.get_pressed()[0] and  pygame.time.get_ticks() - self.last_shot_fired > self.rate_of_fire :  
            
            arrow = Arrow(self.arrow_image,self.rect.centerx,self.rect.centery,self.angle,player.damage )
            self.last_shot_fired = pygame.time.get_ticks()
        
        if pygame.mouse.get_pressed()[2] and  pygame.time.get_ticks() - self.last_shot_fired > self.rate_of_fire and player.mana >= 30:  
            player.mana -= 30
            lightning = Lightning(self.player,self.lightning_animation)
            self.last_shot_fired = pygame.time.get_ticks()

        return arrow,lightning

   
    def draw(self,surface):
        surface.blit(self.image,((self.rect.centerx - self.image.get_width()/2),(self.rect.centery-self.image.get_height()/2)))

class Arrow(pygame.sprite.Sprite):
    def __init__(self,image,x,y,angle,damage):
        pygame.sprite.Sprite.__init__(self)
        
        self.original_img = image
        self.speed = 10
        self.update_time = pygame.time.get_ticks()
        self.angle = angle - 90
        self.damage = damage
        self.image = pygame.transform.rotate(self.original_img,self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def draw(self,surface): 
        surface.blit(self.image,self.rect.center)
    # def draw(self,surface):
    def update(self,screen_scroll,obstacle_tiles,):
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]
        
        self.rect.centerx -= self.speed*math.sin(math.radians(self.angle))
        self.rect.centery -= self.speed*math.cos(math.radians(self.angle))

        # check if arrow is off screen 

        if (self.rect.right < 0) or self.rect.left > constants.SCREEN_WIDTH:
            self.kill()
        if (self.rect.top < 0) or self.rect.bottom > constants.SCREEN_HEIGHT:
            self.kill()
        
        """check collision"""
        for tile in obstacle_tiles:
            if tile[1].colliderect(self.rect):
                self.kill()
        
class Lightning(pygame.sprite.Sprite):
    def __init__(self,player,animation):
        pygame.sprite.Sprite.__init__(self)
        self.animation_list = animation
        self.player = player
        self.image = self.animation_list[0]
        self.rect = self.image.get_rect()
        self.damage = player.magic_damage 
        self.frame_index = 0
        self.last_fired = pygame.time.get_ticks()
        self.animation_cooldown = 70


    def update(self,surface):
        finished = False
        if self.frame_index <= (len(self.animation_list) -1):

            self.rect = self.image.get_rect(center = self.player.rect.center)
            
            start_point = self.player.rect.center 
            end_point = pygame.mouse.get_pos()
            dx = end_point[0] - start_point[0]
            """this is reversed because pygame and canvas like stuff is stupid"""
            dy = start_point[1] - end_point[1]
            self.angle = math.degrees(math.atan2(dy,dx)) + 90
            self.image = pygame.transform.rotate(self.animation_list[self.frame_index],self.angle)
            self.rect.center = (self.player.rect.centerx + 200*math.cos(math.atan2(dy,dx)),self.player.rect.centery - 200*math.sin(math.atan2(dy,dx)))
            surface.blit(self.image,self.rect.topleft)
            finished = True

        else:
            finished = False
        return finished
    


class Fireball(pygame.sprite.Sprite):
    def __init__(self,image,x,y,target_x,target_y):
        pygame.sprite.Sprite.__init__(self)
        self.original_img = image
        self.speed = 5
        self.update_time = pygame.time.get_ticks()
        dist_X =  (target_x - x)
        dist_y = -(target_y - y)
        self.angle = math.degrees(math.atan2(dist_y,dist_X))
        self.damage = 20
        self.image = pygame.transform.rotate(self.original_img,self.angle )
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)
        self.dx = math.cos(math.radians(self.angle))*self.speed
        self.dy = -math.sin(math.radians(self.angle))*self.speed
      
    def draw(self,surface): 
        surface.blit(self.image,self.rect.center)
    # def draw(self,surface):
    def update(self,player,obstacle_tiles,screen_scroll,fire_fx):
        
        self.rect.centerx += self.dx + screen_scroll[0]
        self.rect.centery += self.dy + screen_scroll[1]

        # check if arrow is off screen 

        if (self.rect.right < 0) or self.rect.left > constants.SCREEN_WIDTH:
            self.kill()
        if (self.rect.top < 0) or self.rect.bottom > constants.SCREEN_HEIGHT:
            self.kill()
        
        """check collision"""
        # for tile in obstacle_tiles:
        #     if tile[1].colliderect(self.rect):
        #         self.kill()
     
        
        if player.rect.colliderect(self.rect) and player.alive:
            fire_fx.play()
            player.health -= self.damage 
            player.hit = True
            player.last_hit = pygame.time.get_ticks()
            self.kill()
            
            
