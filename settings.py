import pygame as pg
from random import randint, uniform, choice

vec = pg.math.Vector2

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
CYAN = (0, 255, 255)

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
PLAYER_HEALTH = 100
PLAYER_SPEED = 330
PLAYER_ROT_SPEED = 250
PLAYER_STAMINA = 1000000
PLAYER_IMG = "PNG\\Man Blue\\manBlue_gun.png"
PLAYER_HIT_RECT = pg.Rect(0, 0, 35, 35)
HIT_MOB_FLAG_LIFETIME = 300

# define penalties and awards
SHOT_PENALTY = -1
ROT_PENALTY = -1
COLLIDE_WITH_MOB_PENALTY = -1000
TREASURE_AWARD = 1000
SHOT_MOB_AWARD = 10
KILL_MOB_AWARD = 100

# gun settings
BULLET_IMG = "PNG\\Tiles\\tile_214.png"
BULLET_SPEED = 500
BULLET_LIFETIME = 800
BULLET_RATE = 150
BULLET_WIDTH = 20
BULLET_HEIGHT = 20
KICKBACK = 200
GUN_SPREAD = 7
BARREL_OFFSET = vec(30, 10)
BULLET_DAMAGE = 10

# mob settings
MOB_IMG = "PNG\\Zombie 1\\zoimbie1_hold.png"
MOB_SPEEDS = [150, 100, 75, 125, 200, 150]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCK_BACK = 20
MOB_AVOID_RADIUS = 50
MOB_FADE_RATE = 10
MOB_DETECT_RADIUS = 400

# define visual effects
MUZZLE_FLASHES = ["PNG\\Puff\\whitePuff15.png", "PNG\\Puff\\whitePuff16.png",
                  "PNG\\Puff\\whitePuff17.png", "PNG\\Puff\\whitePuff18.png"]

BLOOD_SPLASHES = ["Particles\\PNG (Transparent)\\scorch_01.png", "Particles\\PNG (Transparent)\\scorch_02.png",
                  "Particles\\PNG (Transparent)\\scorch_03.png"]
FLASH_OFFSET = vec(-10, 0)
FLASH_LIFETIME = 50

BLOOD_SCRATCHES = ["Particles\\PNG (Transparent)\\scratch_01.png"]
SCRATCH_OFFSET = vec(-15, -5)
SCRATCH_LIFETIME = 100

SMOKE_CLOUDS = ["Particles\\PNG (Transparent)\\smoke_01.png", "Particles\\PNG (Transparent)\\smoke_02.png",
                "Particles\\PNG (Transparent)\\smoke_03.png", "Particles\\PNG (Transparent)\\smoke_04.png",
                "Particles\\PNG (Transparent)\\smoke_05.png", "Particles\\PNG (Transparent)\\smoke_06.png",
                "Particles\\PNG (Transparent)\\smoke_07.png", "Particles\\PNG (Transparent)\\smoke_08.png",
                "Particles\\PNG (Transparent)\\smoke_09.png", "Particles\\PNG (Transparent)\\smoke_10.png"]
CLOUD_LIFETIME = 100

# define layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# define items
ITEM_IMAGES = {"health": "PNG\\Items\\health_pack.png"}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.4
