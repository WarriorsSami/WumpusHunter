import pygame as pg

from entities.sprites import Player
from settings import WIDTH, HEIGHT


class Camera:
    def __init__(self, width, height):
        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    # display entity relative to camera on the visible screen
    def apply(self, entity):
        return entity.rect.move(self.camera.topleft)

    # update camera position to follow targeted entity
    def update(self, target):
        x = -target.rect.centerx + int(WIDTH / 2)
        y = -target.rect.centery + int(HEIGHT / 2)

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(-(self.width - WIDTH), x)  # right
        y = max(-(self.height - HEIGHT), y)  # bottom

        self.camera = pg.Rect(x, y, self.width, self.height)
