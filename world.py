import pygame
import constants
from items import Item

class World():
    def __init__(self):
        self.map_tiles = []
        self.obstacle_tiles = []
        self.exit_tile = None
    def process_data(self,data,tile_list,item_image_list):
        self.item_image_list = item_image_list
        self.level_length = len(data)
        """go thrue the data """

        for y,row in enumerate(data):
        
            for x,tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x*constants.TILE_SIZE
                image_y = y*constants.TILE_SIZE
                image_rect.center = (image_x,image_y)
                tile_data = [image,image_rect,image_x,image_y]
                """add to the main list of world tiles """
                if tile >= 0: 
                    self.map_tiles.append(tile_data)
                if tile == 7:
                    self.obstacle_tiles.append(tile_data)
                elif tile == 8:
                    self.exit_tile = tile_data  
                elif tile == 9:
                    coin = Item(image_x,image_y,0,)
                    

    def draw(self,surface):
        for tile in self.map_tiles:
            surface.blit(tile[0],tile[1].center)

    def update(self,screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0] 
            tile[3] += screen_scroll[1] 
            tile[1].center = (tile[2],tile[3])
