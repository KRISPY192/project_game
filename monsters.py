#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pygame import *
import pyganim
import os

SAW_WIDTH = 32
SAW_HEIGHT = 32
MONSTER_COLOR = "#FFFFE0"
ICON_DIR = os.path.dirname(__file__) #  Полный путь к каталогу с файлами


ANIMATION_MONSTERHORYSONTAL = [('%s/saw/s1.png' % ICON_DIR),
                                ('%s/saw/s2.png' % ICON_DIR),
                               ('%s/saw/s3.png' % ICON_DIR),
                               ('%s/saw/s4.png' % ICON_DIR),
                               ('%s/saw/s5.png' % ICON_DIR),
                               ('%s/saw/s6.png' % ICON_DIR),
                               ('%s/saw/s7.png' % ICON_DIR),
                                ('%s/saw/s8.png' % ICON_DIR),
                               ]

class Saw(sprite.Sprite):
    def __init__(self, x, y, left, up, maxLengthLeft, maxLengthUp):
        sprite.Sprite.__init__(self)
        self.image = Surface((SAW_WIDTH, SAW_HEIGHT))
        self.image.fill(Color(MONSTER_COLOR))
        self.rect = Rect(x, y, SAW_WIDTH, SAW_WIDTH)
        self.image.set_colorkey(Color(MONSTER_COLOR))
        self.startX = x # начальные координаты
        self.startY = y
        self.maxLengthLeft = maxLengthLeft # максимальное расстояние, которое может пройти в одну сторону
        self.maxLengthUp= maxLengthUp # максимальное расстояние, которое может пройти в одну сторону, вертикаль
        self.xvel = left # cкорость передвижения по горизонтали, 0 - стоит на месте
        self.yvel = up # скорость движения по вертикали, 0 - не двигается
        boltAnim = []
        for anim in ANIMATION_MONSTERHORYSONTAL:
            boltAnim.append((anim, 0.3))
        self.boltAnim = pyganim.PygAnimation(boltAnim)
        self.boltAnim.play()

    def update(self, platforms): # по принципу героя

        self.image.fill(Color(MONSTER_COLOR))
        self.boltAnim.blit(self.image, (0, 0))

        self.rect.y += self.yvel
        self.rect.x += self.xvel

        self.collide(platforms)

        if (abs(self.startX - self.rect.x) > self.maxLengthLeft):
            self.xvel =-self.xvel  # если прошли максимальное растояние, то идеи в обратную сторону
        if (abs(self.startY - self.rect.y) > self.maxLengthUp):
            self.yvel = -self.yvel # если прошли максимальное растояние, то идеи в обратную сторону, вертикаль

    def collide(self, platforms):
        for p in platforms:
            if sprite.collide_rect(self, p) and self != p: # если с чем-то или кем-то столкнулись
               self.xvel = - self.xvel # то поворачиваем в обратную сторону
               self.yvel = - self.yvel
