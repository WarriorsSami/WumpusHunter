from entities.sprites.effects.i_visual_effect import *
from entities.sprites.utils import fill


class BloodSplash(IVisualEffect):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(60, 80)
        self.image = pg.transform.scale(choice(game.blood_splashes), (size, size))
        fill(self.image, GREEN)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > FLASH_LIFETIME:
            self.kill()

