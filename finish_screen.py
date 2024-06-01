import pygame
import time
import constants

from images import btn_green_1, btn_green_2, btn_red_1, btn_red_2,background_image,scale_img
from damage_text import font
from button import Button


screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
exit_pos = (constants.SCREEN_WIDTH//2 +200,constants.SCREEN_HEIGHT//2 + 220)
restart_pos = (constants.SCREEN_WIDTH//2 - 200,constants.SCREEN_HEIGHT//2 + 220)

main_menu_button = Button( restart_pos,[btn_green_2,btn_red_2],restart_pos,"Main Menu",scale_img)
pause_exit_button = Button( exit_pos,[btn_green_2,btn_red_2],exit_pos,"Exit",scale_img)

prompt = (
    "Congratulations, brave hero!\n"
    "Through your unmatched courage and unwavering determination,\n"
    "you have conquered the treacherous dungeon and vanquished the feared demon lord.\n"
    "The echoes of your triumph resonate through the dark corridors,\n"
    "banishing shadows that long plagued this realm.\n"
    "Your skill in battle and strategic prowess have marked you as a true champion.\n"
    "As you stand amidst the silence left in the wake of your victory,\n"
    "know that your deeds will be sung by bards and celebrated by the grateful souls you have liberated.\n"
    "This day will forever be etched in legend, a testament to your extraordinary heroism.\n"
    "May your future journeys be as victorious,\n"
    "and may the light of your valor continue to drive away the darkness wherever your path may lead.\n"
    "creadits\n"
    "gameplay and mechanics - nadav hameleh\n"
    "sound and effects - nadav hameleh\n"
    "level building - nadav hameleh\n"
    "music\n"
    "evenged sevenfold\n"
    "breacking benjemin\n"
    "J cole\n"
    "sprites - itch.io\n"
    
)

def divide_paragraph(text, pos, color, edge):
    lines = text.splitlines()  
    space_width = font.size(' ')[0]
    x, y = pos
    list_of_lines = []

    for line in lines:
        words = line.split(' ')   
        current_line = []

        for word in words:
            word_surface = font.render(word, True, color)
            word_width, _ = word_surface.get_size()

            if x + word_width >= edge:
                x = pos[0]
                y += 30
                list_of_lines.append([' '.join(current_line), y])
                current_line = []

            current_line.append(word)
            x += word_width + space_width

        if current_line:
            x = pos[0]
            y += 30
            list_of_lines.append([' '.join(current_line), y])

    return list_of_lines

def render_text_letter_by_letter(text, color, n):
    if n < 0:
        return font.render("", True, color)
    elif n < len(text):
        return font.render(text[:n], True, color)
    else:
        return font.render(text, True, color) 

lines = divide_paragraph(prompt, (50, 300), constants.BLACK, 750)  # Start rendering text off-screen

def fin():
    run = True
    index = 0   
    char_index = 0
    scroll_active = True
    ticks = pygame.time.get_ticks
    time = ticks()

    while run:
        screen.blit(background_image,(0,0))

        # Render all completed lines
        for i in range(index):
            line_surface = render_text_letter_by_letter(lines[i][0], constants.BLACK, len(lines[i][0]))
            screen.blit(line_surface, (50, lines[i][1]))

        # Render current line
        if index < len(lines):
            current_line_surface = render_text_letter_by_letter(lines[index][0], constants.BLACK, char_index)
            screen.blit(current_line_surface, (50, lines[index][1]))
            char_index += 1
            if char_index >= len(lines[index][0]):
                index += 1
                char_index = 0

        # Update the y positions to scroll up
        scroll_cooldown = 20
        scroll_speed = 1
        if pygame.mouse.get_pressed()[0]:
            scroll_cooldown = 0
            scroll_speed = 2

        if scroll_active and ticks()-time >= scroll_cooldown:
            time = ticks()
            for line in lines:
                line[1] -= scroll_speed  # Adjust scroll speed here 
            print(lines[-1][1])
            # Stop scrolling when the last line's y-position is 400
            if lines[-1][1] <= 400:
                print(lines[-1][1])
                scroll_active = False
        if not scroll_active:
            if main_menu_button.draw(screen):
                return 1
            if pause_exit_button.draw(screen):
                pygame.quit()


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()
        clock.tick(60)  # Limit to 60 FPS
    
    pygame.quit()


