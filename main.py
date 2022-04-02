import sys
from os import path

from entities.camera import Camera

from entities.sprites.player import Player
from entities.sprites.mob import Mob
from entities.sprites.obstacle import Obstacle
from entities.sprites.effects.i_visual_effect import IVisualEffect
from entities.sprites.effects.blood_splash import BloodSplash
from entities.sprites.effects.blood_scratch import BloodScratch
from entities.sprites.utils import *

from entities.tiled_map import TiledMap


# HUD functions
def draw_player_health(surf, x, y, pct):
    if pct < 0:
        pct = 0

    BAR_LENGTH = 100
    BAR_HEIGHT = 20
    fill = pct * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)

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
        pg.init()
        pg.font.init()
        self.font = pg.font.SysFont('Comic Sans MS', 30)
        self.score_text_rect = None

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

        self.all_sprites = None
        self.draw_debug = False

        self.player = None
        self.player_img = None

        self.wall_img = None
        self.walls = None

        self.mob_img = None
        self.mobs = None

        self.bullet_img = None
        self.bullets = None

        self.playing = False
        self.dt = None

        self.map_img = None
        self.map_rect = None
        self.map = None

        self.camera = None

        self.gun_flashes = []
        self.blood_splashes = []
        self.blood_scratches = []

        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        assets_folder = path.join(game_folder, 'assets')
        maps_folder = path.join(game_folder, 'maps/tiled_maps')

        self.map = TiledMap(path.join(maps_folder, 'level1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        self.player_img = pg.image.load(path.join(assets_folder, PLAYER_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(assets_folder, MOB_IMG)).convert_alpha()

        self.bullet_img = pg.image.load(path.join(assets_folder, BULLET_IMG)).convert_alpha()
        self.bullet_img = pg.transform.scale(self.bullet_img, (BULLET_WIDTH, BULLET_HEIGHT))

        self.wall_img = pg.image.load(path.join(assets_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILE_SIZE, TILE_SIZE))

        for img in MUZZLE_FLASHES:
            self.gun_flashes.append(pg.image.load(path.join(assets_folder, img)).convert_alpha())
        for img in BLOOD_SPLASHES:
            self.blood_splashes.append(pg.image.load(path.join(assets_folder, img)).convert_alpha())
        for img in BLOOD_SCRATCHES:
            self.blood_scratches.append(pg.image.load(path.join(assets_folder, img)).convert_alpha())

    def show_score(self):
        self.screen.blit(self.score_text_rect, (WIDTH - 400, 10))

    def new(self):
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()

        # for row, tiles in enumerate(self.map.data):
        #     for col, tile in enumerate(tiles):
        #         if tile == '1':
        #             Wall(self, col, row)
        #         elif tile == 'P':
        #             self.player = Player(self, col, row)
        #         elif tile == 'M':
        #             Mob(self, col, row)

        for tile_object in self.map.tmx_data.objects:
            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x, tile_object.y)
            elif tile_object.name == 'wall':
                Obstacle(self, tile_object.x, tile_object.y, tile_object.width, tile_object.height)
            elif tile_object.name == 'mob':
                Mob(self, tile_object.x, tile_object.y)

        self.camera = Camera(self.map.width, self.map.height)
        self.draw_debug = False
        self.score_text_rect = self.font.render(f'Current score: {self.player.score}', True, LIGHT_GREEN, BROWN)

    def run(self):
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
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
        # display score on screen
        self.score_text_rect = self.font.render(f'Current score: {self.player.score}', True, LIGHT_GREEN, BROWN)
        # bullet hits mob
        hits = pg.sprite.groupcollide(self.mobs, self.bullets, False, True)
        for hit in hits:
            if isinstance(hit, Mob):
                hit.health -= BULLET_DAMAGE
                hit.vel = vec(0, 0)
                self.player.score += SHOT_MOB_AWARD
                BloodSplash(self, hit.pos + FLASH_OFFSET)

        # mob hits player
        hits = pg.sprite.spritecollide(self.player, self.mobs, False, collide_hit_rect)
        for hit in hits:
            self.player.health -= MOB_DAMAGE
            self.player.score += COLLIDE_WITH_MOB_PENALTY
            BloodScratch(self, self.player.pos + SCRATCH_OFFSET)
            hit.vel = vec(0, 0)
            if self.player.health <= 0:
                self.playing = False
        if hits:
            self.player.pos += vec(MOB_KNOCK_BACK, 0).rotate(-hits[0].rot)

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
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        self.show_score()
        draw_player_health(self.screen, 10, 10, self.player.health / PLAYER_HEALTH)
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
