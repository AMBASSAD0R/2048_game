# основной код игры

import random
import sys
import json
import os

import pygame

from functions import empty_positions, beauty_print, index_from_number, add_2_or_4, is_full, move_left, move_right, \
    move_up, move_down, is_move_available, is_available_name

from database import get_best, insert_result

GAMERS_DB = get_best()


def save_game():
    """сохранение игры"""
    data = {
        'user': USERNAME,
        'score': score,
        'field': field
    }

    with open('data.txt', mode='w') as outfile:
        json.dump(data, outfile)


def init_game():
    """инициализация основных данных игры"""
    global score, field

    field = [
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
    ]

    empty = empty_positions(field)
    random.shuffle(empty)
    random_num1 = empty.pop()
    random_num2 = empty.pop()
    x1, y1 = index_from_number(random_num1)
    x2, y2 = index_from_number(random_num2)
    field = add_2_or_4(field, x1, y1)
    field = add_2_or_4(field, x2, y2)

    score = 0


def draw_top_gamers():
    """зарисовка лучших результатов"""
    font_top = pygame.font.SysFont('Arial', 25)
    font_gamer = pygame.font.SysFont('Arial', 20)

    text_head = font_top.render('Best tries: ', True, TEXT_COLOR)

    screen.blit(text_head, (270, 5))

    for index, gamer in enumerate(GAMERS_DB):
        name, score = gamer
        s = f'{index + 1}. {name} - {score}'
        text_gamer = font_gamer.render(s, True, TEXT_COLOR)
        screen.blit(text_gamer, (290, 35 + 25 * index))
        print(index, name, score)


def draw_follow():
    img_inst = pygame.image.load('inst.png')
    img_vk = pygame.image.load('vk.png')
    img_tg = pygame.image.load('tg.png')

    font_follow = pygame.font.SysFont('Arial', 20)

    text_vk = 'vk.com/test'
    text_inst = 'instagaram.com/test'
    text_tg = 'tg.me/test'

    text_follow_inst = font_follow.render(f'Follow us:  {text_inst}', True, INTERFACE_TEXT_COLOR)
    text_follow_vk = font_follow.render(f'                 {text_vk}', True, INTERFACE_TEXT_COLOR)
    text_follow_tg = font_follow.render(f'                 {text_tg}', True, INTERFACE_TEXT_COLOR)

    screen.blit(pygame.transform.scale(img_inst, (20, 20)), (350, 450))
    screen.blit(text_follow_inst, (100, 450))

    screen.blit(pygame.transform.scale(img_vk, (20, 20)), (350, 480))
    screen.blit(text_follow_vk, (100, 480))

    screen.blit(pygame.transform.scale(img_tg, (20, 20)), (350, 510))
    screen.blit(text_follow_tg, (100, 510))


def draw_interface(score, delta=0):
    """отрисовка интерфейса игры"""
    pygame.draw.rect(screen, INTERFACE_TEXT_COLOR, TITLE)

    font = pygame.font.SysFont('Times New Roman', 70)
    font_score = pygame.font.SysFont('Arial', 40)
    font_delta = pygame.font.SysFont('Arial', 20)

    text_score = font_score.render('Score: ', True, TEXT_COLOR)
    text_score_value = font_score.render(f'{score}', True, TEXT_COLOR)

    screen.blit(text_score, (20, 35))
    screen.blit(text_score_value, (150, 35))

    if delta:
        text_delta = font_delta.render(f'+{delta}', True, TEXT_COLOR)
        screen.blit(text_delta, (200, 80))

    beauty_print(field)
    draw_top_gamers()
    for row in range(4):
        for col in range(4):
            value = field[row][col]
            text = font.render(f'{value}', True, pygame.color.Color('BLACK'))
            w = col * BLOCK_SIZE + (col + 1) * MARGIN
            h = row * BLOCK_SIZE + (row + 1) * MARGIN + BLOCK_SIZE
            pygame.draw.rect(screen, COLORS[value], (w, h, BLOCK_SIZE, BLOCK_SIZE))
            if value != 0:
                font_w, font_h = text.get_size()
                text_x = w + (BLOCK_SIZE - font_w) / 2
                text_y = h + (BLOCK_SIZE - font_h) / 2
                screen.blit(text, (text_x, text_y))


def draw_intro():
    """зарисовка вступительного окна игры"""
    img = pygame.image.load('2048.png')

    font_welcome = pygame.font.SysFont('Times New Roman', 50)

    text_welcome = font_welcome.render('Welcome!', True, INTERFACE_TEXT_COLOR)

    text_start = 'Enter your name'

    name = text_start
    is_find_name = False

    while not is_find_name:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.unicode.isalpha():
                    if name == text_start:
                        name = event.unicode
                    else:
                        name += event.unicode
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif event.key == pygame.K_RETURN:
                    if is_available_name(name):
                        global USERNAME
                        USERNAME = name
                        is_find_name = True

        screen.fill(pygame.color.Color('orange'))

        text_name = font_welcome.render(name, True, INTERFACE_TEXT_COLOR)
        rect_name_coordinates = text_name.get_rect()
        rect_name_coordinates.center = screen.get_rect().center

        screen.blit(pygame.transform.scale(img, (200, 200)), (140, 10))
        screen.blit(text_welcome, (140, 220))
        screen.blit(text_name, rect_name_coordinates)

        draw_follow()

        pygame.display.update()

    screen.fill(pygame.color.Color('black'))


def game_loop():
    """логика игры"""
    global score, field

    draw_interface(score)
    pygame.display.update()

    is_field_moved = False

    while is_full(field) or is_move_available(field):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_game()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                delta = 0
                if event.key == pygame.K_LEFT:
                    field, delta, is_field_moved = move_left(field)
                elif event.key == pygame.K_RIGHT:
                    field, delta, is_field_moved = move_right(field)
                elif event.key == pygame.K_UP:
                    field, delta, is_field_moved = move_up(field)
                elif event.key == pygame.K_DOWN:
                    field, delta, is_field_moved = move_down(field)
                elif event.key == pygame.K_ESCAPE:
                    draw_gameover()
                score += delta
                if is_full(field) and is_field_moved:
                    empty = empty_positions(field)
                    random.shuffle(empty)
                    random_num = empty.pop()
                    x, y = index_from_number(random_num)
                    field = add_2_or_4(field, x, y)
                    print(f'Заполнен элемент под помером {random_num}')
                    is_field_moved = False
                draw_interface(score, delta)
                pygame.display.update()


def draw_gameover():
    """зарисовка заключителььного экрана"""
    global USERNAME, GAMERS_DB, field

    img = pygame.image.load('2048.png')

    font_gameover = pygame.font.SysFont('Times New Roman', 50)
    font_help = pygame.font.SysFont('Arial', 20)

    text_help_space = 'Press SPACE to restart game with old name'
    text_help_enter = 'Press ENTER to restart game without old name'

    text_gameover = font_gameover.render('Game over!', True, INTERFACE_TEXT_COLOR)
    text_result_score = font_gameover.render(f'You have {score}', True, INTERFACE_TEXT_COLOR)
    text_help_space = font_help.render(f'{text_help_space}', True, INTERFACE_TEXT_COLOR)
    text_help_enter = font_help.render(f'{text_help_enter}', True, INTERFACE_TEXT_COLOR)

    best_score = GAMERS_DB[0][1]

    if score > best_score:
        text = 'You bit record!!!'
    else:
        text = f'Record is {best_score}'

    text_record = font_gameover.render(text, True, INTERFACE_TEXT_COLOR)

    insert_result(USERNAME, score)

    restart = False

    while not restart:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # после окончания игры при нажатии на 'пробел' рестартим игру,
                    # инициализируем данные и сохраняем старое имя
                    insert_result(USERNAME, score)
                    restart = True
                    init_game()

                elif event.key == pygame.K_RETURN:  # после окончания игры при нажатии на 'enter' рестартим игру,
                    # инициализируем данные и обнуляем старое имя
                    insert_result(USERNAME, score)
                    USERNAME = None
                    restart = True
                    init_game()

        screen.fill(pygame.color.Color('orange'))
        screen.blit(text_gameover, (120, 250))
        screen.blit(text_result_score, (100, 300))
        screen.blit(text_record, (100, 350))
        screen.blit(text_help_space, (30, 500))
        screen.blit(text_help_enter, (30, 530))
        screen.blit(pygame.transform.scale(img, (200, 200)), (140, 10))

        pygame.display.update()

    screen.fill(pygame.color.Color('black'))


"""инициализация переменных"""

score = None
field = None
USERNAME = None

# сохранение и запись результатов в json файл
PATH = os.getcwd()
if 'data.txt' in os.listdir():
    with open('data.txt', mode='r') as file:
        data = json.load(file)
        score = data['score']
        field = data['field']
        USERNAME = data['user']
    full_path = os.path.join(PATH, 'data.txt')
    os.remove(full_path)
else:
    init_game()

TEXT_COLOR = pygame.color.Color('orange')  # цвет надписей в игре

INTERFACE_TEXT_COLOR = pygame.color.Color('white')


# цвета для закраски ячеек
COLORS = {
    0: pygame.color.Color('gray'),
    2: pygame.color.Color('white'),
    4: pygame.color.Color('yellow'),
    8: pygame.color.Color('orange'),
    16: pygame.color.Color('red'),
    32: pygame.color.Color('gold'),
    64: pygame.color.Color('green'),
    128: pygame.color.Color('purple'),
    256: pygame.color.Color('pink'),
    512: pygame.color.Color('tan'),
    1024: pygame.color.Color('peru'),
    2048: pygame.color.Color('maroon'),
    4096: pygame.color.Color('blue'),
    8192: pygame.color.Color('hot pink')
}

# все что относиться к блокам и отрисовке интерфейса и окна игры
BLOCK = 4
BLOCK_SIZE = 110
MARGIN = 10

WIDTH = BLOCK * BLOCK_SIZE + (BLOCK + 1) * MARGIN  # 445
HEIGHT = WIDTH + 110  # 555
TITLE = pygame.Rect(0, 0, WIDTH, 110)  # вверхняя часть окна игры ( там расположены счет и ТОП лучших игроков )

SIZE = WIDTH, HEIGHT  # (445, 555)

# вывод состояния игры в консоль
print(empty_positions(field))
beauty_print(field)

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('2048')


def main():
    """main - функция кода"""
    running = True
    while running:
        if USERNAME is None:
            draw_intro()
        game_loop()
        draw_gameover()


if __name__ == '__main__':
    main()
