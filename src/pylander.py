#!/usr/bin/python

import os
import sys
import math
import glob
import random
import pygame
from pygame.locals import *
from Dimension import Physics
from Sprites import Ship, Ground, Thruster, LandingPad


class Game(object):
    def __init__(self, screen):
        self.screen = screen
        self.size = (screen.get_rect().width, screen.get_rect().height)
        self.font = pygame.font.SysFont(pygame.font.get_default_font(), 20)
        self.images = {}
        self.sounds = {}

    def write(self, x, y, msg, color=(255,255,255)):
        text = self.font.render(msg, 1, color)
        textpos = text.get_rect()
        textpos.centerx = x
        textpos.centery = y
        self.screen.blit(text, textpos)
        pygame.display.flip()

    def load_sounds(self):
        pygame.mixer.init()
        for sound in glob.glob('sound/*'):
            name = os.path.basename(sound).split('.')[0]
            self.sounds[name] = pygame.mixer.Sound(sound)

    def load_images(self):
        rect = self.screen.get_rect()
        self.write(rect.centerx, rect.centery, 'Loading Images...')
        for image in glob.glob('images/*'):
            name = os.path.basename(image).split('.')[0]
            self.images[name] = pygame.image.load(image).convert_alpha()

    def load_sprites(self):
        rect = self.screen.get_rect()
        self.write(rect.centerx, rect.centery, 'Loading Sprites...')
        self.earth = Physics(self.size[0], self.size[1])
        self.level = self.images['level1']
        self.ground = Ground(self.images['level2-ground'], self)
        self.ground.rect.left = 0
        self.ground.rect.bottom = self.size[1]
        self.ship = Ship(self.images['ship'], self)
        self.ship.set_angle(90.0)
        self.ship.mass = 15.0
        self.left_thrust = Thruster(self.images['left-thrust'], self.earth)
        self.right_thrust = Thruster(self.images['right-thrust'], self.earth)
        self.down_thrust = Thruster(self.images['down-thrust'], self.earth)
        self.landing = LandingPad(self.images['landingpad'], self.earth)
        self.landing.rect.left = 105
        self.landing.rect.top = screen.get_rect().bottom - 105
        self.allsprites = pygame.sprite.LayeredUpdates((self.ground, self.landing, self.ship))
        updates = pygame.sprite.LayeredUpdates()
        self.allsprites.move_to_front(self.landing)
        self.allsprites.move_to_front(self.ship)

        '''
        Part of the resizing, comment out for now
        self.allsprites.add(self.left_thrust)
        self.allsprites.add(self.right_thrust)
        self.allsprites.add(self.down_thrust)'''

    def resize(self, size):
        return
        orig_w = self.screen.get_rect().width
        orig_h = self.screen.get_rect().height
        self.screen = pygame.display.set_mode( size, RESIZABLE )
        level_rect = self.level.get_rect()
        level_rect.width = size[0]
        level_rect.height = size[1]
        self.screen.blit(self.level, (0,0))

        for sprite in self.allsprites:
            print sprite
            image = sprite.image
            rect = image.get_rect()
            print "orig w %d rect width %d" % (orig_w, rect.width)
            pct_h = float(rect.height) / float(orig_h)
            new_h = int(size[1] * pct_h)
            pct_w = float(rect.width) / float(orig_w)
            new_w = int(size[0] * pct_w)
            print "New %d %d" % (new_w, new_h)
            newimage = pygame.transform.scale(image, (new_w, new_h))
            self.images[image] = newimage
            sprite.image = newimage
            sprite.rect = newimage.get_rect()
            sprite.rect.centerx = rect.centerx
            sprite.rect.centery = rect.centery
                        
        '''ground_rect = self.ground.rect
        pct = float(ground_rect.height) / float(orig_h)
        new_h = int(ground_rect.height * pct)
        print "gh / orig_h = pct %d %d %f %d" % (ground_rect.height, orig_h, pct, new_h)
        self.images['level1-ground'] = newground
        self.ground.image = self.images['level1-ground']
        self.ground.rect = self.ground.image.get_rect()
        ground_rect = self.ground.rect
        ground_rect.left = 0
        ground_rect.bottom = ev.h
        ground_rect.width = ev.w'''

    def play(self):
        self.load_sounds()
        self.load_images()
        self.load_sprites()
        while True:
            sound = self.sounds[random.choice(self.sounds.keys())]
            sound.play()
            self._play()
            sound.fadeout(500)


    def _play(self):
        screen_rect = self.screen.get_rect()
        self.resize((screen_rect.left, screen_rect.top))
        fuel = 2000
        fuelgadge_rect = pygame.Rect(screen_rect.right - 30, screen_rect.top + 5, 15, 104) 
        fuel_rect = pygame.Rect(screen_rect.right - 28, screen_rect.top + 7, 12, 100) 
        clock = pygame.time.Clock()
        optimal = 40
        frames = 0
        fps = 0
        self.screen.blit(self.level, (0,0))
        self.ship.xVelocity = 1.0
        self.ship.yVelocity = 1.0
        self.ship.pos_x = 100
        self.ship.pos_y = 100
        self.ship.rect.left = 100
        self.ship.rect.top = 100
        self.ship.collision = False
        self.ship.bottom_thruster = False
        self.ship.left_thruster = False
        self.ship.right_thruster = False
        playing = True

        while True:
            # Don't go above our optimal fps
            dT = clock.tick(optimal)
            self.screen.blit(self.level, self.ship.rect, self.ship.rect)

            if playing is True:
                if self.ship.bottom_thruster is True:
                    if fuel > 0:
                        self.ship.yVelocity = self.ship.yVelocity - 4
                        fuel -= 4
                        self.screen.blit(self.level, self.down_thrust.rect, self.down_thrust.rect)
                        self.down_thrust.rect.centerx = self.ship.rect.centerx
                        self.down_thrust.rect.top = self.ship.rect.bottom - 30
                        self.down_thrust.dirty = 1
                if self.ship.left_thruster is True:
                    if fuel > 0:
                        self.ship.xVelocity = self.ship.xVelocity + 2
                        fuel -= 2
                        self.screen.blit(self.level, self.left_thrust.rect, self.left_thrust.rect)
                        self.left_thrust.rect.right = self.ship.rect.left
                        self.left_thrust.rect.centery = self.ship.rect.centery
                        self.left_thrust.dirty = 1
                if self.ship.right_thruster is True:
                    if fuel > 0:
                        self.ship.xVelocity = self.ship.xVelocity - 2
                        fuel -= 2
                        self.screen.blit(self.level, self.right_thrust.rect, self.right_thrust.rect)
                        self.right_thrust.rect.left = self.ship.rect.right
                        self.right_thrust.rect.centery = self.ship.rect.centery
                        self.right_thrust.dirty = 1

            for ev in pygame.event.get():
                if ev.type is QUIT or (ev.type is KEYDOWN and ev.key == K_q):
                    sys.exit()
                if ev.type is VIDEORESIZE:
                    self.resize(ev.size)

                if ev.type is KEYUP and ev.key == K_UP:
                    self.ship.bottom_thruster = False
                    self.allsprites.remove(self.down_thrust)
                if ev.type is KEYDOWN and ev.key == K_UP:
                    self.ship.bottom_thruster = True
                    self.allsprites.add(self.down_thrust)
                    self.down_thrust.rect.centerx = self.ship.rect.centerx
                    self.down_thrust.rect.top = self.ship.rect.bottom - 30

                if ev.type is KEYUP and ev.key == K_LEFT:
                    self.ship.right_thruster = False
                    self.screen.blit(self.level, self.right_thrust.rect, self.right_thrust.rect)
                    self.allsprites.remove(self.right_thrust)
                if ev.type is KEYDOWN and ev.key == K_LEFT:
                    self.ship.right_thruster = True
                    self.allsprites.add(self.right_thrust)
                    self.right_thrust.rect.left = self.ship.rect.right
                    self.right_thrust.rect.centery = self.ship.rect.centery

                if ev.type is KEYUP and ev.key == K_RIGHT:
                    self.ship.left_thruster = False
                    self.screen.blit(self.level, self.left_thrust.rect, self.left_thrust.rect)
                    self.allsprites.remove(self.left_thrust)
                if ev.type is KEYDOWN and ev.key == K_RIGHT:
                    self.ship.left_thruster = True
                    self.allsprites.add(self.left_thrust)
                    self.left_thrust.rect.right = self.ship.rect.left
                    self.left_thrust.rect.centery = self.ship.rect.centery

                if playing is False:
                    if ev.type is MOUSEBUTTONDOWN:
                        if self.again_rect.collidepoint(ev.pos) == 1:
                            self.screen.blit(self.win, self.win_rect, self.win_rect)
                            self.screen.blit(self.again, self.again_rect, self.again_rect)
                            self.screen.blit(self.quit, self.quit_rect, self.quit_rect)
                            pygame.display.flip()
                            return
                        if self.quit_rect.collidepoint(ev.pos) == 1:
                            sys.exit()

            if pygame.sprite.collide_mask(self.ship, self.landing) and self.ship.yVelocity <= 1.6:
                rect = self.screen.get_rect()
                playing = False
                self.ship.xVelocity = 0
                self.ship.yVelocity = 0
                self.win = self.images['youvelanded']
                self.again = self.images['playagain']
                self.quit = self.images['quit']
                self.win_rect = self.win.get_rect()
                self.win_rect.centerx = screen_rect.centerx
                self.win_rect.centery = screen_rect.centery-200
                self.again_rect = self.again.get_rect()
                self.again_rect.centerx = screen_rect.centerx-200
                self.again_rect.centery = screen_rect.centery-20
                self.quit_rect = self.quit.get_rect()
                self.quit_rect.centerx = screen_rect.centerx+200
                self.quit_rect.centery = screen_rect.centery-20
                self.screen.blit(self.win, self.win_rect)
                self.screen.blit(self.again, self.again_rect)
                self.screen.blit(self.quit, self.quit_rect)
            elif pygame.sprite.collide_mask(self.ship, self.ground):
                self.write(screen_rect.centerx, screen_rect.centery, 'You lose!....')
                self.ship.collision = True
                playing = False
                self.ship.xVelocity = 0
                self.ship.yVelocity = 0

            self.allsprites.update()
            self.allsprites.draw(self.screen)
            pygame.display.flip()
            pygame.draw.rect(self.screen, (255,255,255), fuelgadge_rect, 2)
            pygame.draw.rect(self.screen, (0,0,0), fuel_rect, 0)
            fuel_rect.height = fuel / 20
            fuel_rect.bottom = fuelgadge_rect.bottom - 1
            pygame.draw.rect(self.screen, (255,0,0), fuel_rect, 0)
            frames = frames + 1
            self.earth.dTime = dT / 1000.0
            '''fps = 1000.0 / dT
            if frames % 120 == 0:
                print "FPS %d" % fps
                print "X/Y %d/%d" % (ship.xVelocity, ship.yVelocity)'''


if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode( (1024,768), RESIZABLE )
    game = Game(screen)
    game.play()
