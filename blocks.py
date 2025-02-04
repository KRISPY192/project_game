#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import os
import pyganim

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32
PLATFORM_COLOR = "#000000"
ICON_DIR = os.path.dirname(__file__)  # Полный путь к каталогу с файлами

ANIMATION_KEY = [
    ('%s/blocks/portal2.png' % ICON_DIR),
    ('%s/blocks/portal1.png' % ICON_DIR)]

ANIMATION_FRIEND = [
    ('%s/blocks/h1.png' % ICON_DIR),
    ('%s/blocks/h2.png' % ICON_DIR),
    ('%s/blocks/h3.png' % ICON_DIR),
    ('%s/blocks/h4.png' % ICON_DIR),
    ('%s/blocks/h5.png' % ICON_DIR),
    ('%s/blocks/h6.png' % ICON_DIR),
    ('%s/blocks/h7.png' % ICON_DIR),
    ('%s/blocks/h8.png' % ICON_DIR),
    ]


class Platform(sprite.Sprite):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/blocks/platform.png" % ICON_DIR)
        self.image.set_colorkey(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)


class SpikeDie(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        self.image = image.load("%s/blocks/ship.png" % ICON_DIR)


class Key(Platform):
    def __init__(self, x, y):
        sprite.Sprite.__init__(self)
        self.image = Surface((PLATFORM_WIDTH, PLATFORM_HEIGHT))
        self.image.fill(Color(PLATFORM_COLOR))
        self.image = image.load("%s/blocks/key.png" % ICON_DIR)
        self.image.set_colorkey(Color(PLATFORM_COLOR))
        self.rect = Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
        # Platform.__init__(self, x, y)
        # boltAnim = []
        # for anim in ANIMATION_KEY:
        #     boltAnim.append((anim, 0.3))
        # self.boltAnim = pyganim.PygAnimation(boltAnim)
        # self.boltAnim.play()



# class Key(Platform):
#     def __init__(self, x, y):
#         Platform.__init__(self, x, y)
#         self.image = image.load("%s/blocks/portal2.png" % ICON_DIR)


class Friend(Platform):
    def __init__(self, x, y):
        Platform.__init__(self, x, y)
        boltAnim = []
        for anim in ANIMATION_FRIEND:
            boltAnim.append((anim, 0.8))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self):
        self.image.fill(Color(PLATFORM_COLOR))
        self.boltAnim.blit(self.image, (0, 0))
