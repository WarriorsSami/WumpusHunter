from entities.sprites.utils import *


class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.mob_img
        self.rect = self.image.get_rect()
        self.hit_rect = MOB_HIT_RECT.copy()
        self.hit_rect.center = self.rect.center
        self.pos = vec(x, y)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        self.health = MOB_HEALTH
        self.health_bar = None

    def update(self):
        # rotate mob to face player
        self.rot = (self.game.player.pos - self.pos).angle_to(vec(1, 0))
        self.image = pg.transform.rotate(self.game.mob_img, self.rot)
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

        # accelerate mob movement towards player
        self.acc = vec(MOB_SPEED, 0).rotate(-self.rot)
        # apply friction
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2

        # apply collision
        self.hit_rect.centerx = self.pos.x
        collide_with_entity(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        collide_with_entity(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.health <= 0:
            self.kill()
            self.game.player.score += KILL_MOB_AWARD

    def draw_health(self):
        if self.health > 2 * MOB_HEALTH / 3:
            col = GREEN
        elif self.health > MOB_HEALTH / 3:
            col = YELLOW
        else:
            col = RED

        width = int(self.rect.width * self.health / MOB_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)

        # draw health bar when mob is damaged for the first time
        if self.health < MOB_HEALTH:
            pg.draw.rect(self.image, col, self.health_bar)
