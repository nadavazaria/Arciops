import pygame
import constants
from character import Player
from items import Item ,Door
from monsters import Monster,Spawner
from images import door_closed,door_open

# class Door():
#     def __init__(self,x,y):
#         self.open = False
#         self.images = [door_closed,door_open]
#         self.image = self.images[0]
#         self.rect = self.rect = pygame.Rect(x,y,constants.TILE_SIZE,constants.TILE_SIZE)
#         self.rect.center = (x,y)
        
        
#     def update(self,player,screen_scroll):
        
#         self.rect.x += screen_scroll[0]
#         self.rect.y += screen_scroll[1]
#         print(self.rect.x)
#         if self.open:
#             return False
#         if not self.open and player.keys > 0:
#             self.open = True
#             player.keys -= 1
#             self.image = self.images[1]
#             print("opened the door")
            
#         if not self.open:
            
#             return True
#     def draw(self,surface):
#         surface.blit(self.image,(self.rect.centerx -24,self.rect.centery -24))
#         pygame.draw.rect(surface,constants.RED,self.rect)

class World():
    def __init__(self):
        self.map_tiles = []
        self.obstacle_tiles = []
        self.exit_tile = None
        self.item_list = []
        self.enemy_list = []
        self.spawner_list = []
        self.player = None
        self.ticks = pygame.time.get_ticks() 
        self.list_of_doors = [] 
        
    def process_data(self,data,tile_list,item_image_list,mob_animations,surface,player,sound_effects,level):
        self.item_image_list = item_image_list
        self.mob_animations = mob_animations
        self.level_length = len(data)
        self.sound_effects = sound_effects
        """go thrugh the data that is a 150X150 matrix"""
        self.player = player 
        player_m_fx =[self.sound_effects["player_m_hit_fx"],self.sound_effects["player_m_death_fx"]]
        player_f_fx = [self.sound_effects["player_f_hit_fx"],self.sound_effects["player_f_death_fx"]]
        standard_monster_fx = [self.sound_effects["hit_fx"],self.sound_effects["monster_death_fx"]]
        ogre_fx = [self.sound_effects["hit_fx"],self.sound_effects["ogre_death_fx"],self.sound_effects["ogre_roar_fx"]]
        big_demon_fx = [self.sound_effects["hit_fx"],self.sound_effects["demon_death_fx"],self.sound_effects["fire_fx"]]
        big_zombie_fx = [self.sound_effects["hit_fx"],self.sound_effects["zombie_growl_fx"],self.sound_effects["magical_spell_fx"]]
        spawner_1_fx = [self.sound_effects["hit_fx"],self.sound_effects["monster_death_fx"],self.sound_effects["spawn_fx"]]
        spawner_2_fx = [self.sound_effects["hit_fx"],self.sound_effects["monster_death_fx"],self.sound_effects["summon_fx"]]

        obstacle_list = [constants.WALL,constants.WALL_OOZE,constants.LAVA_WALL,constants.MOSS_WALL,constants.FLAG_BLUE,constants.FLAG_RED,constants.FLAG_GREEN,constants.FLAG_YELLOW,constants.WALL_LAVA_BRIGHT,constants.WALL_LAVA_DUN,constants.WALL_LAVA_POOL]
        boss_list = [constants.TILE_BIG_DEMON,constants.TILE_BIG_ZOMBIE,constants.TILE_OGRE]
        placeholder_tile = 0
        if level >= 9:
            placeholder_tile = 64
        for y,row in enumerate(data):
        
            for x,tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x*constants.TILE_SIZE 
                image_y = y*constants.TILE_SIZE  
                image_rect.center = (image_x ,image_y )
                tile_data = [image,image_rect,image_x,image_y,tile]
                """add to the main list of world tiles """
                if tile in obstacle_list:
                    self.obstacle_tiles.append(tile_data)

                elif tile == constants.EXIT or tile == constants.EXIT_2:
                    self.exit_tile = tile_data  
                    
                elif tile == constants.TILE_DOOR:
                    door = Door(image_x,image_y,[door_closed,door_open])
                    self.list_of_doors.append(door)
                    tile_data[0] = tile_list[placeholder_tile]  
                    
                    

                elif tile == constants.TILE_COIN:
                    coin = Item(image_x  ,image_y  ,constants.COIN,self.item_image_list)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.item_list.append(coin)
                elif tile == constants.TILE_POTION_RED:
                    red_potion = Item(image_x,image_y ,constants.POTION_RED,self.item_image_list)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.item_list.append(red_potion)
                elif tile == constants.TILE_POTION_BLUE:
                    blue_potion = Item(image_x,image_y ,constants.POTION_BLUE,self.item_image_list)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.item_list.append(blue_potion)
                elif tile == constants.TILE_KEY:
                    key = Item(image_x,image_y ,constants.KEY,self.item_image_list)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.item_list.append(key)


                elif tile == constants.TILE_GOBLIN:
                    goblin =  Monster(image_x,image_y,250,self.mob_animations,constants.GOBLIN,standard_monster_fx,3,5)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.enemy_list.append(goblin)
                elif tile == constants.TILE_SKELETON:
                    skeleton =  Monster(image_x ,image_y,100,self.mob_animations,constants.SKELETON,standard_monster_fx,3,3)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.enemy_list.append(skeleton)
                elif tile == constants.TILE_MUDDY:
                    muddy =  Monster(image_x,image_y ,200,self.mob_animations,constants.MUDDY,standard_monster_fx,2,4)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.enemy_list.append(muddy)
                elif tile == constants.TILE_TINY_ZOMBIE:
                    tiny_zombie =  Monster(image_x,image_y,150,self.mob_animations,constants.TINY_ZOMBIE,standard_monster_fx,3,3)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.enemy_list.append(tiny_zombie)
               
                elif tile == constants.TILE_DOCC:
                    docc = Monster(image_x, image_y, 600, self.mob_animations, constants.DOCC, standard_monster_fx, 4,9)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.enemy_list.append(docc)


                elif tile == constants.TILE_GOBLIN_WARRIOR:
                    goblin_warrior = Monster(image_x, image_y,350, self.mob_animations, constants.GOBLIN_WARRIOR, standard_monster_fx, 3,7,15)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.enemy_list.append(goblin_warrior)

                elif tile == constants.TILE_GOBLIN_SHAMAN:
                    goblin_shaman = Spawner(image_x, image_y, 350, self.mob_animations, constants.GOBLIN_SHAMAN, spawner_1_fx, 2,9,7000,constants.GOBLIN,12)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.enemy_list.append(goblin_shaman)
                    self.spawner_list.append(goblin_shaman)
 
                elif tile == constants.TILE_NECROMANCER:
                    necromancer = Spawner(image_x, image_y, 700, self.mob_animations, constants.NECROMANCER, spawner_2_fx, 1,12,6000,constants.SWAMPY,12)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.enemy_list.append(necromancer)
                    self.spawner_list.append(necromancer)

                elif tile == constants.TILE_PUMPKIN:
                    pumpkin = Monster(image_x, image_y, 800, self.mob_animations, constants.PUMPKIN, standard_monster_fx, 4,12,13)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.enemy_list.append(pumpkin)

                elif tile == constants.TILE_SLUG:
                    slug = Monster(image_x, image_y, 900, self.mob_animations, constants.SLUG, standard_monster_fx, 2,12,15)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.enemy_list.append(slug)

                elif tile == constants.TILE_SWAMPY:
                    swampy = Monster(image_x, image_y, 450, self.mob_animations, constants.SWAMPY, standard_monster_fx, 2,9,15)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.enemy_list.append(swampy)
                    
                elif tile == constants.TILE_IMP:
                    imp =  Monster(image_x,image_y,900,self.mob_animations,constants.IMP,standard_monster_fx,6,14,12)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.enemy_list.append(imp)

                elif tile == constants.TILE_WOGOL:
                    wogol = Monster(image_x, image_y, 1200, self.mob_animations, constants.WOGOL, standard_monster_fx, 5,16,15)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.enemy_list.append(wogol)


                elif tile == constants.TILE_CHORT:
                    chort = Monster(image_x, image_y, 1700, self.mob_animations, constants.CHORT, standard_monster_fx, 5,18,15)
                    tile_data[0] = tile_list[placeholder_tile]
                    self.enemy_list.append(chort)



                elif tile in boss_list:
                    if tile == constants.TILE_BIG_DEMON:
                        big_demon =  Spawner(image_x,image_y,40000,self.mob_animations,constants.BIG_DEMON,big_demon_fx,3,500,2000,constants.CHORT,25)
                        tile_data[0] = tile_list[placeholder_tile]
                        self.enemy_list.append(big_demon)
                        self.spawner_list.append(big_demon)
                    if tile == constants.TILE_BIG_ZOMBIE:
                        big_zombie =  Spawner(image_x,image_y,15000,self.mob_animations,constants.BIG_ZOMBIE,big_zombie_fx,3,300,8000,constants.NECROMANCER,20)
                        tile_data[0] = tile_list[placeholder_tile]
                        self.enemy_list.append(big_zombie)
                        self.spawner_list.append(big_zombie)
                    if tile == constants.TILE_OGRE:
                        ogre =  Monster(image_x,image_y,6000,self.mob_animations,constants.OGRE,ogre_fx,4,150,20)
                        tile_data[0] = tile_list[placeholder_tile]
                        self.enemy_list.append(ogre)
                        #this  is specific for player charecters 
             
               
                elif tile == constants.TILE_ELF:
                    if self.player:
                        self.player.rect.centerx = image_x
                        self.player.rect.centery = image_y
                        tile_data[0] = tile_list[placeholder_tile]
                    # elif tile == constants.TILE_KNIGHT:
                    #     self.player = Player(image_x,image_y,100,mob_animations,constants.KNIGHT,player_m_fx,5)
                    #     self.player.make_the_difference(130,85,4,35,40)
                    #     tile_data[0] = tile_list[placeholder_tile]
                    else :
                        self.player = Player(image_x,image_y,100,mob_animations,constants.ELF,player_m_fx,5)
                        tile_data[0] = tile_list[placeholder_tile]
                    # elif tile == constants.TILE_ELF_F:
                    #     self.player = Player(image_x,image_y,100,mob_animations,constants.ELF_F,player_f_fx,5)
                    #     self.player.make_the_difference(100,120,6,15,60)
                    #     tile_data[0] = tile_list[0]
                        
                if tile >= 0: 
                    self.map_tiles.append(tile_data)
                    

    def draw(self,surface):
        for tile in self.map_tiles:
            surface.blit(tile[0],(tile[2] -24,tile[3]-24))

    def update(self,screen_scroll):
        
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0] 
            tile[3] += screen_scroll[1] 
            tile[1].center = (tile[2],tile[3])
            
    def spawn_enemy(self):
        enemy = Player(self.player.centerx + 50,self.player.centery + 50,100,self.mob_animations,constants.DOCC,)
        self.enemy_list.append()