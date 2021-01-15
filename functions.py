# вспомогаительные функции для игры - логика

import copy
import random


def beauty_print(mas):
    """красивый вывод в консоль"""
    print('-' * 10)
    for row in mas:
        print(*row)
    print('-' * 10)


def enumerate_mas(i, j):
    """нумерация каждого элмента массива ( поля на коотором идёт игра ) 1-2-3-4-5-...-16"""
    return i * 4 + j + 1


def get_index_from_number(num):
    """получение индекса элемента по данному элементу (x, y)"""
    num -= 1
    x, y = num // 4, num % 4
    return x, y


def add_2_or_4(mas, x, y):
    """добавление случайного числа на поле (2 или 4)"""
    if random.random() <= 0.8:
        mas[x][y] = 2
    else:
        mas[x][y] = 4
    return mas


def is_empty(mas):
    """проверка пустоты массива"""
    empty_pos = []
    for i in range(4):
        for j in range(4):
            if mas[i][j] == 0:
                empty_pos.append(enumerate_mas(i, j))
    return empty_pos


def is_full(mas):
    """проверка полноты массива"""
    for row in mas:
        for elem in row:
            if elem == 0:
                return True
    return False


def move_left(mas):
    """движение всех элементов игры влево"""
    start = copy.deepcopy(mas)
    delta = 0
    for row in mas:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.append(0)
    for i in range(4):
        for j in range(3):
            if mas[i][j] == mas[i][j + 1] and mas[i][j] != 0:
                mas[i][j] *= 2
                delta += mas[i][j]
                mas[i].pop(j + 1)
                mas[i].append(0)
    return mas, delta, not start == mas


def move_right(mas):
    """движение всех элементов игры вправо"""
    start = copy.deepcopy(mas)
    delta = 0
    for row in mas:
        while 0 in row:
            row.remove(0)
        while len(row) != 4:
            row.insert(0, 0)
    for i in range(4):
        for j in range(3, 0, -1):
            if mas[i][j] == mas[i][j - 1] and mas[i][j] != 0:
                mas[i][j] *= 2
                delta += mas[i][j]
                mas[i].pop(j - 1)
                mas[i].insert(0, 0)
    return mas, delta, not start == mas


def move_up(mas):
    """двжиение всех элементов игры вверх"""
    start = copy.deepcopy(mas)
    delta = 0
    for j in range(4):
        col = []
        for i in range(4):
            if mas[i][j] != 0:
                col.append(mas[i][j])
        while len(col) != 4:
            col.append(0)
        for i in range(3):
            if col[i] == col[i + 1] and col[i] != 0:
                col[i] *= 2
                delta += mas[i][j]
                col.pop(i + 1)
                col.append(0)
        for i in range(4):
            mas[i][j] = col[i]
    return mas, delta, not start == mas


def move_down(mas):
    """движение всех элементов игры вниз"""
    start = copy.deepcopy(mas)
    delta = 0
    for j in range(4):
        col = []
        for i in range(4):
            if mas[i][j] != 0:
                col.append(mas[i][j])
        while len(col) != 4:
            col.insert(0, 0)
        for i in range(3, 0, -1):
            if col[i] == col[i - 1] and col[i] != 0:
                col[i] *= 2
                delta += mas[i][j]
                col.pop(i - 1)
                col.insert(0, 0)
        for i in range(4):
            mas[i][j] = col[i]
    return mas, delta, not start == mas


def is_move_available(mas):
    """проверка на возможность хода"""
    for i in range(3):
        for j in range(3):
            if mas[i][j] == mas[i][j + 1] or mas[i][j] == mas[i + 1][j]:
                return True
    for i in range(1, 4):
        for j in range(1, 4):
            if mas[i][j] == mas[i][j - 1] or mas[i][j] == mas[i - 1][j]:
                return True
    return False


def is_available_name(name):
    """проверка на валидность имени"""
    return len(name) >= 2
