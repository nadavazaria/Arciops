import pygame
import pygame.event
import constants
from images import btn_green_1,btn_red_1,background_image,scale_img,speed_up_image,hp_up_image,mp_up_image,att_speed_up_image,damage_up_image,shop_item_bg,shop_item_bg_dark,item_image_list
from button import Button,NoTextButton
import random
from sound_fx import buy_item_fx
from damage_text import font
pygame.init()

Clock = pygame.time.Clock()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))
button_pos = ()
roll = random.random()

"""make a screen that looks like a maplestory shop with a buy option and prtice listed in it"""

def roll_for_dicount(level): 
    roll = random.random()
    price_modifier = 1
    color = constants.BLACK
    if roll < 0.4:
        price_modifier = 1.3
        color = constants.RED
    elif roll >= 0.4 and roll <= 0.8:
        pass
    elif roll >= 0.6 and roll < 0.95:
        price_modifier = 0.7
        color = constants.GREEN
    else:
        price_modifier = 0.4
        color = constants.GREEN
    return price_modifier*level,color

def draw_shop_screen(font):
    # pygame.draw.rect(screen,constants.MENU_BG,(75,100,650,00))
    pygame.draw.rect(screen,constants.BLACK,(70,100,660,375),5)
    pygame.draw.rect(screen,constants.WHITE,(75,100,650,75))
    pygame.draw.rect(screen,constants.BLACK,(70,100,660,75),5)
    shop_title = font.render("Black Merchent",True,constants.BLACK)
    screen.blit(scale_img(shop_title,1.5),(180,125))
    
def add_shop_entry(image,pos,text,price,color,index):
    coin_frame = item_image_list[constants.COIN][index]
    item_cost = str(price)
    action = False
    """pos = (100,175)"""
    buy_button = NoTextButton((pos[0] + 325,pos[1]+25),[shop_item_bg,shop_item_bg_dark],scale_img,1)
    if buy_button.draw(screen):
        action = True
    pygame.draw.line(screen,constants.BLACK,(pos[0]+50,pos[1]),(pos[0]+50,pos[1] + 50),5)
    screen.blit(font.render(text,True,constants.BLACK),(pos[0] + 65,pos[1]+15))
    pygame.draw.line(screen,constants.BLACK,(pos[0]+575,pos[1]),(pos[0]+575,pos[1] + 50),5)
    screen.blit(image,pos)
    screen.blit(coin_frame,(pos[0]+625,pos[1]+10))
    screen.blit(font.render(item_cost,True,color),(pos[0] + 585,pos[1]+15))
    return action


"""trying to make a pop up confirmation message"""

"""the game loop crashes when i try to access the confirnation window"""
def confirmation_message():  
    
    now = pygame.time.get_ticks()
    buy_button = Button((350,250),[btn_green_1,btn_red_1],(350,250),"Buy",scale_img)
    cancel_button = Button((350,350),[btn_green_1,btn_red_1],(350,350),"Cancel",scale_img)
    run = True
    
    while run:
        clicked = False
        for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        clicked = True
        pygame.draw.rect(screen,constants.MENU_BG,(200,100,300,300))
        pygame.draw.rect(screen,constants.WHITE,(200,100,300,50))
        screen.blit(font.render("are you sure?",True,constants.BLACK),(225,110))
        pygame.draw.rect(screen,constants.BLACK,(200,100,300,50),5)
        pygame.draw.rect(screen,constants.BLACK,(200,100,300,300),5)
        if buy_button.draw(screen) and clicked:
            run = False
            return True

        if cancel_button.draw(screen) and clicked:
            run = False
            return False
                        
        pygame.display.update()

    

def merchent(player,weapon,level):
    ticks = pygame.time.get_ticks
    updated_frame = ticks() 
    frame_cooldown = 150
    upgrade = -1
    index = 0
    done_button = Button((600,540),[btn_green_1,btn_red_1],(600,540),"Done",scale_img) 
     
   
    [price_modifier1,color1] = roll_for_dicount(level) 
    [price_modifier2,color2] = roll_for_dicount(level) 
    [price_modifier3,color3] = roll_for_dicount(level) 
    [price_modifier4,color4] = roll_for_dicount(level) 
    [price_modifier5,color5] = roll_for_dicount(level) 
    price1 = int(8*price_modifier1//1)
    price2 = int(5*price_modifier2//1)
    price3 = int(5*price_modifier3//1)
    price4 = int(10*price_modifier4//1)
    price5 = int(10*price_modifier5//1)
    run = True 
    while run:
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        pygame.display.update()
        if ticks() - updated_frame >= frame_cooldown:
            if index <= 2:
                index += 1 
                updated_frame = ticks()
            else:
                index = 0
                updated_frame = ticks()
        screen.blit(background_image,(0,0))
        draw_shop_screen(font)
        
        if  add_shop_entry(damage_up_image,(75,175),"Increase damage slightly",price1,color1,index) and  clicked :
            upgrade = 0
        if add_shop_entry(hp_up_image,(75,225),"Increase health slightly",price2,color2,index) and  clicked:
            upgrade = 1
        if add_shop_entry(mp_up_image,(75,275),"Increase mana slightly",price3,color3,index) and  clicked:
            upgrade = 2
        if add_shop_entry(speed_up_image,(75,325),"Increase speed slightly",price4,color4,index) and  clicked:
            upgrade = 3
        if add_shop_entry(att_speed_up_image,(75,375),"Increase rate of fire",price5,color5,index) and  clicked:
            upgrade = 4
        screen.blit(font.render("coins X"+str(player.coins),True,constants.BLACK),(75,450))

        if done_button.draw(screen) and clicked:
            run = False
        

        if upgrade == 0:
            upgrade = -1
            if confirmation_message():
                if process_deal(player.coins,price1):
                    player.coins -= price1
                    buy_item_fx.play()
                    player.damage += 7
        if upgrade == 1:
            upgrade = -1
            if confirmation_message():
                if process_deal(player.coins,price2):
                    player.coins -= price2
                    buy_item_fx.play()
                    player.max_health += 10

        if upgrade == 2:
            upgrade = -1
            if confirmation_message():
                if process_deal(player.coins,price3):
                    player.coins -= price3
                    buy_item_fx.play()
                    player.max_mana += 10
                
        if upgrade == 3:
            upgrade = -1
            if confirmation_message():
                if process_deal(player.coins,price4):
                    player.coins -= price4
                    buy_item_fx.play()
                    player.speed += 0.5
        if upgrade == 4:
            upgrade = -1
            if confirmation_message():
                if process_deal(player.coins,price5):
                    player.coins -= price5
                    buy_item_fx.play()
                    weapon.rate_of_fire -= 30

       

def process_deal(coins,price):
    if coins < price:
        ok_button = Button((350,350),[btn_green_1,btn_red_1],(350,350),"OK",scale_img)                       
        while True:
            pygame.draw.rect(screen,constants.MENU_BG,(200,200,300,200))
            pygame.draw.rect(screen,constants.WHITE,(200,200,300,75))
            screen.blit(font.render("insuficiant",True,constants.BLACK),(240,210))
            screen.blit(font.render("coins",True,constants.BLACK),(300,230))
            pygame.draw.rect(screen,constants.BLACK,(200,200,300,75),5)
            pygame.draw.rect(screen,constants.BLACK,(200,200,300,200),5)

            if ok_button.draw(screen):
                return False
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
    else:
        return True

