import pygame
import math
from world import World
import constants
from character import Player
from weapon import Weapon,Lightning,Fireball
from damage_text import  DamageText,font
from items import Item
pygame.init() 
import csv
# create player


screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))

pygame.display.set_caption("Arciops")

clock = pygame.time.Clock()

"""define the game level"""
screen_scroll = [0,0]




moving_up = False
moving_down = False
moving_left = False
moving_right = False

def scale_img(image,scale):
    width = image.get_width()
    height = image.get_height()
    return pygame.transform.scale(image,(width*scale,height*scale))

"""load map tiles"""
list_of_tiles = []
for x in range(constants.TILE_TYPES):
    tile_image = pygame.image.load(f"assets/images/tiles/{x}.png").convert_alpha()
    tile_image = pygame.transform.scale(tile_image, (constants.TILE_SIZE, constants.TILE_SIZE))
    list_of_tiles.append(tile_image)



"""load the health images"""
heart_full = scale_img(pygame.image.load("assets/images/items/heart_full.png").convert_alpha(),constants.ITEM_SCALE) 
heart_half = scale_img(pygame.image.load("assets/images/items/heart_half.png").convert_alpha(),constants.ITEM_SCALE) 
heart_empty = scale_img(pygame.image.load("assets/images/items/heart_empty.png").convert_alpha(),constants.ITEM_SCALE) 

"""load the items"""
item_image_list = []
potion_red = scale_img(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(),constants.POTION_SCALE) 

"""load coin animation"""
coin_amination_list = []
for i in range(4):
    coin = scale_img(pygame.image.load(f"assets/images/items/coin_f{i}.png").convert_alpha(),constants.ITEM_SCALE) 
    coin_amination_list.append(coin)
    
"""add the items to the list in in a nested list format similar to the mob images"""
item_image_list.append(coin_amination_list)
item_image_list.append([potion_red])

"""load weapon images"""
weapon_image  = scale_img(pygame.image.load(f"assets/images/weapons/bow.png").convert_alpha(),constants.WHEAPON_SCALE)
arrow_image  = scale_img(pygame.image.load(f"assets/images/weapons/arrow.png").convert_alpha(),constants.WHEAPON_SCALE)
fireball_image = scale_img(pygame.image.load(f"assets/images/weapons/fireball.png").convert_alpha(),constants.WHEAPON_SCALE)

"""load magic images"""
lightning_animation = []
for i in range(5):
    lightning = pygame.image.load(f"assets/images/weapons/lightning/lightning_{i}.png").convert_alpha()
    lightning_animation.append(lightning)


"""loading the mob images"""
mob_animations = []
mob_types = ["elf","goblin","imp","muddy","skeleton","tiny_zombie","big_demon"]
for mob in mob_types:
    animation_list = []
    animation_types = ["idle","run"]
    for animation in animation_types:
        list_of_img = []
        for i in range(4):
            img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha()
            img = scale_img(img,constants.SCALE)
            list_of_img.append(img)
        #     print("image added")
        # print(list_of_img)
        animation_list.append(list_of_img)
    mob_animations.append(animation_list)

"""displaying game info"""
def draw_text(text,font,color,x,y):
    img = font.render(text,True,color)
    screen.blit(img,(x,y))


def draw_info():
    """draw life the numbers passed to the screen blit is the offset of the hearts"""
    pygame.draw.line(screen,constants.WHITE,(0,50),(constants.SCREEN_WIDTH,50))
    for i in range(5):
        if player.health >= ((i+1)*20):
            screen.blit(heart_full,(10 + i*50,5))
        elif player.health <= ((i+1)*20) and player.health >((i)*20):
            screen.blit(heart_half,(10 + i*50,5))
        else:screen.blit(heart_empty,(10 + i*50,5))
    """level"""
    draw_text(f"Level: {level}",font,constants.WHITE,350,20)

    """show score"""
    draw_text(f"X{player.coins}",font,constants.WHITE,695,17)




def reset_level():
    item_group.empty()
    lightning_group.empty()
    fireball_group.empty()
    damage_text_group.empty()
    arrow_group.empty()
    score_coin = Item(680,25,constants.COIN,item_image_list,True)
    item_group.add(score_coin)
    
    world_data = []
    for row in range(constants.ROWS):
        r = [-1]*constants.COLS
        world_data.append(r)
    return world_data
"""creating the initial player instance"""
def make_world_data(level): 
 
    world_data = []
    for row in range(constants.ROWS):
        r = [-1]*constants.COLS
        world_data.append(r)

    with open(f"levels/level{level}_data.csv",newline="") as csvfile:
        reader =csv.reader(csvfile,delimiter=",")
        for row_num,row in enumerate(reader):
            for col_num,tile in enumerate(row):
                if tile != "-1":
                    world_data[row_num][col_num] = int(tile)
    return world_data

"""creating all the object groups """
arrow_group = pygame.sprite.Group()
lightning_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
score_coin = Item(680,25,constants.COIN,item_image_list,True)
item_group.add(score_coin)

level = 1
world = World()
world_data = make_world_data(level)
world.process_data(world_data,list_of_tiles,item_image_list,mob_animations,screen)

player = world.player
bow = Weapon(weapon_image,arrow_image,lightning_animation,player)

for item in world.item_list:
    item_group.add(item)








"""the actual game loop"""
run = True
while run:
    """initializing the game clock and drawing the charecter and weapon"""
    clock.tick(constants.FPS)
    screen.fill(constants.BLACK)
    world.draw(screen)
    player.draw(screen)    
    for enemy in world.enemy_list:
        if enemy.alive:
            enemy.draw(screen)
    bow.draw(screen)
    draw_info()
    # score_coin.draw(screen)
   
    lightning_magic =None
    
    dx = 0
    dy = 0
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False

        """these are the actual game keys and functionalities"""        
        if event.type == pygame.KEYDOWN:
        
            if event.key == pygame.K_a:
                moving_left = True

            if event.key == pygame.K_d:
                moving_right =True
                    
            if event.key == pygame.K_s:
                moving_down = True
                    
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_0:
                player = Player(player.rect.centerx,player.rect.centery,player.health,mob_animations,0)
                bow = Weapon(weapon_image,arrow_image,lightning_animation,player)
            if event.key == pygame.K_1:
                player = Player(player.rect.centerx,player.rect.centery,player.health,mob_animations,1)
                    
            if event.key == pygame.K_2:
                player = Player(player.rect.centerx,player.rect.centery,player.health,mob_animations,2)
                    
            if event.key == pygame.K_3:
                player = Player(player.rect.centerx,player.rect.centery,player.health,mob_animations,3)
                    
            if event.key == pygame.K_4:
                player = Player(player.rect.centerx,player.rect.centery,player.health,mob_animations,4)
                    
            if event.key == pygame.K_5:
                player = Player(player.rect.centerx,player.rect.centery,player.health,mob_animations,5)
                    
            if event.key == pygame.K_6:
                player = Player(player.rect.centerx,player.rect.centery,player.health,mob_animations,6)
                bow  = Weapon(weapon_image,fireball_image,lightning_animation,player)
            if event.key == pygame.K_f:
                bow.rate_of_fire -= 50
                    
            if event.key == pygame.K_r:
                bow.rate_of_fire = 300
            
                
                

                    
        """checking for keyboard release"""
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False                

            if event.key == pygame.K_d:
                moving_right =False

            if event.key == pygame.K_s:
                moving_down = False

            if event.key == pygame.K_w:
                moving_up = False

        """ trnaslate the events into actions """
    if moving_up:
        dy = -constants.SPEED
    if moving_down:
        dy = constants.SPEED
    if moving_left:
        dx = -constants.SPEED
    if moving_right:
        dx = constants.SPEED

    
    screen_scroll,level_complete = player.move(dx,dy,world.obstacle_tiles,world.exit_tile)


    """updateing the objects and the world data """
    world.update(screen_scroll)
    player.update()

    # if level_complete:
    #     level += 1
    #     world_data = reset_level()
    #     with open(f"levels/level{level}_data.csv",newline="") as csvfile:
    #         reader =csv.reader(csvfile,delimiter=",")
    #         for row_num,row in enumerate(reader):
    #             for col_num,tile in enumerate(row):
    #                 if tile != "-1":
    #                     world_data[row_num][col_num] = int(tile)
    #     woeld = World()
    #     world.process_data(world_data,list_of_tiles,item_image_list,mob_animations,screen)

    cooldown = 500
    fireball = None        
    for enemy in world.enemy_list:
        if enemy.alive:
            fireball = enemy.enemy_movement(player,world.obstacle_tiles,screen_scroll,fireball_image)
            enemy.update()
        if fireball:    
            fireball_group.add(fireball)

            
            
    fireball_group.update(player,world.obstacle_tiles,screen_scroll)
    damage_text_group.update(screen_scroll)
    item_group.update(screen_scroll,player)   


    """this is the shooting function and the bow that fixes itself to the player"""
    arrow,lightning_magic = bow.update(player)
    if arrow:
        arrow_group.add(arrow)
    for arrow in arrow_group:
        arrow.draw(screen)
        damage_text = arrow.update(world.enemy_list,screen_scroll,world.obstacle_tiles)
        if damage_text:
            damage_text_group.add(damage_text)
    
    if lightning_magic:
        lightning_group.add(lightning_magic)
    for lightning in lightning_group:
        damage_text = lightning.update(screen,world.enemy_list,screen_scroll)
        if damage_text:
            damage_text_group.add(damage_text)
        
    """checking the damage"""
    fireball_group.draw(screen)
    damage_text_group.draw(screen)
    item_group.draw(screen)
    


    pygame.display.update()

pygame.quit()