import pandas as pd
import constants
import pygame
from damage_text import font
from button import Button,NoTextButton
from images import mob_animations,btn_red_2,btn_green_2,btn_arrow_left,btn_arrow_right,btn_arrow_left_hover,btn_arrow_right_hover,scale_img,background_image
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))

# Path to the CSV file
file_path = 'levels/level1_data.csv'
def change_character():
   
    button_left = NoTextButton((80,420),[btn_arrow_left,btn_arrow_left_hover],scale_img)
    button_right = NoTextButton((290,420),[btn_arrow_right,btn_arrow_right_hover],scale_img)
    buttom_select = Button((200,500),[btn_red_2,btn_green_2],(200,500),"Select",scale_img)
    current_charecter = 1

    """direct the reader to the place the charecter is soppoused to be to make it more efficient"""
    """ make this reqursive to catch mistakes in the initial data {calls itself if the number it was looking for was not found in the csv}"""
    run = True
    while run:
        click_cooldown = 300
        ticks = pygame.time.get_ticks()
        clock.tick(constants.FPS)
        """add a button to switch between charecters """
        screen.blit(background_image,(0,0))
        screen.blit(scale_img(font.render("Select your character",True,constants.BLACK),1.5),(70,70))
        if current_charecter == 1:
            screen.blit(font.render("Loyd",True,constants.BLACK),(130,150))
            screen.blit(font.render("Loyd is an elf from ",True,constants.BLACK),(340,200))
            screen.blit(font.render("the fay realm he is",True,constants.BLACK),(340,230))
            screen.blit(font.render("good at all things",True,constants.BLACK),(340,260))
            screen.blit(font.render("but he does not ",True,constants.BLACK),(340,290))
            screen.blit(font.render("exel in enything",True,constants.BLACK),(340,320))

            screen.blit(scale_img(mob_animations[constants.ELF][0][0],3),(110,150)) 
        if  current_charecter == 2:
            screen.blit(font.render("Fyona",True,constants.BLACK),(130,150))
            screen.blit(font.render("Fyona is the princess ",True,constants.BLACK),(340,200))
            screen.blit(font.render("of the elf kingdom ",True,constants.BLACK),(340,230))
            screen.blit(font.render("she is trained in ",True,constants.BLACK),(340,260))
            screen.blit(font.render("magic and has excelt ",True,constants.BLACK),(340,290))
            screen.blit(font.render("speed but she is ",True,constants.BLACK),(340,320))
            screen.blit(font.render("quite frail tho ...",True,constants.BLACK),(340,350))

            screen.blit(scale_img(mob_animations[constants.ELF_F][0][0],3),(110,150)) 
        if  current_charecter == 3:
            screen.blit(font.render("Kyle",True,constants.BLACK),(130,150))
            screen.blit(font.render("Kyle is an acomplished ",True,constants.BLACK),(340,200))
            screen.blit(font.render("knigt he has good ",True,constants.BLACK),(340,230))
            screen.blit(font.render("strength and toughness",True,constants.BLACK),(340,260))
            screen.blit(font.render("but the armor could",True,constants.BLACK),(340,290))
            screen.blit(font.render("be quite heavy...",True,constants.BLACK),(340,320))

            screen.blit(scale_img(mob_animations[constants.KNIGHT][0][0],3),(110,150)) 
        if  current_charecter == 4:
            screen.blit(font.render("Abraham",True,constants.BLACK),(130,150))
            screen.blit(font.render("Abraham the wizard,",True,constants.BLACK),(340,200))
            screen.blit(font.render("renowned for his wisdom ",True,constants.BLACK),(340,230))
            screen.blit(font.render("His hard shaft, made",True,constants.BLACK),(340,260))
            screen.blit(font.render("from oak strengthens ",True,constants.BLACK),(340,290))
            screen.blit(font.render("his mana but",True,constants.BLACK),(340,320))
            screen.blit(font.render("he is getting old to",True,constants.BLACK),(340,350))
            screen.blit(font.render("still be exploaring",True,constants.BLACK),(340,380))

            screen.blit(scale_img(mob_animations[constants.WIZARD][0][0],3),(110,150)) 
        if current_charecter > 1:
            if button_left.draw(screen):
                if ticks - button_left.last_clicked > click_cooldown: 
                    current_charecter -= 1
                    button_left.last_clicked = ticks
                    print(current_charecter)
        if current_charecter < 4:                
            if button_right.draw(screen):
                if ticks - button_right.last_clicked > click_cooldown: 
                    current_charecter += 1
                    button_right.last_clicked = ticks
                    print(current_charecter)
        if buttom_select.draw(screen):
            run = False
            return current_charecter
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # screen.blit(btn_,)

        """on click calls change charecter and changes the """

        pygame.display.update()
        
    pygame.quit()

