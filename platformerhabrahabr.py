#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Импортируем библиотеку pygame
import pygame
import sys
import pygame.freetype
from player import *
from blocks import *
from monsters import *



# Объявляем переменные
WIN_WIDTH = 800  # Ширина создаваемого окна
WIN_HEIGHT = 640  # Высота
DISPLAY = (WIN_WIDTH, WIN_HEIGHT)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#AFEEEE"

FILE_DIR = os.path.dirname(__file__)


class Camera(object):
    def __init__(self, camera_func, width, height):
        self.camera_func = camera_func
        self.state = Rect(0, 0, width, height)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect)


def camera_configure(camera, target_rect):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l, t = -l + WIN_WIDTH / 2, -t + WIN_HEIGHT / 2

    l = min(0, l)  # Не движемся дальше левой границы
    l = max(-(camera.width - WIN_WIDTH), l)  # Не движемся дальше правой границы
    t = max(-(camera.height - WIN_HEIGHT), t)  # Не движемся дальше нижней границы
    t = min(0, t)  # Не движемся дальше верхней границы

    return Rect(l, t, w, h)


def loadLevel():
    global playerX, playerY  # объявляем глобальные переменные, это координаты героя

    levelFile = open('%s/levels/1.txt' % FILE_DIR)
    line = " "
    commands = []
    while line[0] != "/":  # пока не нашли символ завершения файла
        line = levelFile.readline()  # считываем построчно
        if line[0] == "[":  # если нашли символ начала уровня
            while line[0] != "]":  # то, пока не нашли символ конца уровня
                line = levelFile.readline()  # считываем построчно уровень
                if line[0] != "]":  # и если нет символа конца уровня
                    endLine = line.find("|")  # то ищем символ конца строки
                    level.append(line[0: endLine])  # и добавляем в уровень строку от начала до символа "|"

        if line[0] != "":  # если строка не пустая
            commands = line.split()  # разбиваем ее на отдельные команды
            if len(commands) > 1:  # если количество команд > 1, то ищем эти команды
                if commands[0] == "player":  # если первая команда - player
                    playerX = int(commands[1])  # то записываем координаты героя
                    playerY = int(commands[2])
                # if commands[0] == "portal": # если первая команда portal, то создаем портал
                #     tp = BlockTeleport(int(commands[1]),int(commands[2]),int(commands[3]),int(commands[4]))
                #     entities.add(tp)
                #     platforms.append(tp)
                #     animatedEntities.add(tp)
                if commands[0] == "saw":  # если первая команда monster, то создаем монстра
                    sn = Saw(int(commands[1]), int(commands[2]), int(commands[3]), int(commands[4]), int(commands[5]),
                             int(commands[6]))
                    entities.add(sn)
                    platforms.append(sn)
                    saw.add(sn)


def terminate():
    pygame.quit()
    sys.exit()


def main():
    loadLevel()
    pygame.init()  # Инициация PyGame, обязательная строчка
    font = pygame.freetype.SysFont("ofont.ru_Montserrat.ttf", 34)
    font.origin = True
    screen = pygame.display.set_mode(DISPLAY)  # Создаем окошко
    pygame.display.set_caption("Save a firend")  # Пишем в шапку
    bg = Surface((WIN_WIDTH, WIN_HEIGHT))  # Создание видимой поверхности
    # будем использовать как фон
    bg.fill(Color(BACKGROUND_COLOR))  # Заливаем поверхность сплошным цветом

    left = right = False  # по умолчанию - стоим
    up = False
    running = False

    hero = Player(playerX, playerY)  # создаем героя по (x,y) координатам
    entities.add(hero)

    timer = pygame.time.Clock()
    x = y = 0  # координаты
    for row in level:  # вся строка
        for col in row:  # каждый символ
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "*":
                sp = SpikeDie(x, y)
                entities.add(sp)
                platforms.append(sp)
            if col == "F":
                fr = Friend(x, y)
                entities.add(fr)
                platforms.append(fr)
                animatedEntities.add(fr)
            if col == "K":
                ke = Key(x, y)
                entities.add(ke)
                keys.append(ke)
                animatedEntities.add(ke)

            x += PLATFORM_WIDTH  # блоки платформы ставятся на ширине блоков
        y += PLATFORM_HEIGHT  # то же самое и с высотой
        x = 0  # на каждой новой строчке начинаем с нуля

    total_level_width = len(level[0]) * PLATFORM_WIDTH  # Высчитываем фактическую ширину уровня
    total_level_height = len(level) * PLATFORM_HEIGHT  # высоту

    camera = Camera(camera_configure, total_level_width, total_level_height)

    while not hero.winner:  # Основной цикл программы
        screen.blit(bg, (0, 0))  # Каждую итерацию необходимо всё перерисовывать
        timer.tick(60)
        for e in pygame.event.get():  # Обрабатываем события
            if e.type == QUIT:
                terminate()

            if e.type == KEYDOWN and e.key == K_UP:
                up = True

            if e.type == KEYDOWN and e.key == K_LEFT:
                left = True
            if e.type == KEYDOWN and e.key == K_RIGHT:
                right = True
            if e.type == KEYDOWN and e.key == K_LSHIFT:
                running = True

            if e.type == KEYUP and e.key == K_UP:
                up = False
            if e.type == KEYUP and e.key == K_RIGHT:
                right = False
            if e.type == KEYUP and e.key == K_LEFT:
                left = False
            if e.type == KEYUP and e.key == K_LSHIFT:
                running = False




        animatedEntities.update()  # показываеaм анимацию
        saw.update(platforms)  # передвигаем всех монстров
        camera.update(hero)  # центризируем камеру относительно персонажа
        hero.update(left, right, up, running, platforms)  # передвижение
        for e in entities:
            screen.blit(e.image, camera.apply(e))
        ticks = pygame.time.get_ticks()
        millis = ticks % 1000
        seconds = int(ticks / 1000 % 60)
        minutes = int(ticks / 60000 % 24)
        out = '{minutes:02d}:{seconds:02d}:{millis}'.format(minutes=minutes, millis=millis, seconds=seconds)
        font.render_to(screen, (100, 100), out, pygame.Color('Black'))
        pygame.display.flip()


    pygame.display.update()  # обновление и вывод всех изменений на экран



def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def start_screen():
    pygame.init()
    size = width, height = 960, 540
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Save a firend")
    clock = pygame.time.Clock()
    FPS = 50
    intro_text = ["Спаси друга!",
                  "",
                  "Выберите уровень:",
                  "Выберите уровень ",
                  "(Номер уровня - цифра на клавиатуре от 1 до 3)"]

    fon = pygame.transform.scale(load_image('fon.jpeg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font("ofont.ru_Montserrat.ttf", 30)
    text_coord = 90
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main()
                    run = False
        pygame.display.flip()
        clock.tick(FPS)


level = []
entities = pygame.sprite.Group()  # Все объекты
animatedEntities = pygame.sprite.Group()  # все анимированные объекты, за исключением героя
saw = pygame.sprite.Group()  # Все передвигающиеся объекты
platforms = []  # то, во что мы будем врезаться или опираться
keys = []
if __name__ == "__main__":
    start_screen()
