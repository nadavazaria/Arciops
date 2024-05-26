import pygame
from pygame import mixer
import math
from world import World
import constants
from weapon import Weapon
from damage_text import font
from items import Item
from button import Button
from character_select import change_character
from merchent_screen import merchent
import time 
import csv
import random
from damage_text import DamageText
from images import mob_animations,item_image_list,game_bg,background_image,reaper_image,lightning_animation,bow_image,staff_image,knife_image,knife_throw_image,arrow_image,fireball_image,btn_green_1,btn_green_3,btn_green_2,btn_red_1,btn_red_3,btn_red_2,scale_img,list_of_tiles
from sound_fx import sound_effects, music
def main():
        
    mixer.init()
    pygame.init() 
    # create the game window
    screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))

    pygame.display.set_caption("Arciops")

    clock = pygame.time.Clock()

    """define the game level"""
    level = 2
    start_game = False
    pause_game = False
    screen_scroll = [0,0]
    start_intro = True
    moving_up = False
    moving_down = False
    moving_left = False
    moving_right = False
    exp_font = pygame.font.SysFont("Ariel",26)

    class ScreenFade():
        
        def __init__(self,direction,color,speed):
            self.speed = speed
            self.color = color
            self.direction = direction
            self.fade_counter = 0

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
    exp_gauge_size = (constants.SCREEN_WIDTH, 20)  # Width and height of the gauge
    corner_radius = 5  # Radius of the rounded corners
    health_position = (40,5)
    mana_position = (40,25)
    exp_position = (5,constants.SCREEN_HEIGHT - 25)
    health_gauge_outline= pygame.Rect(health_position, gauge_size)
    mana_gauge_outline= pygame.Rect(mana_position, gauge_size)
    exp_gauge_outline = pygame.Rect(exp_position,exp_gauge_size)

    def draw_rounded_rect(surface, rect, color, radius):
        pygame.draw.rect(surface, color, rect.inflate(-2 * radius, 0), border_radius=radius)
        pygame.draw.rect(surface, color, rect.inflate(0, -2 * radius), border_radius=radius)
    

    # Function to draw the gauge
    def draw_gauge(surface, percentage,color,rect,radius,pos,gauge_size):
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

    def write_paragraph(surface,text,pos,color):
        collection = [word.split(' ') for word in text.splitlines()]
        space = font.size(' ')[0]
        x,y = pos
        for lines in collection:
            for words in lines :
                word_surface = font.render(words,True,color)
                word_width , word_hiegt  = word_surface.get_size()
                if x + word_width >=constants.SCREEN_WIDTH:
                    x = pos[0]
                    y += 30
                surface.blit(word_surface,(x,y))
                x += word_width + space
            x = pos[0]
            y += 30
        pass

    def draw_info():
        """draw life the numbers passed to the screen blit is the offset of the hearts"""

        text_color = constants.WHITE
        if player.exp/player.to_next_lv*100//1  > 60:
            text_color = constants.BLACK    

        pygame.draw.rect(screen,constants.MENU_BG,(0,0,constants.SCREEN_WIDTH,50))
        pygame.draw.line(screen,constants.WHITE,(0,50),(constants.SCREEN_WIDTH,50))

        draw_gauge(screen,player.health/player.max_health*100,constants.RED,health_gauge_outline,10,health_position,gauge_size)
        draw_gauge(screen,player.mana/player.max_mana*100,constants.BLUE,mana_gauge_outline,10,mana_position,gauge_size)
        draw_gauge(screen,player.exp/player.to_next_lv*100,constants.EXP_COLOR,exp_gauge_outline,10,exp_position,exp_gauge_size)
        screen.blit(exp_font.render(f"{int(player.exp/player.to_next_lv*100//1)}%",True,text_color),(constants.SCREEN_WIDTH/2,exp_position[1] + 5))
        """level"""
        draw_text(f"Level: {player.lv}",font,constants.WHITE,400,20)
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
                    if tile[0] != "-":
                        world_data[row_num][col_num] = int(tile)  

        return world_data

    world_data = make_world_data()
    world.process_data(world_data,list_of_tiles,item_image_list,mob_animations,screen,player,sound_effects)
    player = world.player
    weapon = Weapon(bow_image,arrow_image,lightning_animation,world.player)


    for item in world.item_list:
        item_group.add(item)







    start_pos = (constants.SCREEN_WIDTH - 635,constants.SCREEN_HEIGHT//2 - 40)
    restart_pos = (constants.SCREEN_WIDTH- 630  ,constants.SCREEN_HEIGHT//2 + 80)
    charecter_pos = (constants.SCREEN_WIDTH- 630  ,constants.SCREEN_HEIGHT//2 + 80 )
    resume_pos = (constants.SCREEN_WIDTH- 630  ,constants.SCREEN_HEIGHT//2)
    option_pos = (constants.SCREEN_WIDTH- 630  ,constants.SCREEN_HEIGHT//2 + 90)
    exit_pos = (constants.SCREEN_WIDTH- 630 ,constants.SCREEN_HEIGHT//2 + 200)


    start_button = Button(start_pos,[btn_green_3,btn_red_3],(start_pos[0],start_pos[1]+5),"start",scale_img)
    main_exit_button = Button( exit_pos,[btn_green_2,btn_red_2],exit_pos,"exit",scale_img)
    charecter_button = Button( charecter_pos,[btn_green_1,btn_red_1],(charecter_pos[0]-5,charecter_pos[1]-5),"charecter",scale_img)


    restart_button = Button( restart_pos,[btn_green_2,btn_red_2],restart_pos,"restart",scale_img)
    pause_exit_button = Button( exit_pos,[btn_green_2,btn_red_2],exit_pos,"exit",scale_img)
    resume_button = Button(resume_pos,[btn_green_3,btn_red_3],resume_pos,"resume",scale_img)


    options_button = Button( option_pos,[btn_green_1,btn_red_1],option_pos,"options",scale_img)

    def cacl_damage(arrow):
        arrow.draw(screen)
        arrow.update(screen_scroll,world.obstacle_tiles)
        for enemy in world.enemy_list:
            damage_text = None
            if enemy.rect.colliderect(arrow.rect) and enemy.alive:
                enemy.hit_fx.play()
                damage = int(arrow.damage - 5 + random.random()*10//1)
                if enemy.health - damage <= 0:
                    enemy.death_fx.play()
                    player.exp += enemy.exp_value
                    drop_item(enemy.rect.centerx,enemy.rect.centery)
                enemy.health -= damage
                enemy.hit = True
                enemy.last_hit = pygame.time.get_ticks()
                arrow.kill()
                damage_text = DamageText(enemy.rect.centerx,enemy.rect.centery,str(damage),constants.RED)   
                break
        return damage_text
    def drop_item(x,y):
        drop = False
        if random.random()> 0.95:
            drop = True
        if drop: 
            item = random.random()
            if item > 0 and item <= 0.7:
                item = constants.COIN
            elif item > 0.7 and item <= 0.8:
                item = constants.POTION_BLUE
            elif item > 0.8 and item <= 0.85:
                item = constants.POTION_RED
            elif item > 0.85 and item <= 0.95:
                item = constants.POTION_YELLOW
            elif item > 0.95 and item < 1:
                item = constants.POTION_YELLOW_BIG
            new_item = Item(x,y,item,item_image_list) 
            item_group.add(new_item)

    def render_text_leter_by_leter(text,color,n,delay_s = 0):
        if delay_s >0 : 
            time.sleep(delay_s)
        if n < 0 :
            return font.render("",True,color)
        elif n < len(text) - 1:
            return font.render(text[:n],True,color)
        else:
            return font.render(text,True,color) 

    
    prompt_1 = "welcome to a world of magic"
    prompt_2 = "young hero we need you!"
    prompt_3 = "the demon lord has come"
    prompt_4 = "only you can traverse"
    prompt_5 = "the doungeon and slay"
    prompt_6 = "the beast for the sake"
    prompt_7 = "of our world"


    """the actual game loop"""
    run = True
    index = 0

    while run:

        
        """initializing the game clock and drawing the charecter and weapon"""
        clock.tick(constants.FPS)

        if start_game == False:
            if pygame.mouse.get_pressed()[0]:
                index = 150
            if index < 150:
                index += 1      
                    
            screen.blit(background_image,(0,0))
            screen.blit(scale_img(font.render("~ARCIOPS~",True,constants.BLACK),3),(140,70))
            # intro_fx.play()
            if start_button.draw(screen):
                start_game = True
            if main_exit_button.draw(screen):
                run = False
            if charecter_button.draw(screen):
                selected_charecter = change_character()

                if selected_charecter == 1: #chose the elf
                    player.animation_list = mob_animations[constants.ELF]
                    player.image = player.animation_list[0][0]
                    player.death_fx = sound_effects["player_m_death_fx"]
                    player.hit_fx = sound_effects["player_m_hit_fx"]
                    player.make_the_difference(100,100,5,20,50)
                    
                if selected_charecter == 2:# chose the female player
                    player.animation_list = mob_animations[constants.ELF_F]
                    player.image = player.animation_list[0][0]
                    player.death_fx = sound_effects["player_f_death_fx"]
                    player.hit_fx = sound_effects["player_f_hit_fx"]
                    player.mana_regen *= 2
                    
                    player.make_the_difference(100,120,6,15,60)
                    
                if selected_charecter == 3: #chose the knigt
                    player.animation_list = mob_animations[constants.KNIGHT]
                    player.image = player.animation_list[0][0]
                    player.death_fx = sound_effects["player_m_death_fx"]
                    player.hit_fx = sound_effects["player_m_hit_fx"]
                    weapon.original_image = knife_image
                    weapon.arrow_image = knife_throw_image 
                    player.make_the_difference(130,85,4,35,40)

                if selected_charecter == 4: #chose the wizard
                    print("wizard")
                    player.animation_list = mob_animations[constants.WIZARD]
                    player.image = player.animation_list[0][0]
                    player.death_fx = sound_effects["wizard_death_fx"]
                    player.hit_fx = sound_effects["wizard_hit_fx"]
                    weapon.original_image = staff_image
                    weapon.arrow_image = fireball_image
                    player.mana_regen = 0.03
                    player.make_the_difference(100,200,3,20,70)



                    
            prompt_ln_1 = render_text_leter_by_leter(prompt_1,constants.BLACK,index,0.01)
            prompt_ln_2 = render_text_leter_by_leter(prompt_2,constants.BLACK,index - 27,0.01)
            prompt_ln_3 = render_text_leter_by_leter(prompt_3,constants.BLACK,index - 50,0.01)
            prompt_ln_4 = render_text_leter_by_leter(prompt_4,constants.BLACK,index - 73,0.01)
            prompt_ln_5 = render_text_leter_by_leter(prompt_5,constants.BLACK,index - 94,0.01)
            prompt_ln_6 = render_text_leter_by_leter(prompt_6,constants.BLACK,index - 115,0.01)
            prompt_ln_7 = render_text_leter_by_leter(prompt_7,constants.BLACK,index - 137,0.01)
            
            # screen.blit(font.render(prompt_1,True,constants.BLACK), (400,150))
            screen.blit(prompt_ln_1, (150,150))
            screen.blit(prompt_ln_2, (310,230))
            screen.blit(prompt_ln_3, (305,270))
            screen.blit(prompt_ln_4, (335,310))
            screen.blit(prompt_ln_5, (335,350))
            screen.blit(prompt_ln_6, (327,390))
            screen.blit(prompt_ln_7, (420,430))

            # if index > first_line_len and index < first_line_len + second_line_len + 1:   
            #     prompt_line_2 = font.render(prompt_2[:index-first_line_len], True, constants.BLACK)
            # else:
            #     prompt_line_2 = font.render("", True, constants.BLACK)
            # render_text_letter_by_letter(prompt, screen, font, (100, 100), constants.BLACK, 0.01,n)
        else:
            if pause_game:
                screen.blit(background_image,(0,0))
                if pause_exit_button.draw(screen):
                    run = False
                if options_button.draw(screen):
                    print("otions")   
                if resume_button.draw(screen):
                    pause_game = False
            else:
                screen.blit(game_bg,(0,0))



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

                    for spawner in world.spawner_list:
                        if spawner.alive:
                            new_mob = spawner.spawn()
                            if new_mob:
                                world.enemy_list.append(new_mob)

                world.draw(screen)
                player.draw(screen)    
                for enemy in world.enemy_list:
                    if enemy.alive:
                        enemy.draw(screen)
                weapon.draw(screen)
                arrow,lightning_magic = weapon.update(player)
                if arrow:
                    sound_effects["shot_fx"].play()
                    arrow_group.add(arrow)
                for arrow in arrow_group:
                    damage_text = cacl_damage(arrow)
                    if damage_text:
                        damage_text_group.add(damage_text)
                
                if lightning_magic:
                    lightning_group.add(lightning_magic)
                    
                for lightning in lightning_group:
                    sound_effects["lightning_fx"].play()
                    damage_text = lightning.update(screen,world.enemy_list,screen_scroll,player)

                    if damage_text:
                        damage_text_group.add(damage_text)

                fireball_group.update(player,world.obstacle_tiles,screen_scroll,sound_effects["fire_fx"])
                damage_text_group.update(screen_scroll)
                item_group.update(screen_scroll,player,sound_effects["potion_fx"],sound_effects["coin_fx"])   
                """this is the shooting function and the weapon that fixes itself to the player"""
                
                draw_info()


                """drawing out the different grops"""
                damage_text_group.draw(screen)
                fireball_group.draw(screen)
                item_group.draw(screen)
                # draw_gauge(screen,player.mana)
                if level_complete:
                    start_intro = True
                    moving_down = False
                    moving_right =False
                    moving_left = False
                    moving_up = False
                    merchent(player,weapon,level)
                    level += 1
                    world_data = make_world_data()

                    if level == 3:
                        # ititiate the merchent screen 
                        music.fadeout(1000)
                        music.unload()
                        music.load("assets/audio/Avenged Sevenfold - Nightmare.mp3")
                        music.play(-1,0.0,5000)
                    if level == 6:
                        # ititiate the merchent screen 
                        music.fadeout(1000)
                        music.unload()
                        music.load("assets/audio/Dance With The Devil.mp3")
                        music.play(-1,0.0,5000)
                    world = World()
                    world.process_data(world_data,list_of_tiles,item_image_list,mob_animations,screen,player,sound_effects)
                    player = world.player

                    
                    for item in world.item_list:
                        item_group.add(item)

                    
                
                if start_intro:
                    
                    if screen_fade.fade():
                        start_intro = False
                        screen_fade.fade_counter = 0

                if not player.alive:
                    if death_fade.fade():
                        screen.blit(reaper_image,(450,0))
                        if restart_button.draw(screen):
                            death_fade.fade_counter = 0
                            start_intro =True
                            level = 1
                            world_data = make_world_data()
                            
                            world = World()
                            world.process_data(world_data,list_of_tiles,item_image_list,mob_animations,screen,player,sound_effects)
                            player = world.player
                            player.health = 10
                            player.alive = True
                            for item in world.item_list:
                                item_group.add(item)
                        if main_exit_button.draw(screen):
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

if __name__ == "__main__":
    main()