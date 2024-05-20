import pygame
import constants
from character import Player
from items import Item

class World():
    def __init__(self):
        self.map_tiles = []
        self.obstacle_tiles = []
        self.exit_tile = None
        self.item_list = []
        self.enemy_list = []
        self.player = None
        
    def process_data(self,data,tile_list,item_image_list,mob_animations,surface):
        self.item_image_list = item_image_list
        self.mob_animations = mob_animations
        self.level_length = len(data)
        """go thrugh the data that is a 150X150 matrix"""
        for y,row in enumerate(data):
        
            for x,tile in enumerate(row):
                image = tile_list[tile]
                image_rect = image.get_rect()
                image_x = x*constants.TILE_SIZE 
                image_y = y*constants.TILE_SIZE  
                image_rect.center = (image_x ,image_y )
                tile_data = [image,image_rect,image_x,image_y]
                """add to the main list of world tiles """
                if tile == constants.WALL:
                    self.obstacle_tiles.append(tile_data)
                elif tile == constants.EXIT:
                    self.exit_tile = tile_data  
                elif tile == constants.TILE_COIN:
                    coin = Item(image_x  ,image_y  ,constants.COIN,self.item_image_list)
                    tile_data[0] = tile_list[0]
                    self.item_list.append(coin)
                elif tile == constants.TILE_POTION_RED:
                    red_potion = Item(image_x,image_y ,constants.POTION_RED,self.item_image_list)
                    tile_data[0] = tile_list[0]
                    self.item_list.append(red_potion)

                elif tile == constants.TILE_IMP:
                    imp =  Player(image_x,image_y,70,self.mob_animations,constants.IMP)
                    tile_data[0] = tile_list[0]
                    self.enemy_list.append(imp)
                elif tile == constants.TILE_GOBLIN:
                    goblin =  Player(image_x,image_y,150,self.mob_animations,constants.GOBLIN)
                    tile_data[0] = tile_list[0]
                    self.enemy_list.append(goblin)
                elif tile == constants.TILE_SKELETON:
                    skeleton =  Player(image_x ,image_y,250,self.mob_animations,constants.SKELETON)
                    tile_data[0] = tile_list[0]
                    self.enemy_list.append(skeleton)
                elif tile == constants.TILE_MUDDY:
                    muddy =  Player(image_x,image_y ,150,self.mob_animations,constants.MUDDY)
                    tile_data[0] = tile_list[0]
                    self.enemy_list.append(muddy)
                elif tile == constants.TILE_TINY_ZOMBIE:
                    tiny_zombie =  Player(image_x,image_y,150,self.mob_animations,constants.TINY_ZOMBIE)
                    tile_data[0] = tile_list[0]
                    self.enemy_list.append(tiny_zombie)
                elif tile == constants.TILE_BIG_DEMON:
                    big_demon =  Player(image_x,image_y,1500,self.mob_animations,constants.BIG_DEMON)
                    tile_data[0] = tile_list[0]
                    self.enemy_list.append(big_demon)
                elif tile == constants.TILE_ELF:
                    player = Player(image_x ,image_y ,100,self.mob_animations,constants.ELF)
                    self.player = player
                    tile_data[0] = tile_list[0]
                if tile >= 0: 
                    self.map_tiles.append(tile_data)
                    

    def draw(self,surface):
        for tile in self.map_tiles:
            surface.blit(tile[0],(tile[2] -24,tile[3]-24))

    def update(self,screen_scroll):
        for tile in self.map_tiles:
            tile[2] += screen_scroll[0] 
            tile[3] += screen_scroll[1] 
            tile[1].center = (tile[2],tile[3])
