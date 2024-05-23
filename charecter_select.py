import pandas as pd
import constants
import pygame

pygame.init()

clock = pygame.time.Clock()

# Path to the CSV file
file_path = 'levels/level1_data.csv'
def change_charecter(current_player,chosen_player):
    target_value = current_player
    replacement_value = chosen_player    
    df = pd.read_csv(file_path)
    df.replace(target_value, replacement_value, inplace=True)
    df.to_csv(file_path, index=False)

run = False
while run:
    pass
