from settings import *


# fill pixels with color preserving alpha
def fill(surface, color):
    w, h = surface.get_size()
    r, g, b = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            surface.set_at((x, y), pg.Color(r, g, b, a))


def collide_hit_rect(one, two):
    return one.hit_rect.colliderect(two.rect)


def collide_with_group(sprite, group, dir_str):
    # check if sprite collides with any sprite in group
    hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
    if hits:
        if dir_str == 'x':
            # collide with obstacle from the left
            if hits[0].rect.centerx > sprite.hit_rect.centerx:
                # hold sprite's position to the left side of the obstacle
                sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
            # collide with obstacle from the right
            if hits[0].rect.centerx < sprite.hit_rect.centerx:
                # hold sprite's position to the right side of the obstacle
                sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
            # init horizontal gliding
            sprite.vel.x = 0
            # update the position of the sprite's collider
            sprite.hit_rect.centerx = sprite.pos.x
        if dir_str == 'y':
            # collide with obstacle from the top
            if hits[0].rect.centery > sprite.hit_rect.centery:
                # hold sprite's position to the top side of the obstacle
                sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
            if hits[0].rect.centery < sprite.hit_rect.centery:
                # hold sprite's position to the bottom side of the obstacle
                sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
            # init vertical gliding
            sprite.vel.y = 0
            # update the position of the sprite's collider
            sprite.hit_rect.centery = sprite.pos.y
