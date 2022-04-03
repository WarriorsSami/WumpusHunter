from entities.sprites.utils import *


class Item(pg.sprite.Sprite):
    def __init__(self, game, pos, item_type):
        self._layer = ITEMS_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[item_type]
        self.rect = self.image.get_rect()
        self.item_type = item_type
        self.rect.center = pos