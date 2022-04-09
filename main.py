import sys
from os import path
from random import random

from entities.camera import Camera
from entities.sprites.effects.blood_scratch import BloodScratch
from entities.sprites.effects.blood_splash import BloodSplash
from entities.sprites.effects.i_visual_effect import IVisualEffect
from entities.sprites.item import Item
from entities.sprites.mob import Mob
from entities.sprites.obstacle import Obstacle
from entities.sprites.player import Player
from entities.sprites.utils import *
from entities.tiled_map import TiledMap


# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0

    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill_percentage = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill_percentage, BAR_HEIGHT)

    if pct > 0.6:
        col = GREEN
    elif pct > 0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf, col, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)


class Game:
    def __init__(self):
        pg.mixer.pre_init(44100, -16, 1, 4096)
        pg.init()
        pg.font.init()

        self.flag_font = None
        self.title_font = None

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

        self.dim_screen = None
        self.all_sprites = None
        self.draw_debug = False

        self.player = None
        self.player_img = None

        self.wall_img = None
        self.walls = None

        self.mob_img = None
        self.mobs = None

        self.bullets_img = {}
        self.bullets = None

        self.playing = False
        self.dt = None
        self.paused = False

        self.map_img = None
        self.map_rect = None
        self.map = None

        self.items = None

        self.camera = None

        self.gun_flashes = []
        self.blood_splashes = []
        self.blood_scratches = []
        self.smoke_clouds = []

        self.splat_green_img = None
        self.splat_red_img = None

        self.item_images = {}

        self.effects_sounds = {}
        self.weapon_sounds = {}
        self.mob_moan_sounds = []
        self.player_hit_sounds = []
        self.mob_hit_sounds = []

        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        assets_folder = path.join(game_folder, 'assets')
        maps_folder = path.join(game_folder, 'maps/tiled_maps')
        music_folder = path.join(assets_folder, 'music')

        self.title_font = path.join(assets_folder, 'fonts/ZOMBIE.ttf')
        self.flag_font = path.join(assets_folder, 'fonts/FLAG.ttf')

        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0, 0, 0, 180))

        self.map = TiledMap(path.join(maps_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        self.player_img = pg.image.load(path.join(assets_folder, PLAYER_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(assets_folder, MOB_IMG)).convert_alpha()

        temp_bullet_img = pg.image.load(path.join(assets_folder, BULLET_IMG)).convert_alpha()
        self.bullets_img['lg'] = pg.transform.scale(temp_bullet_img, (BULLET_LG_WIDTH, BULLET_LG_HEIGHT))
        self.bullets_img['sm'] = pg.transform.scale(temp_bullet_img, (BULLET_SM_WIDTH, BULLET_SM_HEIGHT))

        self.wall_img = pg.image.load(path.join(assets_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILE_SIZE, TILE_SIZE))

        self.splat_green_img = pg.image.load(path.join(assets_folder, SPLAT_GREEN)).convert_alpha()
        self.splat_green_img = pg.transform.scale(self.splat_green_img, (TILE_SIZE, TILE_SIZE))
        self.splat_red_img = pg.image.load(path.join(assets_folder, SPLAT_RED)).convert_alpha()
        self.splat_red_img = pg.transform.scale(self.splat_red_img, (TILE_SIZE, TILE_SIZE))

        # load the assets for visual effects
        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(assets_folder, img)).convert_alpha())
        for img in BLOOD_SPLASHES:
            self.blood_splashes.append(pg.image.load(path.join(assets_folder, img)).convert_alpha())
        for img in BLOOD_SCRATCHES:
            self.blood_scratches.append(pg.image.load(path.join(assets_folder, img)).convert_alpha())
        for img in SMOKE_CLOUDS:
            self.smoke_clouds.append(pg.image.load(path.join(assets_folder, img)).convert_alpha())

        # load the assets for items
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(assets_folder, ITEM_IMAGES[item])).convert_alpha()

        # load sounds and music
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        for sound in EFFECTS_SOUNDS:
            snd = pg.mixer.Sound(path.join(music_folder, EFFECTS_SOUNDS[sound]))
            snd.set_volume(0.4)
            self.effects_sounds[sound] = snd

        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                snd = pg.mixer.Sound(path.join(music_folder, snd))
                snd.set_volume(0.1)
                self.weapon_sounds[weapon].append(snd)

        for sound in MOB_MOAN_SOUNDS:
            snd = pg.mixer.Sound(path.join(music_folder, sound))
            snd.set_volume(0.1)
            self.mob_moan_sounds.append(snd)

        for sound in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(music_folder, sound)))

        for sound in MOB_HIT_SOUNDS:
            snd = pg.mixer.Sound(path.join(music_folder, sound))
            snd.set_volume(0.2)
            self.mob_hit_sounds.append(snd)

    def show_performance(self):
        # display score on screen
        self.draw_text(f'Current Score: {self.player.score}', self.flag_font, FLAG_FONT_SIZE, BLACK, WIDTH - 400, 10)

        # display hit obstacle flag on screen
        color = BLACK if not self.player.hit_obstacle else RED
        self.draw_text(f'W: {self.player.hit_obstacle}', self.flag_font, FLAG_FONT_SIZE, color, WIDTH - 400, 50)

        # display hit mob flag on screen
        color = BLACK if not self.player.hit_mob else RED
        self.draw_text(f'M: {self.player.hit_mob}', self.flag_font, FLAG_FONT_SIZE, color, WIDTH - 260, 50)

        # display hit treasure flag on screen
        color = BLACK if not self.player.hit_treasure else RED
        self.draw_text(f'T: {self.player.hit_treasure}', self.flag_font, FLAG_FONT_SIZE, color, WIDTH - 120, 50)

    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()

        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)
        #         elif tile == 'P':
        #             self.player = Player(self, col, row)
        #         elif tile == 'M':
        #             Mob(self, col, row)

        for tile_object in self.map.tmx_data.objects:
            obj_center = vec(tile_object.x + tile_object.width / 2,
                             tile_object.y + tile_object.height / 2)
            if tile_object.name == 'player':
                self.player = Player(self, obj_center.x, obj_center.y)
            elif tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            elif tile_object.name == 'mob':
                Mob(self, obj_center.x, obj_center.y)
            elif tile_object.name in list(ITEM_IMAGES.keys()):
                Item(self, obj_center, tile_object.name)

        self.camera = Camera(self.map.width, self.map.height)
        self.effects_sounds['level_start'].play()

    def run(self):
        self.playing = True
        pg.mixer.music.play(loops=-1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    @staticmethod
    def quit():
        pg.quit()
        sys.exit()

    def update(self):
        # update all sprites
        self.all_sprites.update()
        self.camera.update(self.player)

        # player hits items
        hits = pg.sprite.spritecollide(self.player, self.items, False)
        for hit in hits:
            if hit.item_type == 'health' and self.player.health < PLAYER_HEALTH:
                hit.kill()
                self.effects_sounds['health_up'].play()
                self.player.add_health(HEALTH_PACK_AMOUNT)
                self.player.hit_treasure = True
                self.player.last_hit_treasure = pg.time.get_ticks()
            elif hit.item_type == 'shotgun' and self.player.weapon != 'shotgun':
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'

        # bullet hits mob
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            if isinstance(hit, Mob):
                hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
                hit.vel = vec(0, 0)
                self.player.score += SHOT_MOB_AWARD
                BloodSplash(self, hit.pos + FLASH_OFFSET)

        # mob hits player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            if random() < 0.8:
                choice(self.player_hit_sounds).play()
            self.player.health -= MOB_DAMAGE
            self.player.score += COLLIDE_WITH_MOB_PENALTY
            BloodScratch(self, self.player.pos + SCRATCH_OFFSET)
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCK_BACK, 0).rotate(-hits[0].rot)
            self.player.hit_mob = True
            self.player.last_hit_mob = pg.time.get_ticks()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def draw_grid(self):
        # draw vertical lines
        for x in range(0, WIDTH, TILE_SIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, HEIGHT))

        # draw horizontal lines
        for y in range(0, HEIGHT, TILE_SIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        # self.screen.fill(BG_COLOR)
        # self.draw_grid()
        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite, Mob):
                sprite.draw_health()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
            if self.draw_debug and not isinstance(sprite, IVisualEffect):
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(sprite.hit_rect), 1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect), 1)
        self.show_performance()
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)

        if self.paused:
            self.screen.blit(self.dim_screen, (0, 0))
            self.draw_text("Paused", self.title_font, TITLE_FONT_SIZE, RED, WIDTH / 2, HEIGHT / 2, align="center")
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_F1:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused

    def show_start_screen(self):
        pass

    def show_go_screen(self):
        pass


g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
