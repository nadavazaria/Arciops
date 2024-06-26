import pygame
import constants

pygame.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))


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


"""load door image"""
door_closed = pygame.transform.scale(pygame.image.load("assets/images/miselanious/door_closed.png").convert_alpha(), (constants.TILE_SIZE, constants.TILE_SIZE)) 
door_open = pygame.transform.scale(pygame.image.load("assets/images/miselanious/door_open.png").convert_alpha(), (constants.TILE_SIZE, constants.TILE_SIZE)) 




"""load the items"""
item_image_list = []
potion_red = scale_img(pygame.image.load("assets/images/items/potion_red.png").convert_alpha(),constants.POTION_SCALE) 
potion_blue = scale_img(pygame.image.load("assets/images/items/potion_blue.png").convert_alpha(),constants.POTION_SCALE) 
potion_yellow = scale_img(pygame.image.load("assets/images/items/potion_yellow.png").convert_alpha(),constants.POTION_SCALE) 
potion_yellow_big = scale_img(pygame.image.load("assets/images/items/potion_yellow_big.png").convert_alpha(),constants.POTION_SCALE) 

"""load coin and key animation"""
coin_amination_list = []
for i in range(4):
    coin = scale_img(pygame.image.load(f"assets/images/items/coin_f{i}.png").convert_alpha(),constants.ITEM_SCALE) 
    coin_amination_list.append(coin)
    
key_amination_list = []
for i in range(4):
    key = scale_img(pygame.image.load(f"assets/images/items/key_f{i}.png").convert_alpha(),constants.WHEAPON_SCALE) 
    key_amination_list.append(key)
    
"""add the items to the list in in a nested list format similar to the mob images"""
item_image_list.append(coin_amination_list)
item_image_list.append([potion_red])
item_image_list.append([potion_blue])
item_image_list.append([potion_yellow])
item_image_list.append([potion_yellow_big])
item_image_list.append(key_amination_list)


"""load button images"""
btn_green_1 = scale_img(pygame.image.load("assets/images/buttons/button_green_1.png").convert_alpha(),constants.BUTTON_SCALE)
btn_green_2 = scale_img(pygame.image.load("assets/images/buttons/button_green_2.png").convert_alpha(),constants.BUTTON_SCALE)
btn_green_3 = scale_img(pygame.image.load("assets/images/buttons/button_green_3.png").convert_alpha(),constants.BUTTON_SCALE)
btn_red_1 = scale_img(pygame.image.load("assets/images/buttons/button_red_1.png").convert_alpha(),constants.BUTTON_SCALE)
btn_red_2 = scale_img(pygame.image.load("assets/images/buttons/button_red_2.png").convert_alpha(),constants.BUTTON_SCALE)
btn_red_3 = scale_img(pygame.image.load("assets/images/buttons/button_red_3.png").convert_alpha(),constants.BUTTON_SCALE)
btn_settings = scale_img(pygame.image.load("assets/images/buttons/button_settings.png").convert_alpha(),constants.BUTTON_SCALE)
btn_arrow_right = scale_img(pygame.image.load("assets/images/buttons/btn_arrow_right.png").convert_alpha(),0.4)
btn_arrow_left = pygame.transform.flip(scale_img(pygame.image.load("assets/images/buttons/btn_arrow_right.png").convert_alpha(),0.4),1,0)
btn_arrow_right_hover = scale_img(pygame.image.load("assets/images/buttons/btn_arrow_right_dark.png").convert_alpha(),0.4)
btn_arrow_left_hover = pygame.transform.flip(scale_img(pygame.image.load("assets/images/buttons/btn_arrow_right_dark.png").convert_alpha(),0.4),1,0)

"""load shop images"""
speed_up_image  = pygame.image.load(f"assets/images/miselanious/speed_up.png").convert_alpha()
mp_up_image  = pygame.image.load(f"assets/images/miselanious/mp_up.png").convert_alpha()
hp_up_image  = pygame.image.load(f"assets/images/miselanious/hp_up.png").convert_alpha()
damage_up_image  = pygame.image.load(f"assets/images/miselanious/damage_up.png").convert_alpha()
att_speed_up_image  = pygame.image.load(f"assets/images/miselanious/arrow_speed_up.png").convert_alpha()
shop_item_bg =  pygame.transform.scale(pygame.image.load(f"assets/images/miselanious/shop_background.jpg").convert_alpha(),(650,50))
shop_item_bg_dark =  pygame.transform.scale(pygame.image.load(f"assets/images/miselanious/shop_background_dark.png").convert_alpha(),(650,50))



"""load weapon images"""
knife_image  = pygame.image.load(f"assets/images/weapons/knife.png").convert_alpha()
knife_throw_image  = scale_img(pygame.image.load(f"assets/images/weapons/knife_throw.png").convert_alpha(),constants.WHEAPON_SCALE)
staff_image =  scale_img(pygame.image.load(f"assets/images/weapons/staff_green.png").convert_alpha(),constants.WHEAPON_SCALE)
bow_image  = scale_img(pygame.image.load(f"assets/images/weapons/bow.png").convert_alpha(),constants.WHEAPON_SCALE)
arrow_image  = scale_img(pygame.image.load(f"assets/images/weapons/arrow.png").convert_alpha(),constants.WHEAPON_SCALE)
fireball_image = scale_img(pygame.image.load(f"assets/images/weapons/fireball.png").convert_alpha(),constants.WHEAPON_SCALE)
energy_ball_image = scale_img(pygame.image.load(f"assets/images/weapons/energy_ball.png").convert_alpha(),constants.WHEAPON_SCALE)
shuriken_image = scale_img(pygame.image.load(f"assets/images/weapons/Shuriken.png").convert_alpha(),constants.WHEAPON_SCALE)

"""load magic images"""
lightning_animation = []
for i in range(5):
    lightning = pygame.image.load(f"assets/images/weapons/lightning/lightning_{i}.png").convert_alpha()
    lightning_animation.append(lightning)

"""loading the menu images image """
reaper_image = scale_img(pygame.image.load(f"assets/images/miselanious/grim_reaper.png").convert_alpha(),2)
background_image = pygame.transform.scale(pygame.image.load(f"assets/images/miselanious/background_image.jpg").convert_alpha(),(800,600))
game_bg = pygame.transform.scale(pygame.image.load(f"assets/images/miselanious/game_bg.jpg").convert_alpha(),(800,600))
death_bg = pygame.transform.scale(pygame.image.load(f"assets/images/miselanious/death_bg.jpg").convert_alpha(),(800,600))

"""loading the mob images"""
mob_animations = []
mob_types = ["elf","goblin","imp","muddy","skeleton","tiny_zombie","big_demon","big_zombie","chort","docc","elf_f","goblin_warrior",
             'goblin_shaman',"Knight","necromancer","ogre","pumpkin","slug","swampy","wogol","wizard"]
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

"""the exports
mob_animations,
item_image_list
game_bg,
background_image,
reaper_image,
lightning_animation,
weapon_image,
arrow_image,
fireball_image,
btn_green_1,
btn_green_2,
btn_red_1,
btn_red_2
scale_img,
list_of_tiles
"""