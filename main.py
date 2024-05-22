import pygame
from pygame import mixer
import math
from world import World
import constants
from character import Player
from weapon import Weapon,Lightning,Fireball
from damage_text import  DamageText,font
from items import Item
from button import Button
mixer.init()
pygame.init() 
import csv
# create player


screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))

pygame.display.set_caption("Arciops")

clock = pygame.time.Clock()

"""define the game level"""
level = 1
start_game = False
pause_game = False
screen_scroll = [0,0]
start_intro = True


moving_up = False
moving_down = False
moving_left = False
moving_right = False

class ScreenFade():
    def __init__(self,direction,color,speed):
        self.speed = speed
        self.color = color
        self.direction = direction
        self.fade_counter = 0
        # self.game_over_screen = False
    def fade(self):
        fading  = False
        self.fade_counter += self.speed
        if self.direction == 1:
            pygame.draw.rect(screen,self.color,(0 - self.fade_counter,0,constants.SCREEN_WIDTH//2,constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen,self.color,(constants.SCREEN_WIDTH//2 + self.fade_counter,0,constants.SCREEN_WIDTH//2,constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen,self.color,(0,0 - self.fade_counter,constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT//2))
            pygame.draw.rect(screen,self.color,(0,constants.SCREEN_HEIGHT//2 + self.fade_counter,constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT//2))
        if self.direction == 2:
            pygame.draw.rect(screen,self.color,(constants.SCREEN_WIDTH - self.fade_counter,0,constants.SCREEN_WIDTH//2,constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen,self.color,(-constants.SCREEN_WIDTH//2 + self.fade_counter,0,constants.SCREEN_WIDTH//2,constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen,self.color,(0,-constants.SCREEN_HEIGHT + self.fade_counter,constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))
            pygame.draw.rect(screen,self.color,(0,constants.SCREEN_HEIGHT - self.fade_counter,constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))
      
        if self.fade_counter > constants.SCREEN_WIDTH:
            fading = True
            self.fade_counter = constants.SCREEN_WIDTH
            
        return fading
def transition(transition):
    screen_fade = ScreenFade(transition,constants.BLACK,10)
    return screen_fade
    
def scale_img(image,scale):
    width = image.get_width()
    height = image.get_height()
    return pygame.transform.scale(image,(width*scale,height*scale))

"""load music """

pygame.mixer.music.load("assets/audio/music.wav")
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(-1,0.0,5000)

shot_fx = pygame.mixer.Sound("assets/audio/arrow_shot.mp3")
shot_fx.set_volume(0.5)
hit_fx = pygame.mixer.Sound("assets/audio/arrow_hit.wav")
monster_death_fx = pygame.mixer.Sound("assets/audio/squeek.wav")
player_m_hit_fx = pygame.mixer.Sound("assets/audio/player_m_hit.mp3")
player_m_death_fx = pygame.mixer.Sound("assets/audio/death_sound.wav")
player_f_hit_fx = pygame.mixer.Sound("assets/audio/player_f_hit.mp3")
player_f_death_fx = pygame.mixer.Sound("assets/audio/player_f_death.opus")
walk_1_fx =  pygame.mixer.Sound("assets/audio/walk_1.mp3")
walk_2_fx =  pygame.mixer.Sound("assets/audio/walk_2.mp3")
demon_death_fx = pygame.mixer.Sound("assets/audio/demon_death.mp3")
ogre_death_fx = pygame.mixer.Sound("assets/audio/ogre_death.mp3")
ogre_roar_fx = pygame.mixer.Sound("assets/audio/ogre_roar.mp3")
zombie_growl_fx = pygame.mixer.Sound("assets/audio/zombie_growl.mp3")
coin_fx = pygame.mixer.Sound("assets/audio/coin.wav")
potion_fx = pygame.mixer.Sound("assets/audio/heal.wav")
lightning_fx = pygame.mixer.Sound("assets/audio/lightning.wav")
fire_fx = pygame.mixer.Sound("assets/audio/fire.wav")
intro_fx = pygame.mixer.Sound("assets/audio/intro_heavy.opus")


sound_effects = {"shot_fx":shot_fx,"hit_fx":hit_fx,"player_m_death_fx":player_m_death_fx,
                 "player_m_death_fx":player_m_death_fx,
                 "monster_death_fx":monster_death_fx
                 ,"demon_death_fx":demon_death_fx,"ogre_death_fx":ogre_death_fx,"ogre_roar_fx":ogre_roar_fx,
                 "zombie_growl_fx":zombie_growl_fx,"coin_fx":coin_fx,"potion_fx":potion_fx,
                 "lightning_fx":lightning_fx,"fire_fx":fire_fx,"player_m_hit_fx":player_m_hit_fx,
                 "player_f_hit_fx":player_f_hit_fx,"player_f_death_fx":player_f_death_fx,"walk_1_fx":walk_1_fx,"walk_2_fx":walk_2_fx}

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

item_image_list = []
potion_blue = scale_img(pygame.image.load("assets/images/items/potion_blue.png").convert_alpha(),constants.POTION_SCALE) 

"""load coin animation"""
coin_amination_list = []
for i in range(4):
    coin = scale_img(pygame.image.load(f"assets/images/items/coin_f{i}.png").convert_alpha(),constants.ITEM_SCALE) 
    coin_amination_list.append(coin)
    
"""load button images"""
btn_green_1 = scale_img(pygame.image.load("assets/images/buttons/button_green_1.png").convert_alpha(),constants.BUTTON_SCALE)
btn_green_2 = scale_img(pygame.image.load("assets/images/buttons/button_green_2.png").convert_alpha(),constants.BUTTON_SCALE)
btn_red_1 = scale_img(pygame.image.load("assets/images/buttons/button_red_1.png").convert_alpha(),constants.BUTTON_SCALE)
btn_red_2 = scale_img(pygame.image.load("assets/images/buttons/button_red_2.png").convert_alpha(),constants.BUTTON_SCALE)
btn_settings = scale_img(pygame.image.load("assets/images/buttons/button_settings.png").convert_alpha(),constants.BUTTON_SCALE)

"""add the items to the list in in a nested list format similar to the mob images"""
item_image_list.append(coin_amination_list)
item_image_list.append([potion_red])
item_image_list.append([potion_blue])

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
mob_types = ["elf","goblin","imp","muddy","skeleton","tiny_zombie","big_demon","big_zombie","chort","docc","elf_f","goblin_warrior",
             'goblin_shaman',"Knight","necromancer","ogre","pumpkin","slug","swampy","wogol"]
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


"""creating all the object groups """
world = World()
player = None
arrow_group = pygame.sprite.Group()
lightning_group = pygame.sprite.Group()
fireball_group = pygame.sprite.Group()
damage_text_group = pygame.sprite.Group()
item_group = pygame.sprite.Group()
score_coin = Item(680,25,constants.COIN,item_image_list,True)
item_group.add(score_coin)
screen_fade = transition(1)
death_fade = transition(2)

gauge_size = (300, 20)  # Width and height of the gauge
corner_radius = 5  # Radius of the rounded corners
health_gauge_outline= pygame.Rect((40,5), gauge_size)
mana_gauge_outline= pygame.Rect((40,25), gauge_size)

def draw_rounded_rect(surface, rect, color, radius):
    pygame.draw.rect(surface, color, rect.inflate(-2 * radius, 0), border_radius=radius)
    pygame.draw.rect(surface, color, rect.inflate(0, -2 * radius), border_radius=radius)
 

# Function to draw the gauge
def draw_gauge(surface, percentage,color,rect,radius,pos):
    # Ensure percentage is within 0-100 range
    percentage = max(0, min(100, percentage))
    
    # Calculate the width of the filled part of the gauge
    fill_width = (percentage / 100) * gauge_size[0]
    """draw the outline"""
    pygame.draw.rect(surface, constants.BLACK, rect.inflate(-2 * radius, 0), border_radius=radius)
    pygame.draw.rect(surface, constants.BLACK, rect.inflate(0, -2 * radius), border_radius=radius)
    # Draw the filled part of the gauge
    if fill_width > 0:
        fill_rect = pygame.Rect(pos[0], pos[1] + 3, fill_width, gauge_size[1] - 3)
        draw_rounded_rect(surface, fill_rect, color, corner_radius)

"""displaying game info"""
def draw_text(text,font,color,x,y):
    img = font.render(text,True,color)
    screen.blit(img,(x,y))


def draw_info():
    """draw life the numbers passed to the screen blit is the offset of the hearts"""
    pygame.draw.rect(screen,constants.MENU_BG,(0,0,constants.SCREEN_WIDTH,50))
    pygame.draw.line(screen,constants.WHITE,(0,50),(constants.SCREEN_WIDTH,50))
    # for i in range(5):
    #     if player.health >= ((i+1)*20):
    #         screen.blit(heart_full,(10 + i*50,5))
    #     elif player.health <= ((i+1)*20) and player.health >((i)*20):
    #         screen.blit(heart_half,(10 + i*50,5))
    #     else:screen.blit(heart_empty,(10 + i*50,5))
    draw_gauge(screen,player.health,constants.RED,health_gauge_outline,10,(40,5))
    draw_gauge(screen,player.mana,constants.BLUE,mana_gauge_outline,10,(40,25))
    """level"""
    draw_text(f"Level: {level}",font,constants.WHITE,400,20)
    draw_text("HP",font,constants.WHITE,5,5)
    draw_text("MP",font,constants.WHITE,5,25)

    """show score"""
    draw_text(f"X{player.coins}",font,constants.WHITE,695,17)




"""creating the initial player instance"""
def make_world_data(): 
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

    with open(f"levels/level{level}_data.csv",newline="") as csvfile:
        reader =csv.reader(csvfile,delimiter=",")
        for row_num,row in enumerate(reader):
            for col_num,tile in enumerate(row):
                if tile != "-1":
                    world_data[row_num][col_num] = int(tile)  

    return world_data

world_data = make_world_data()
world.process_data(world_data,list_of_tiles,item_image_list,mob_animations,screen,player,sound_effects)
player = world.player
bow = Weapon(weapon_image,arrow_image,lightning_animation,world.player)


for item in world.item_list:
    item_group.add(item)

start_pos = (constants.SCREEN_WIDTH - 600,constants.SCREEN_HEIGHT//2 - 150 )
restart_pos = (constants.SCREEN_WIDTH- 600  ,constants.SCREEN_HEIGHT//2 - 50)
resume_pos = (constants.SCREEN_WIDTH- 600  ,constants.SCREEN_HEIGHT//2 - 150)
option_pos = (constants.SCREEN_WIDTH- 600  ,constants.SCREEN_HEIGHT//2)
exit_pos = (constants.SCREEN_WIDTH- 600 ,constants.SCREEN_HEIGHT//2 + 150)

start_button = Button(start_pos,[btn_green_2,btn_red_2],start_pos,"start",scale_img)
exit_button = Button( exit_pos,[btn_green_1,btn_red_1],exit_pos,"exit",scale_img)
options_button = Button( option_pos,[btn_green_1,btn_red_1],option_pos,"options",scale_img)
restart_button = Button( restart_pos,[btn_green_2,btn_red_2],restart_pos,"restart",scale_img)
resume_button = Button(resume_pos,[btn_green_1,btn_red_1],resume_pos,"resume",scale_img)

"""the actual game loop"""
run = True
while run:
   
    """initializing the game clock and drawing the charecter and weapon"""
    clock.tick(constants.FPS)
    if start_game == False:
        screen.fill(constants.MENU_BG)
        # intro_fx.play()
        if start_button.draw(screen):
            start_game = True
        if exit_button.draw(screen):
            run = False
    else:
        if pause_game:
            screen.fill(constants.MENU_BG)
            if exit_button.draw(screen):
                run = False
            if options_button.draw(screen):
                print("otions")   
            if resume_button.draw(screen):
                pause_game = False
        else:
            screen.fill(constants.BLACK)


            if player.alive:
                dx = 0
                dy = 0
                
                """ trnaslate the events into actions """
                if moving_up:
                    dy = -player.speed
                if moving_down:
                    dy = player.speed
                if moving_left:
                    dx = -player.speed
                if moving_right:
                    dx = player.speed

                # score_coin.draw(screen)
            
                lightning_magic =None
                cooldown = 500
                fireball = None     
                screen_scroll,level_complete = player.move(dx,dy,world.obstacle_tiles,world.exit_tile)

                """updateing the objects and the world data """
                world.update(screen_scroll)
                player.update() 
                
                    
                for enemy in world.enemy_list:
                    if enemy.alive:
                        fireball = enemy.enemy_movement(player,world.obstacle_tiles,screen_scroll,fireball_image)
                        enemy.update()
                    if fireball:    
                        fireball_group.add(fireball)

            
            world.draw(screen)
            player.draw(screen)    
            for enemy in world.enemy_list:
                if enemy.alive:
                    enemy.draw(screen)
            bow.draw(screen)
            arrow,lightning_magic = bow.update(player)
            if arrow:
                shot_fx.play()
                arrow_group.add(arrow)
            for arrow in arrow_group:
                arrow.draw(screen)
                damage_text = arrow.update(world.enemy_list,screen_scroll,world.obstacle_tiles,monster_death_fx)
                if damage_text:
                    damage_text_group.add(damage_text)
            
            if lightning_magic:
                lightning_group.add(lightning_magic)
                
            for lightning in lightning_group:
                lightning_fx.play()
                damage_text = lightning.update(screen,world.enemy_list,screen_scroll)

                if damage_text:
                    damage_text_group.add(damage_text)

            fireball_group.update(player,world.obstacle_tiles,screen_scroll,fire_fx)
            damage_text_group.update(screen_scroll)
            item_group.update(screen_scroll,player,potion_fx,coin_fx)   
            """this is the shooting function and the bow that fixes itself to the player"""
            
            draw_info()


            """drawing out the different grops"""
            damage_text_group.draw(screen)
            fireball_group.draw(screen)
            item_group.draw(screen)
            # draw_gauge(screen,player.mana)
            if level_complete:
                start_intro = True
                level += 1
                world_data = make_world_data()
                
                world = World()
                world.process_data(world_data,list_of_tiles,item_image_list,mob_animations,screen,player,hit_fx,sound_effects)
                player = world.player

                
                for item in world.item_list:
                    item_group.add(item)

                
            
            draw_text("this is sumthing",font,constants.RED,constants.SCREEN_WIDTH//2,constants.SCREEN_HEIGHT//1)
            if start_intro:
                
                if screen_fade.fade():
                    start_intro = False
                    screen_fade.fade_counter = 0

            if not player.alive:
                if death_fade.fade():
                    if restart_button.draw(screen):
                        death_fade.fade_counter = 0
                        start_intro =True
                        level = 1
                        world_data = make_world_data()
                        
                        world = World()
                        world.process_data(world_data,list_of_tiles,item_image_list,mob_animations,screen,player,hit_fx,sound_effects)
                        player = world.player
                        player.health = 10
                        player.alive = True
                        for item in world.item_list:
                            item_group.add(item)
                    if exit_button.draw(screen):
                        run = False



    """event handler loop """
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
           
            if event.key == pygame.K_f:
                bow.rate_of_fire -= 50
                    
            if event.key == pygame.K_r:
                bow.rate_of_fire = 300
                
            if event.key == pygame.K_ESCAPE:
                pause_game = True
                
                

                    
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



    pygame.display.update()

pygame.quit()