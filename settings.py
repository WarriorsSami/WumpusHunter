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
HIT_FLAG_LIFETIME = 300

# define penalties and awards
SHOT_PENALTY = -1
ROT_PENALTY = -1
COLLIDE_WITH_MOB_PENALTY = -1000
TREASURE_AWARD = 1000
SHOT_MOB_AWARD = 10
KILL_MOB_AWARD = 100

# weapons settings
BULLET_IMG = "PNG\\Tiles\\tile_214.png"
WEAPONS = {
    "pistol": {
        "bullet_speed": 500,
        "bullet_lifetime": 1000,
        "rate": 200,
        "kickback": 200,
        "spread": 5,
        "damage": 10,
        "bullet_size": "lg",
        "bullet_count": 1
    },
    "shotgun": {
        "bullet_speed": 500,
        "bullet_lifetime": 1000,
        "rate": 900,
        "kickback": 300,
        "spread": 20,
        "damage": 5,
        "bullet_size": "sm",
        "bullet_count": 12
    }
}
BULLET_LG_WIDTH = 20
BULLET_LG_HEIGHT = 20
BULLET_SM_WIDTH = 10
BULLET_SM_HEIGHT = 10
BARREL_OFFSET = vec(30, 10)

# mob settings
MOB_IMG = "PNG\\Zombie 1\\zoimbie1_hold.png"
MOB_SPEEDS = [150, 100, 75, 125, 200, 150]
MOB_HIT_RECT = pg.Rect(0, 0, 30, 30)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCK_BACK = 20
MOB_AVOID_RADIUS = 50
MOB_FADE_RATE = 10
MOB_DETECT_RADIUS = 600

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

SPLAT_GREEN = "Particles\\PNG (Transparent)\\splat green.png"
SPLAT_RED = "Particles\\PNG (Transparent)\\splat red.png"

DAMAGE_ALPHA = [i for i in range(0, 255, 55)]

# define layers
WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

# define items
ITEM_IMAGES = {
    "health": "PNG\\Items\\health_pack.png",
    "shotgun": "PNG\\Items\\shotgun.png"
}
HEALTH_PACK_AMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = 0.4

# define sounds
BG_MUSIC = "espionage.ogg"
PLAYER_HIT_SOUNDS = ["sound\\pain\\8.wav", "sound\\pain\\9.wav", "sound\\pain\\10.wav", "sound\\pain\\11.wav",
                     "sound\\pain\\12.wav", "sound\\pain\\13.wav", "sound\\pain\\14.wav"]
MOB_HIT_SOUNDS = ["sound\\splat.wav"]
MOB_MOAN_SOUNDS = ["sound\\roar\\zombie-roar-1.wav", "sound\\roar\\zombie-roar-2.wav", "sound\\roar\\zombie-roar-3.wav",
                   "sound\\roar\\zombie-roar-4.wav", "sound\\roar\\zombie-roar-5.wav", "sound\\roar\\zombie-roar-6.wav",
                   "sound\\roar\\zombie-roar-7.wav", "sound\\roar\\zombie-roar-8.wav", "sound\\roar\\zombie-roar-9.wav",
                   "sound\\roar\\zombie-roar-10.wav"]
WEAPON_SOUNDS = {
    "pistol": ["sound\\gun\\pistol.wav"],
    "shotgun": ["sound\\gun\\shotgun.wav"]
}
EFFECTS_SOUNDS = {
    "level_start": "sound\\level_start.wav",
    "health_up": "sound\\health_pack.wav",
    "wall_hit": "sound\\wall_hit.wav",
    "gun_pickup": "sound\\gun\\gun_pickup.wav"
}

# font settings
FLAG_FONT_SIZE = 30
TITLE_FONT_SIZE = 100
