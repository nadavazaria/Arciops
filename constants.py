FPS = 60





"""image constatns"""

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCALE = 3
POTION_SCALE = 2
ITEM_SCALE = 3
BUTTON_SCALE = 2.5
WHEAPON_SCALE = 1.5



"""color constants"""
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
MENU_BG = (50,50,50)
PINK = (255,0,255)
WHITE = (255,255,255)
EXP_COLOR = (165, 210, 4)

"""world constatnts """
SPEED = 5
ENEMY_SPEED = 3
RANGE = 40
ATT_RANGE = 55


SCROLL_THRESHOLD =250


"""charecter type constants"""

ELF = 0
GOBLIN = 1
IMP = 2
MUDDY = 3
SKELETON = 4
TINY_ZOMBIE = 5
BIG_DEMON = 6
BIG_ZOMBIE = 7
CHORT = 8
DOCC = 9
ELF_F = 10
GOBLIN_WARRIOR = 11
GOBLIN_SHAMAN = 12
KNIGHT = 13
NECROMANCER = 14
OGRE = 15
PUMPKIN = 16
SLUG = 17 
SWAMPY = 18
WOGOL = 19
WIZARD = 20
mob_types = ["elf","goblin","imp","muddy","skeleton","tiny_zombie","big_demon","big_zombie","chort","docc","elf_f","goblin_warrior",
             'goblin_shamen',"Knight","necromancer","pumpkin","slug","swampy","wogol","wizard"]

"""item type constants """
COIN = 0
POTION_RED = 1
POTION_BLUE = 2
POTION_YELLOW = 3
POTION_YELLOW_BIG = 4
KEY = 5

"""tile constants FLOOR and WALL tiles"""

TILE_SIZE =16 * SCALE
TILE_TYPES = 70
ROWS = 150
COLS = 150

FLOOR_NEW = 0
FLOOR_CRACKED1 = 1
FLOOR_CRACKED2 = 2
FLOOR_BROKE1 = 3
FLOOR_BROKE2 = 4
FLOOR_BROKE3 = 5
FLOOR_BROKE4 = 6
WALL = 7
FLAG_BLUE = 8
FLAG_GREEN = 9
FLAG_RED = 10
FLAG_YELLOW = 11
WALL_OOZE =12
FLOOR_OOZE = 13
FLOOR_RED_HOLE1 = 38
FLOOR_RED_HOLE2 = 39
FLOOR_RED = 40
FLOOR_RED_BROKEN = 41
LAVA_WALL = 42
LAVA_POOL = 43
MOSS_WALL = 44
OOZE_POOL1 = 45
OOZE_POOL2 = 46
OOZE_POOL3 = 47
OOZE_POOL4 = 48
OOZE_POOL5 = 49
TILE_CHECKER_PATTERN_0 = 50
TILE_CHECKER_PATTERN_1 = 51
TILE_CHECKER_PATTERN_2 = 52
TILE_CHECKER_PATTERN_3 = 53
TILE_CHECKER_PATTERN_4 = 54
TILE_CHECKER_PATTERN_5 = 55
TILE_CHECKER_PATTERN_6 = 56
TILE_CHECKER_PATTERN_7 = 57
TILE_CHECKER_PATTERN_8 = 58
TILE_CHECKER_PATTERN_9 = 61
WALL_LAVA_DUN = 59
WALL_LAVA_BRIGHT = 60
WALL_LAVA_POOL = 67
TILE_LAVA_POOL = 66
FLOOR_BLACK_1 = 63
FLOOR_BLACK_2 = 64
FLOOR_SILVER = 62
TILE_DOOR = 69

"""ITEM constants"""
TILE_COIN = 14
TILE_POTION_RED = 15
TILE_POTION_BLUE = 16
TILE_KEY = 68

"""CHARECTER tile constants"""

TILE_ELF = 17
TILE_ELF_F = 18
TILE_KNIGHT = 19
TILE_SKELETON = 20
TILE_TINY_ZOMBIE = 21
TILE_MUDDY = 22
TILE_SWAMPY = 23
TILE_GOBLIN = 24
TILE_GOBLIN_WARRIOR = 25
TILE_GOBLIN_SHAMAN = 26
TILE_OGRE = 27
TILE_SLUG = 28
TILE_DOCC = 29
TILE_PUMPKIN = 30
TILE_NECROMANCER = 31
TILE_BIG_ZOMBIE = 32
TILE_IMP = 33
TILE_WOGOL = 34
TILE_CHORT = 35
TILE_BIG_DEMON = 36

EXIT = 37
EXIT_2 = 65