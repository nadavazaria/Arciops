import pygame
import constants
from character import Player
pygame.init 

# create player


screen = pygame.display.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))

pygame.display.set_caption("Arciops")

clock = pygame.time.Clock()

moving_up = False
moving_down = False
moving_left = False
moving_right = False

def scale_img(image,scale):
    width = image.get_width()
    height = image.get_height()
    return pygame.transform.scale(image,(width*constants.SCALE,height*scale))
     

animation_list = []
animation_types = ["idle","run"]
for animation in animation_types:
    list_of_img = []
    for i in range(4):
        img = pygame.image.load(f"assets/images/characters/elf/{animation}/{i}.png").convert_alpha()
        img = scale_img(img,constants.SCALE)
        list_of_img.append(img)
    #     print("image added")
    # print(list_of_img)
    animation_list.append(list_of_img)


player = Player(100,100,animation_list)

run = True
def key_events(event):
    """checking for keyboard pressing"""
  
    return moving_up,moving_down,moving_left,moving_right

while run:
    clock.tick(constants.FPS)
    screen.fill(constants.BLACK)
    player.draw(screen)    
    dx = 0
    dy = 0
    for event in pygame.event.get():
        # quit game
        if event.type == pygame.QUIT:
            run = False


        if event.type == pygame.KEYDOWN:
        
            if event.key == pygame.K_a:
                moving_left = True

            if event.key == pygame.K_d:
                moving_right =True
                    
            if event.key == pygame.K_s:
                moving_down = True
                    
            if event.key == pygame.K_w:
                moving_up = True
                    
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
               
    if moving_up:
        dy = -constants.SPEED
    if moving_down:
        dy = constants.SPEED
    if moving_left:
        dx = -constants.SPEED
    if moving_right:
        dx = constants.SPEED

                
                   
    player.move(dx,dy)
    player.update()

    pygame.display.update()

pygame.quit()