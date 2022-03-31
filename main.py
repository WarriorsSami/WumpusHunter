import sys
from os import path

from entities.camera import Camera

from entities.sprites.player import Player
from entities.sprites.wall import Wall
from entities.sprites.mob import Mob
from entities.sprites.utils import *

from entities.tilemap import TileMap


class Game:
    def __init__(self):
        pg.init()

        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)

        self.all_sprites = None
        self.player = None
        self.player_img = None

        self.wall_img = None
        self.walls = None

        self.mob_img = None
        self.mobs = None

        self.playing = False
        self.dt = None
        self.map = None
        self.camera = None

        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)
        assets_folder = path.join(game_folder, 'assets')
        self.map = TileMap(path.join(game_folder, 'maps/map_extended.txt'))

        self.player_img = pg.image.load(path.join(assets_folder, PLAYER_IMG)).convert_alpha()
        self.mob_img = pg.image.load(path.join(assets_folder, MOB_IMG)).convert_alpha()

        self.wall_img = pg.image.load(path.join(assets_folder, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILE_SIZE, TILE_SIZE))

    def new(self):
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        for row, tiles in enumerate(self.map.data):
            for col, tile in enumerate(tiles):
                if tile == '1':
                    Wall(self, col, row)
                elif tile == 'P':
                    self.player = Player(self, col, row)
                elif tile == 'M':
                    Mob(self, col, row)
        self.camera = Camera(self.map.width, self.map.height)

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
        self.all_sprites.update()
        self.camera.update(self.player)

    def draw_grid(self):
        # draw vertical lines
        for x in range(0, WIDTH, TILE_SIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (x, 0), (x, HEIGHT))

        # draw horizontal lines
        for y in range(0, HEIGHT, TILE_SIZE):
            pg.draw.line(self.screen, LIGHT_GREY, (0, y), (WIDTH, y))

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        self.screen.fill(BG_COLOR)
        # self.draw_grid()
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        # pg.draw.rect(self.screen, WHITE, self.player.hit_rect, 2)
        pg.display.flip()

    def events(self):
        for event in pg.event.get():
            if self.player.score < 0:
                self.quit()
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()

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
