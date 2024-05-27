import pygame
import constants
import math
from weapon import Fireball
from sound_fx import summon_fx,monster_death_fx


player_charecters = [0,13,10]
boss_list = [7,15,6]
long_mob_list = [constants.GOBLIN_SHAMAN,constants.GOBLIN_WARRIOR,constants.PUMPKIN,constants.CHORT,constants.WOGOL]
ticks = pygame.time.get_ticks
class Monster:
    def __init__(self,x,y,health,mob_animations,char_type,sound_effect,speed,exp_value,damage = 10):
        self.char_type = char_type #
        self.animation_list = mob_animations[self.char_type]#
        self.action = "idle"#
        self.frame_index = 0#
        self.update_time = ticks()#
        self.last_hit = ticks()#
        self.alive = True#
        self.image = self.animation_list[0][self.frame_index]#
        self.flip = False#
        self.hit_fx = sound_effect[0]#
        self.death_fx = sound_effect[1]#
        self.speed = speed#
        self.health = health#
        self.hit = False
        self.stunned = False
        self.chase = False
        self.chase_clooldown = 0
        self.speciel = ticks()
        self.exp_value = exp_value
        self.damage = damage

        if self.char_type in boss_list:    
            self.rect = pygame.Rect(0,0,constants.TILE_SIZE*2,constants.TILE_SIZE*2) 
            self.special_fx = sound_effect[2]
        elif self.char_type in long_mob_list:
            self.rect = pygame.Rect(0,0,constants.TILE_SIZE,constants.TILE_SIZE*1.2)
        else:
            self.rect = pygame.Rect(0,0,constants.TILE_SIZE*0.9,constants.TILE_SIZE*0.9) 
        self.rect.center = (x,y)


    def update(self): 
        """am i alive ?"""
       
        if self.alive:   
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
            
            if ticks() - self.update_time > animation_cooldown:
                self.frame_index += 1
                self.update_time = ticks()
            if self.frame_index >= len(self.animation_list[is_runing]):
                self.frame_index = 0

    def draw(self,surface):
        # pygame.draw.rect(surface,constants.RED,self.rect)
        fliped_image = pygame.transform.flip(self.image,self.flip,False)
        
        surface.blit(fliped_image,self.rect)

        pygame.draw.rect(surface,constants.PINK,self.rect,1)

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
            stun_cooldown = 100
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


class Spawner(Monster):
    def __init__(self,x,y,health,mob_animations,char_type,sound_effect,speed,exp_value,delay,spawned_mob,damage = 10):
        Monster.__init__(self,x,y,health,mob_animations,char_type,sound_effect,speed,exp_value,damage)
        ticks = pygame.time.get_ticks
        self.mob_animations = mob_animations 
        self.spawn_delay = delay
        self.spawned_mob = spawned_mob
        self.last_spawn = ticks()
        self.special_fx = sound_effect[2]
        # self.spawned_mob_fx = sound_effect[],sound_effect[3]

    def spawn(self):
        
        new_monster = None

        if ticks() - self.last_spawn > self.spawn_delay and self.dist_from_player < 600:
            self.stunned = True
            if self.spawned_mob in [constants.NECROMANCER,constants.GOBLIN_SHAMAN]:
                new_monster = Spawner(self.rect.centerx,self.rect.centery,250,self.mob_animations,self.spawned_mob,[self.hit_fx,monster_death_fx,summon_fx],3,3,4000,constants.SKELETON)
            else:    
                new_monster = Monster(self.rect.centerx,self.rect.centery,250,self.mob_animations,self.spawned_mob,[self.hit_fx,self.death_fx],3,3)
            self.special_fx.play()
            self.last_spawn = ticks()

        return new_monster
    
        
