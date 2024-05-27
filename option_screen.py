import pygame
from sound_fx import player_sfx,monster_stx,game_sound, music
import constants
from damage_text import font
from button import Button,DragButton
from images import background_image,btn_green_2,btn_red_2,scale_img

"""control volume """

"""game volume control with a knob that goes left and right and a button to murte with indication """
"""charecter volume  control with a knob that goes left and right and a button to murte with indication """
"""mob volume control with a knob that goes left and right and a button to murte with indication """


pygame.init()
screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))

# def draw_gauge(surface, percentage,color,rect,radius,pos,gauge_size):
#     # Ensure percentage is within 0-100 range
#     percentage = max(0, min(100, percentage))
    
#     # Calculate the width of the filled part of the gauge
#     fill_width = (percentage / 100) * gauge_size[0]
#     """draw the outline"""
#     pygame.draw.rect(surface, constants.BLACK, rect.inflate(-2 * radius, 0), border_radius=radius)
#     pygame.draw.rect(surface, constants.BLACK, rect.inflate(0, -2 * radius), border_radius=radius)
#     # Draw the filled part of the gauge
#     if fill_width > 0:
#         fill_rect = pygame.Rect(pos[0], pos[1] + 3, fill_width, gauge_size[1] - 3)
#         draw_rounded_rect(surface, fill_rect, color, corner_radius)

def draw_rounded_rect(surface, rect, color, radius):
    pygame.draw.rect(surface, color, rect.inflate(-2 * radius, 0), border_radius=radius)
    pygame.draw.rect(surface, color, rect.inflate(0, -2 * radius), border_radius=radius)

def set_volume(bg_music_vol,game_vol,mob_vol,player_vol):
    music.set_volume(bg_music_vol)
    for sfx in game_sound:
        sfx.set_volume(game_vol) 
    for sfx in monster_stx:
        sfx.set_volume(mob_vol) 
    for sfx in player_sfx:
        sfx.set_volume(player_vol) 

togle_length = 250
music_togle_pos = (650,100)
game_sound_togle_pos = (650,200)
mob_sound_togle_pos = (650,300)
player_sound_togle_pos = (650,400)

text_1 = font.render("Game Music: ",True,constants.BLACK)
text_2 = font.render("Game Sound: ",True,constants.BLACK)
text_3 = font.render("Monster Sound: ",True,constants.BLACK)
text_4 = font.render("Player Sound: ",True,constants.BLACK)


music_togle = DragButton(music_togle_pos,music_togle_pos[0] - togle_length,music_togle_pos[0])
game_sound_togle = DragButton(game_sound_togle_pos,game_sound_togle_pos[0] - togle_length,game_sound_togle_pos[0])
mob_sound_togle = DragButton(mob_sound_togle_pos,mob_sound_togle_pos[0] - togle_length,mob_sound_togle_pos[0])
player_sound_togle = DragButton(player_sound_togle_pos,player_sound_togle_pos[0] - togle_length,player_sound_togle_pos[0])

confirm_button = Button((600,500),[btn_green_2,btn_red_2],(600,500),"Confirm",scale_img)
def options():
    corner_radius = 5
    mouse_pos = (0,0)
    clicked = False
    run = True
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
            if event.type == pygame.MOUSEMOTION:
                mouse_pos = pygame.mouse.get_pos()
                
        screen.blit(background_image,(0,0))        
        screen.blit(text_1,(100,100))        
        screen.blit(text_2,(100,200))        
        screen.blit(text_3,(100,300))        
        screen.blit(text_4,(100,400))        
        draw_rounded_rect(screen,pygame.rect.Rect(music_togle_pos[0] - togle_length,music_togle_pos[1],togle_length,10),constants.BLACK,corner_radius)
        draw_rounded_rect(screen,pygame.rect.Rect(game_sound_togle_pos[0] - togle_length,game_sound_togle_pos[1],togle_length,10),constants.BLACK,corner_radius)
        draw_rounded_rect(screen,pygame.rect.Rect(player_sound_togle_pos[0] - togle_length,player_sound_togle_pos[1],togle_length,10),constants.BLACK,corner_radius)
        draw_rounded_rect(screen,pygame.rect.Rect(mob_sound_togle_pos[0] - togle_length,mob_sound_togle_pos[1],togle_length,10),constants.BLACK,corner_radius)
        music_togle.draw(screen)
        bg_music_vol = music_togle.drag(mouse_pos)
        game_sound_togle.draw(screen)
        game_vol = game_sound_togle.drag(mouse_pos)
        mob_sound_togle.draw(screen)
        mob_vol =  mob_sound_togle.drag(mouse_pos)
        player_sound_togle.draw(screen)
        player_vol = player_sound_togle.drag(mouse_pos)
        if confirm_button.draw(screen):
            set_volume(bg_music_vol,game_vol,mob_vol,player_vol)
            run = False
        pygame.display.update()



