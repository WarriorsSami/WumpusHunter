from entities.sprites.utils import *


class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        # because obstacles are used only as colliders,
        # we keep them into an invisible group
        self._layer = WALL_LAYER
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
