import constants
import pygame
from damage_text import font
from button import Button,NoTextButton
from images import mob_animations,btn_red_2,btn_green_2,btn_arrow_left,btn_arrow_right,btn_arrow_left_hover,btn_arrow_right_hover,scale_img,background_image
from death_screen import write_paragraph
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))
loyd_flavor = "Loyd is an elf from the fay realm \nHe is good at all things \nBut he does not exel in anything in particular"
fyona_flavor = "Fyona is the most accomplished thief in the western kingdom. \nDont let her looks fool you, \nor you will be left penniless..." 
kyle_flavor = "Kyle is an acomplished knigt \nHe has good strength and toughness \nBut the armor could be quite heavy..."
abraham_flavor = "Abraham the wizard, \nknown for his wisdom.  \nHis staff, made from the branch of the world tree, \nstrengthens his mana greatly \nBut he is getting pretty old to still be exploaring doengeons.."
# Path to the CSV file
file_path = 'levels/level1_data.csv'
def change_character():
   
    button_left = NoTextButton((80,420),[btn_arrow_left,btn_arrow_left_hover],scale_img,0.743)
    button_right = NoTextButton((290,420),[btn_arrow_right,btn_arrow_right_hover],scale_img,0.743)
    button_select = Button((200,500),[btn_red_2,btn_green_2],(200,500),"Select",scale_img)
    current_charecter = 1

    """direct the reader to the place the charecter is soppoused to be to make it more efficient"""
    """ make this reqursive to catch mistakes in the initial data {calls itself if the number it was looking for was not found in the csv}"""
    run = True
    while run:
        click_cooldown = 100
        ticks = pygame.time.get_ticks()
        clock.tick(constants.FPS)
        """add a button to switch between charecters """
        screen.blit(background_image,(0,0))
        screen.blit(scale_img(font.render("Select your character",True,constants.BLACK),1.5),(70,70))
        if current_charecter == 1:
            screen.blit(font.render("Loyd",True,constants.BLACK),(130,150))
            # screen.blit(font.render("Loyd is an elf from ",True,constants.BLACK),(340,200))
            write_paragraph(screen,loyd_flavor,(340,200),constants.BLACK,750)
            # screen.blit(font.render("the fay realm he is",True,constants.BLACK),(340,230))
            # screen.blit(font.render("good at all things",True,constants.BLACK),(340,260))
            # screen.blit(font.render("but he does not ",True,constants.BLACK),(340,290))
            # screen.blit(font.render("exel in enything",True,constants.BLACK),(340,320))

            screen.blit(scale_img(mob_animations[constants.ELF][0][0],3),(110,150)) 
        if  current_charecter == 2:
            screen.blit(font.render("Fyona",True,constants.BLACK),(130,150))
            write_paragraph(screen,fyona_flavor,(340,200),constants.BLACK,750)
            # screen.blit(font.render("Fyona",True,constants.BLACK),(130,150))
            # screen.blit(font.render("Fyona is the most ",True,constants.BLACK),(340,200))
            # screen.blit(font.render("accomplished thief in",True,constants.BLACK),(340,230))
            # screen.blit(font.render("she is trained in ",True,constants.BLACK),(340,260))
            # screen.blit(font.render("magic and has excelt ",True,constants.BLACK),(340,290))
            # screen.blit(font.render("speed but she is ",True,constants.BLACK),(340,320))
            # screen.blit(font.render("quite frail tho ...",True,constants.BLACK),(340,350))

            screen.blit(scale_img(mob_animations[constants.ELF_F][0][0],3),(110,150)) 
        if  current_charecter == 3:
            screen.blit(font.render("Kyle",True,constants.BLACK),(130,150))
            write_paragraph(screen,kyle_flavor,(340,200),constants.BLACK,750)        
            screen.blit(scale_img(mob_animations[constants.KNIGHT][0][0],3),(110,150)) 
        if  current_charecter == 4:
            screen.blit(font.render("Abraham",True,constants.BLACK),(130,150))
            write_paragraph(screen,abraham_flavor,(340,200),constants.BLACK,750)
            
            screen.blit(scale_img(mob_animations[constants.WIZARD][0][0],3),(110,150)) 
        if current_charecter > 1:
            if button_left.draw(screen):
                if ticks - button_left.last_clicked > click_cooldown: 
                    current_charecter -= 1
                    button_left.last_clicked = ticks
                    
        if current_charecter < 4:                
            if button_right.draw(screen):
                if ticks - button_right.last_clicked > click_cooldown: 
                    current_charecter += 1
                    button_right.last_clicked = ticks
                    
        if button_select.draw(screen):
            run = False
            return current_charecter
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        # screen.blit(btn_,)

        """on click calls change charecter and changes the """

        pygame.display.update()
        
    pygame.quit()

