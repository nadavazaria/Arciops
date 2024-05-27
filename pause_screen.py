import pygame
import pygame.event
import constants
from images import btn_green_1,btn_red_1,btn_green_2,btn_green_3,btn_red_2,btn_red_3,background_image,scale_img,speed_up_image,hp_up_image,mp_up_image,att_speed_up_image,damage_up_image,shop_item_bg,shop_item_bg_dark,item_image_list
from button import Button
import random
from damage_text import font
from option_screen import options
pygame.init()

Clock = pygame.time.Clock()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))
button_pos = ()

pause_text = font.render("GAME PAUSED",True,constants.BLACK)
resume_pos = (constants.SCREEN_WIDTH//2 -10 ,constants.SCREEN_HEIGHT//2 - 140)
options_pos = (constants.SCREEN_WIDTH//2 ,constants.SCREEN_HEIGHT//2 -20)
restart_pos = (constants.SCREEN_WIDTH//2 ,constants.SCREEN_HEIGHT//2 + 100)
exit_pos = (constants.SCREEN_WIDTH//2,constants.SCREEN_HEIGHT//2 + 220)


resume_button = Button(resume_pos,[btn_green_3,btn_red_3],(resume_pos[0],resume_pos[1] + 5),"Resume",scale_img)
options_button = Button( options_pos,[btn_green_1,btn_red_1],options_pos,"Options",scale_img)
main_menu_button = Button( restart_pos,[btn_green_1,btn_red_1],restart_pos,"Main Menu",scale_img)
pause_exit_button = Button( exit_pos,[btn_green_2,btn_red_2],exit_pos,"Exit",scale_img)

# done_button = Button((600,540),[btn_green_1,btn_red_1],(600,540),"Done",scale_img) 

def pause():
    ticks = pygame.time.get_ticks
   
       
    
    run = True 
    action = 0
    while run:
        clicked = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
        screen.blit(background_image,(0,0)) 
        # screen.blit(scale_img(pause_text,1.5),(constants.SCREEN_WIDTH//2 - 150 ,50))
        screen.blit(scale_img(pause_text,1.5),(constants.SCREEN_WIDTH//2 - 170 ,50))
        if resume_button.draw(screen) and clicked:
            action = 1
        if pause_exit_button.draw(screen) and clicked:
            action = 2
        if options_button.draw(screen) and clicked:
            options()
        if main_menu_button.draw(screen) and clicked:
            action = 3
        if action != 0 :
            return action
         
       
        pygame.display.update()


# def confirmation_message():  
    
#     now = pygame.time.get_ticks()
#     buy_button = Button((350,250),[btn_green_1,btn_red_1],(350,250),"Buy",scale_img)
#     cancel_button = Button((350,350),[btn_green_1,btn_red_1],(350,350),"Cancel",scale_img)
#     run = True
    
#     while run:
#         clicked = False
#         for event in pygame.event.get():
#                     if event.type == pygame.QUIT:
#                         pygame.quit()
#                     if event.type == pygame.MOUSEBUTTONDOWN:
#                         print("found the button ")
#                         clicked = True
#         pygame.draw.rect(screen,constants.MENU_BG,(200,100,300,300))
#         pygame.draw.rect(screen,constants.WHITE,(200,100,300,50))
#         screen.blit(font.render("are you sure?",True,constants.BLACK),(225,110))
#         pygame.draw.rect(screen,constants.BLACK,(200,100,300,50),5)
#         pygame.draw.rect(screen,constants.BLACK,(200,100,300,300),5)
#         print(clicked)
#         if buy_button.draw(screen) and clicked:
#             print("the events overlapp")
#             run = False
#             return True

#         if cancel_button.draw(screen) and clicked:
#             run = False
#             return False
                        
#         pygame.display.update()

