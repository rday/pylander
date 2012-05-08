#!/usr/bin/python

import sys
import math
import glob
import pygame
from pygame.locals import *


class Physics(object):
    '''
        The dimension we operate in controls the math
        we use to determine physics
    '''
    def __init__(self, width, height, gravity=3, speed=2):
        self.height = height
        self.width = width
        self.gravity = gravity
        self.speed = speed

        # The deviance is used to adjust movements based on
        # the frames per second we are getting
        self.dTime = 1
        self.t = 1

    def get_velocity(self, sprite):
        scale_x = math.cos(sprite.angle)
        scale_y = math.sin(sprite.angle)
        return (scale_x, scale_y)

    def move_sprite(self, sprite):
        ''' Make sure we are within the boundries '''
        if sprite.rect.bottom >= self.height:
            sprite.pos_y = sprite.pos_y - sprite.yVelocity
            if sprite.angle >= 180:
                sprite.angle = sprite.angle - 180
            else:
                sprite.angle = sprite.angle + 180
            sprite.yVelocity = -(sprite.yVelocity*0.75)
        if sprite.rect.right >= self.width:
            sprite.rect.right = self.width - 2
            if sprite.angle >= 180:
                sprite.angle = sprite.angle - 180
            else:
                sprite.angle = sprite.angle + 180
            sprite.xVelocity = -(sprite.xVelocity*0.75)
        if sprite.rect.left <= -1:
            sprite.rect.left = 0
            if sprite.angle >= 180:
                sprite.angle = sprite.angle - 180
            else:
                sprite.angle = sprite.angle + 180
            sprite.xVelocity = -(sprite.xVelocity*0.75)

        ''' Apply gravity '''
        sprite.yVelocity = sprite.yVelocity + ((self.dTime*self.gravity) * sprite.mass)

        ''' Move the sprite '''
        sprite.pos_x = sprite.pos_x + (sprite.xVelocity * self.dTime)
        sprite.pos_y = sprite.pos_y + (sprite.yVelocity * self.dTime)
