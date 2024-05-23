import pygame
import constants
import math
from weapon import Fireball



player_charecters = [0,13,10]
boss_list = [7,15,6]
ticks = pygame.time.get_ticks
class Player:
    def __init__(self,x,y,health,mob_animations,char_type,sound_effect,speed):
        self.char_type = char_type
        self.animation_list = mob_animations[self.char_type]
        self.action = "idle"
        self.frame_index = 0
        self.update_time = ticks()
        self.alive = True
        self.image = self.animation_list[0][self.frame_index]
        self.flip = False
        self.coins = 0
        self.last_hit = ticks()
        self.hit = False
        self.stunned = False
        self.chase = False
        self.chase_clooldown = 0
        self.speciel = ticks()
        self.hit_fx = sound_effect[0]
        self.death_fx = sound_effect[1]
        self.speed = speed
        self.health = health
        self.mana = 100
        self.mana_regen = 0.01
        self.max_health = 100 
        self.max_mana = 100
        self.damage = 10
        self.magic_damage = 50

        if self.char_type in boss_list:
            print("fountheogre")
            self.rect = pygame.Rect(0,0,constants.TILE_SIZE*2,constants.TILE_SIZE*2) 
            self.damage = 20
            self.special_fx = sound_effect[2]
        else:
            self.rect = pygame.Rect(0,0,constants.TILE_SIZE*0.9,constants.TILE_SIZE*0.9) 
        self.rect.center = (x,y)


    def make_the_difference(self,max_health,max_mana,speed,damage,magic_damage):
        self.max_health = max_health
        self.health = max_health
        self.max_mana = max_mana
        self.mana = max_mana
        self.speed = speed
        self.damage = damage
        self.magic_damage = magic_damage
        
    def update(self): 
        """am i alive ?"""
        dmg_cooldown = 1000
        
        if ticks() - self.last_hit > dmg_cooldown and self.char_type in player_charecters:
            self.hit = False

        if self.health <= 0:
            self.health = 0
            self.alive = False

        if self.mana < self.max_mana:
            self.mana += self.mana_regen
        
        animation_cooldown = 70
        is_runing = 0
        if self.action == "idle":
            is_runing = 0 
        if self.action == "runing":
            is_runing = 1

        self.image = self.animation_list[is_runing][self.frame_index]
        
        if ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = ticks()
        if self.frame_index >= len(self.animation_list[is_runing]):
            self.frame_index = 0

    def draw(self,surface):
        # pygame.draw.rect(surface,constants.RED,self.rect)
        fliped_image = pygame.transform.flip(self.image,self.flip,False)
        
        if self.char_type in player_charecters:
            surface.blit(fliped_image,(self.rect.x,self.rect.y - 40))
        else:    
            surface.blit(fliped_image,self.rect)

        # pygame.draw.rect(surface,constants.PINK,self.rect,1)

    def update_action(self,new_action):
        if self.action != new_action:
            self.action = new_action 
            self.frame_index = 0

    # def spawn(self,x,y,amount,mob_type):


    def enemy_movement(self,player,obstacle_tiles,screen_scroll,fireball_image):
        self.dist_from_player = math.sqrt(((self.rect.centerx - player.rect.centerx)**2) + (( self.rect.centery - player.rect.centery)**2))
        self.rect.x += screen_scroll[0]
        self.rect.y += screen_scroll[1]

        """move mobs reletive to camra"""
        if self.dist_from_player < 500:
            clipped_line = ()
            stun_cooldown = 150
            fireball = None
            fireball_cooldown = 700

            self.mob_dx =0
            self.mob_dy =0





            if ticks() - self.last_hit < stun_cooldown:
                self.stunned = True
                self.action = "idle" 
            else:
                self.stunned = False
                self.action = "runing"

            line_of_sight = ((self.rect.centerx,self.rect.centery),(player.rect.centerx,player.rect.centery))
            """check if line of sight is obstructed"""
            
            for obstacle in obstacle_tiles:
                if obstacle[1].clipline(line_of_sight):
                    clipped_line = obstacle[1].clipline(line_of_sight)

            """make the chase machanic"""
            if not clipped_line:
                self.chase = True
                self.chase_clooldown = ticks() + 4000
            
            if self.chase_clooldown - ticks() < 0:
                self.chase = False
                

            if self.dist_from_player > constants.RANGE and self.chase:
                if self.rect.centerx > player.rect.centerx and self.health > 0:
                    self.mob_dx = -self.speed
                if self.rect.centerx < player.rect.centerx and self.health > 0:
                    self.mob_dx = self.speed
                
                if self.rect.centery > player.rect.centery and self.health > 0:
                    self.mob_dy = -self.speed
                if self.rect.centery < player.rect.centery and self.health > 0:
                    self.mob_dy = self.speed
                
            if not self.stunned:
                self.move(self.mob_dx,self.mob_dy,obstacle_tiles)

            """damage to player"""

            
            if self.dist_from_player < constants.ATT_RANGE and not player.hit:
                player.health -= self.damage 
                if player.health <= 0:
                    player.death_fx.play()
                else:
                    player.hit_fx.play()
                player.hit = True
                player.last_hit = ticks()


            """BOSS mechanics"""
            if self.char_type == constants.BIG_DEMON:
                if ticks() - self.speciel > fireball_cooldown:
                    self.speciel = ticks()
                    fireball = Fireball(fireball_image,self.rect.centerx,self.rect.centery,player.rect.centerx,player.rect.centery)
            if self.char_type == constants.OGRE:
                duration = 1500
                self.damage = 20
                now = ticks()
                if now - self.speciel > 4000:
                    self.speciel = now + duration
                    self.special_fx.play()
                    self.speed = 6
                                   
                    """download ogre grunt sound"""
                if self.speciel - now < 0:
                    self.speed = 3

            if self.char_type == constants.BIG_ZOMBIE:
                
                """do the special thing with animation change using the special timer """
            return fireball
        return None

    def move(self,dx,dy,obstacle_tiles,exit_tile = None):
        screen_scroll = [0,0]
        level_complete = False
        
        
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
        if self.char_type in player_charecters:
           
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

            if exit_tile[1].colliderect(self.rect):
                dist = math.sqrt(((exit_tile[1].centerx - self.rect.centerx)**2) + (( exit_tile[1].centery - self.rect.centery)**2))
                if dist < 30 and not level_complete:
                    level_complete = True
                   

        return screen_scroll,level_complete
    

    # def killed(self):
    #     if self.char_type != constants.ELF:
            