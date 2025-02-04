import os
import sys
import pygame

width = 800  # Ширина создаваемого окна
height = 640  # Высота
size = (width, height)  # Группируем ширину и высоту в одну переменную
BACKGROUND_COLOR = "#000000"
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
FPS = 50


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["Перемещение героя",
                  "",
                  "Герой двигается",
                  "Выберите уровень:",
                  "Выберите уровень (Номер уровня - цифра на клавиатуре от 1 до 3)"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)
    level = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    level = 1
                    continue
                napr = (0, 0)
                if event.key == pygame.K_w:
                    napr = (0, -1)
                if event.key == pygame.K_a:
                    napr = (-1, 0)
                if event.key == pygame.K_s:
                    napr = (0, 1)
                if event.key == pygame.K_d:
                    napr = (1, 0)
                # управление персом
                # player.move_player(napr)
            # if level == 1:
            # all_sprites.draw(screen)
            # player_group.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == '__main__':
    start_screen()
