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
                        print("found the button ")
                        clicked = True
        pygame.draw.rect(screen,constants.MENU_BG,(200,100,300,300))
        pygame.draw.rect(screen,constants.WHITE,(200,100,300,50))
        screen.blit(font.render("are you sure?",True,constants.BLACK),(225,110))
        pygame.draw.rect(screen,constants.BLACK,(200,100,300,50),5)
        pygame.draw.rect(screen,constants.BLACK,(200,100,300,300),5)
        print(clicked)
        if buy_button.draw(screen) and clicked:
            print("the events overlapp")
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
                    player.speed += 1
        if upgrade == 4:
            upgrade = -1
            if confirmation_message():
                if process_deal(player.coins,price5):
                    player.coins -= price5
                    buy_item_fx.play()
                    weapon.rate_of_fire -= 30

       

