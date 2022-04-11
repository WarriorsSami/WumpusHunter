from itertools import chain
from random import random

from entities.sprites.bullet import Bullet
from entities.sprites.effects.muzzle_flash import MuzzleFlash
from entities.sprites.effects.smoke_cloud import SmokeCloud
from entities.sprites.utils import *


class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        self.hit_rect = PLAYER_HIT_RECT
        self.hit_rect.center = self.rect.center

        self.vel = vec(0, 0)
        self.pos = vec(x, y)
        self.rot_speed = 0
        self.rot = 0

        self.last_shot = 0
        self.score = PLAYER_STAMINA
        self.health = PLAYER_HEALTH
        self.damaged = False
        self.damaged_alpha = None

        self.hit_obstacle = False
        self.hit_mob = False
        self.last_hit_mob = 0
        self.hit_treasure = False
        self.last_hit_treasure = 0

        self.main_weapon = 'pistol'
        self.available_weapons = ['pistol']

    def get_keys(self):
        self.rot_speed = 0
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        if self.score > 0:
            if keys[pg.K_LEFT] or keys[pg.K_a]:
                self.rot_speed = PLAYER_ROT_SPEED
                self.score += ROT_PENALTY
            if keys[pg.K_RIGHT] or keys[pg.K_d]:
                self.rot_speed = -PLAYER_ROT_SPEED
                self.score += ROT_PENALTY
            if keys[pg.K_UP] or keys[pg.K_w]:
                self.vel = vec(PLAYER_SPEED, 0).rotate(-self.rot)
            if keys[pg.K_DOWN] or keys[pg.K_s]:
                self.vel = vec(-PLAYER_SPEED / 2, 0).rotate(-self.rot)
        # shoot
        if keys[pg.K_SPACE]:
            self.shoot()

        if self.vel.x != 0 and self.vel.y != 0:
            self.vel.x *= 0.7071
            self.vel.y *= 0.7071

    def hit(self):
        self.damaged = True
        self.damaged_alpha = chain(DAMAGE_ALPHA * 3)

    def switch_weapon(self):
        if len(self.available_weapons) > 1:
            self.game.effects_sounds['gun_pickup'].play()
        self.main_weapon = self.available_weapons[(
            self.available_weapons.index(self.main_weapon) + 1)
            % len(self.available_weapons)]

    def add_weapon(self, weapon):
        self.main_weapon = weapon
        self.available_weapons.append(weapon)

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > WEAPONS[self.main_weapon]['rate']:
            self.last_shot = now
            dir_vec = vec(1, 0).rotate(-self.rot)
            pos = self.pos + BARREL_OFFSET.rotate(-self.rot)
            self.vel = vec(-WEAPONS[self.main_weapon]['kickback'], 0).rotate(-self.rot)

            for _ in range(WEAPONS[self.main_weapon]['bullet_count']):
                self.score += SHOT_PENALTY
                spread = uniform(-WEAPONS[self.main_weapon]['spread'], WEAPONS[self.main_weapon]['spread'])
                Bullet(self.game, pos, dir_vec.rotate(spread), WEAPONS[self.main_weapon]['damage'])
                snd = choice(self.game.weapon_sounds[self.main_weapon])
                if snd.get_num_channels() >= 2:
                    snd.stop()
                snd.play()

            MuzzleFlash(self.game, pos)

    def update(self):
        self.get_keys()
        if pg.time.get_ticks() - self.last_hit_mob > HIT_FLAG_LIFETIME:
            self.hit_mob = False
        if pg.time.get_ticks() - self.last_hit_treasure > HIT_FLAG_LIFETIME:
            self.hit_treasure = False

        # apply rotation and linear velocity
        self.rot = (self.rot + self.rot_speed * self.game.dt) % 360
        self.image = pg.transform.rotate(self.game.player_img, self.rot)
        if self.damaged:
            try:
                self.image.fill((255, 255, 255, next(self.damaged_alpha)), special_flags=pg.BLEND_RGBA_MULT)
            except StopIteration:
                self.damaged = False
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt

        # apply collision
        self.hit_obstacle = False
        self.hit_rect.centerx = self.pos.x
        self.hit_obstacle = collide_with_group(self, self.game.walls, 'x')
        self.hit_rect.centery = self.pos.y
        self.hit_obstacle = collide_with_group(self, self.game.walls, 'y')
        self.rect.center = self.hit_rect.center
        if self.hit_obstacle:
            if random() < 0.1:
                self.game.effects_sounds['wall_hit'].play()
            SmokeCloud(self.game, self.pos)

    def add_health(self, amount):
        self.health += amount
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH
