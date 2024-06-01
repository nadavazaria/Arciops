import pygame 
from images import scale_img,reaper_image,btn_green_1,btn_green_2,btn_green_3,btn_red_1,btn_red_2,btn_red_3,death_bg 
from button import Button
from damage_text import font
import constants
pygame.init()

screen = pygame.display.set_mode((800,600))

btn_revive = Button((140,200),[btn_green_3,btn_red_3],(150,210),"Revive",scale_img)
btn_main_menu = Button((150,350),[btn_green_1,btn_red_1],(150,350),"Main Menu",scale_img)
btn_quit = Button((150,500),[btn_green_2,btn_red_2],(150,500),"Quit Game",scale_img)

prompt_1="I am willing to grant you a pardon from death \nfor a price..."
prompt_2="There are no favors I will give out for free \nbetter luck in the next world..."



def write_paragraph(surface,text,pos,color,edge):
        collection = [word.split(' ') for word in text.splitlines()]
        space = font.size(' ')[0]
        x,y = pos
        for lines in collection:
            for words in lines :
                word_surface = font.render(words,True,color)
                word_width , garbage  = word_surface.get_size()
                if x + word_width >= edge:
                    x = pos[0]
                    y += 30
                surface.blit(word_surface,(x,y))
                x += word_width + space
            x = pos[0]
            y += 30
        pass
def you_died(player):
    rich = False
    revive_cost = player.lv*4
    prompt = ""
    if player.coins >= revive_cost:
        rich = True
        prompt = prompt_1 
    else:
        prompt = prompt_2
    run = True
    while run:
        clicked = False
        action = -1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True

        
        screen.blit(death_bg,(0,0))
        screen.blit(reaper_image,(430,0))
        write_paragraph(screen,prompt,(300,200),constants.RED,600)
        
        if btn_quit.draw(screen) and clicked:
            action = 0
        if btn_main_menu.draw(screen)and clicked:
            action = 1
        if rich:
            if btn_revive.draw(screen)and clicked:
                player.coins -= revive_cost
                action = 2
        if action >=0:
            return action
        pygame.display.update()
