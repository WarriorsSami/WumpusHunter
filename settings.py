import pygame as pg

# define some common color (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREY = (40, 40, 40)
LIGHT_GREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
LIGHT_GREEN = (0, 255, 0)
BROWN = (106, 55, 5)

# game settings
WIDTH = 1024
HEIGHT = 768
FPS = 60
TITLE = "Wumpus Hunter"
BG_COLOR = BROWN

TILE_SIZE = 64
GRID_WIDTH = WIDTH / TILE_SIZE
GRID_HEIGHT = HEIGHT / TILE_SIZE

# wall settings
WALL_IMG = "PNG\\Tiles\\tile_46.png"

# player settings
PLAYER_SPEED = 330
PLAYER_ROT_SPEED = 250
PLAYER_STAMINA = 100000000
PLAYER_IMG = "PNG\\Man Blue\\manBlue_gun.png"
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
