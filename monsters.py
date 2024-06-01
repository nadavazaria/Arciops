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
        self.collision_left = False
        self.collision_top = False
        self.collision_right = False
        self.collision_bottom = False
        self.hit = False
        self.stunned = False
        self.chase = False
        self.chase_clooldown = 0
        self.speciel = ticks()
        self.exp_value = exp_value
        self.damage = damage
        if self.char_type in boss_list:
            self.stun_duration = 30
        else:
            self.stun_duration = 100

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
            fireball = None
            fireball_cooldown = 500

            self.mob_dx =0
            self.mob_dy =0


            if ticks() - self.last_hit < self.stun_duration:
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
                if self.rect.centerx > player.rect.centerx  and self.health > 0:
                    self.mob_dx = -self.speed
                if self.rect.centerx < player.rect.centerx and self.health > 0:
                    self.mob_dx = self.speed
                if self.rect.centerx <= player.rect.centerx + 1 and self.rect.centerx >= player.rect.centerx - 1:
                    self.mob_dx = 0
                
                if self.rect.centery > player.rect.centery and self.health > 0:
                    self.mob_dy = -self.speed
                if self.rect.centery < player.rect.centery and self.health > 0:
                    self.mob_dy = self.speed
                
            if not self.stunned:
                self.move(obstacle_tiles)

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
                duration = 2500
                self.damage = 20
                now = ticks()
                if now - self.speciel > 4000:
                    self.speciel = now + duration
                    self.special_fx.play()
                    self.speed = 6
                                   
                if self.speciel - now < 0:
                    self.speed = 3


                
                """do the special thing with animation change using the special timer """
            return fireball
        return None

    def move(self,obstacle_tiles):
        
        if (self.mob_dx == 0 and self.mob_dy == 0):
            self.action = "idle" 
        else:
            self.action = "runing"
        self.update_action(self.action)

        if (self.mob_dx > 0):
            self.flip = False
        if (self.mob_dx < 0):
            self.flip = True

        if self.mob_dx != 0 and self.mob_dy != 0:
            self.mob_dx = self.mob_dx * math.sqrt(2)/2  
            self.mob_dy = self.mob_dy * math.sqrt(2)/2  

        """check for collision with walls in x axis"""
        
        self.rect.x += self.mob_dx
      
        for wall in obstacle_tiles:
            if wall[1].colliderect(self.rect):
                """chack where the monster is moving"""
                if  self.mob_dx > 0:
                    self.rect.right = wall[1].left
                    self.collision_right = True
                if self.mob_dx < 0:
                    self.rect.left = wall[1].right
                    self.collision_left = True
                """try to move dowm """

        self.rect.y += self.mob_dy
     
        for wall in obstacle_tiles:
            if wall[1].colliderect(self.rect):
                """chack where the mpnster is moving"""
                if  self.mob_dy > 0:
                    self.rect.bottom = wall[1].top
                    self.collision_bottom = True
                    
                    
                if self.mob_dy < 0:
                    self.rect.top = wall[1].bottom
                    self.collision_top = True
                    
                
                    """try to move up """
        # if self.collision_bottom:
        #     print ("collision_bottom")
        # if self.collision_top:
        #     print ("collision_top")
        # if self.collision_left:
        #     print ("collision_left")
        # if self.collision_right:
        #     print ("collision_right")
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

        if ticks() - self.last_spawn > self.spawn_delay and self.dist_from_player < 400:
            self.stunned = True
            if self.spawned_mob in [constants.NECROMANCER,constants.GOBLIN_SHAMAN]:
                new_monster = Spawner(self.rect.centerx,self.rect.centery,400,self.mob_animations,self.spawned_mob,[self.hit_fx,monster_death_fx,summon_fx],3,5,5000,constants.SKELETON)
            elif self.spawned_mob == constants.CHORT:    
                new_monster = Monster(self.rect.centerx,self.rect.centery,1200,self.mob_animations,self.spawned_mob,[self.hit_fx,self.death_fx],4,25)
            else:    
                new_monster = Monster(self.rect.centerx,self.rect.centery,250,self.mob_animations,self.spawned_mob,[self.hit_fx,self.death_fx],3,10)
            self.special_fx.play()
            self.last_spawn = ticks()

        return new_monster
    
        
