#!/usr/bin/python

import sys
import math
import glob
import pygame
from pygame.locals import *


class Ship(pygame.sprite.DirtySprite):
    def __init__(self, image, game):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.game = game
        self.speed = 0
        self.mass = 15.0
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.yVelocity = 1.0
        self.xVelocity = 1.0
        self.dirty = 2
        self.collision = False
        self.collision_index = 0
        self.collision_images = []
        images = ['ship-exp1','ship-exp2','ship-exp3','ship-exp4','ship-exp5','ship-exp6','ship-exp7']
        for image in images:
            self.collision_images.append(game.images[image])

    def set_angle(self, angle):
        ''' When the angle changes, our velocities change '''
        self.angle = math.radians(angle)
        (self.xVelocity, self.yVelocity) = self.game.earth.get_velocity(self)

    def update(self):
        ''' Update the sprite's coordinates '''
        self.game.earth.move_sprite(self)
        self.rect.left = self.pos_x
        self.rect.top = self.pos_y

        if self.collision is True:
            if self.speed == 6:
                self.image = self.collision_images[self.collision_index]
                self.collision_index += 1
                if self.collision_index == 7:
                    self.collision = False
                    self.collision_index = 0
                    self.image = self.game.images['ship']

                self.speed = 0
            else:
                self.speed += 1


class Ground(pygame.sprite.DirtySprite):
    def __init__(self, image, dimension):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.dimension = dimension
        self.mass = 1.0
        self.speed = 6
        self.angle = 0.0
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.yVelocity = 0.0
        self.xVelocity = 17.0
        self.dirty = 1
        self.collision = False
        self.collision_index = 0
        self.collision_images = []

    def set_angle(self, angle):
        ''' When the angle changes, our velocities change '''
        self.angle = math.radians(angle)
        (self.xVelocity, self.yVelocity) = self.dimension.earth.get_velocity(self)

    def update(self):
        ''' Update the sprite's coordinates '''
        pass


class Thruster(pygame.sprite.Sprite):
    def __init__(self, image, dimension):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.dimension = dimension
        self.mass = 0.0
        self.angle = 0.0
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.yVelocity = 0.0
        self.xVelocity = 17.0
        self.dirty = 0

    def set_angle(self, angle):
        ''' When the angle changes, our velocities change '''
        pass

    def update(self):
        ''' Update the sprite's coordinates '''
        pass


class LandingPad(pygame.sprite.Sprite):
    def __init__(self, image, dimension):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.dimension = dimension
        self.mass = 0.0
        self.angle = 0.0
        self.pos_x = 0.0
        self.pos_y = 0.0
        self.yVelocity = 0.0
        self.xVelocity = 0.0
        self.dirty = 1

    def set_angle(self, angle):
        ''' When the angle changes, our velocities change '''
        pass

    def update(self):
        ''' Update the sprite's coordinates '''
        pass
