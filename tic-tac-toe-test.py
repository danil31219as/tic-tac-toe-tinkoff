import sys
from copy import deepcopy

PLAYER_CHAR = 'x'
COMPUTER_CHAR = 'o'
EMPTY_CHAR = '.'
PLAYER_TURN = False
COMPUTER_TURN = True
SCORE = {PLAYER_CHAR: - 100, COMPUTER_CHAR: 100, 'full': 0}
CHARS = {COMPUTER_CHAR: PLAYER_CHAR, PLAYER_CHAR: COMPUTER_CHAR}


def horizontal_check(field, n, k, simbol):  # проверка победы по горизонталям
    max_count = 0
    for i in range(n):
        count = 0
        for j in range(n):
            if field[i][j] == simbol:
                count += 1
            else:
                if count > max_count:
                    max_count = count
                count = 0
        if count > max_count:
            max_count = count
    return max_count


def vertical_check(field, n, k, simbol):  # проверка победы по вертикалям
    max_count = 0
    for i in range(n):
        count = 0
        for j in range(n):
            if field[j][i] == simbol:
                count += 1
            else:
                if count > max_count:
                    max_count = count
                count = 0
        if count > max_count:
            max_count = count

    return max_count


def main_diagonal_check(field, n, k,
                        simbol):  # проверка победы по главным диагоналям
    max_count = 0
    for i in range(-n + 1, n):
        if i < 0:
            count = 0
            for j in range(n + i):
                if field[abs(i) + j][0 + j] == simbol:
                    count += 1
                else:
                    if count > max_count:
                        max_count = count
                    count = 0
            if count > max_count:
                max_count = count
        else:
            count = 0
            for j in range(n - i):
                if field[0 + j][i + j] == simbol:
                    count += 1
                else:
                    if count > max_count:
                        max_count = count
                    count = 0
            if count > max_count:
                max_count = count

    return max_count


def other_diagonal_check(field, n, k,
                         simbol):  # проверка победы по побочным диагоналям
    max_count = 0
    for i in range(-n + 1, n):
        if i < 0:
            count = 0
            for j in range(n + i):
                if field[abs(i) + j][n - 1 - j] == simbol:
                    count += 1
                else:
                    if count > max_count:
                        max_count = count
                    count = 0
            if count > max_count:
                max_count = count

        else:
            count = 0
            for j in range(i + 1):
                if field[0 + j][i - j] == simbol:
                    count += 1
                else:
                    if count > max_count:
                        max_count = count
                    count = 0
            if count > max_count:
                max_count = count
    return max_count


def check_win(field, n, k,
              simbol):  # сравнение максимума максимумов подряд идущих символов с необходимым для победы
    if max([horizontal_check(field, n, k, simbol), vertical_check(field, n, k,
                                                                  simbol),
            main_diagonal_check(
                field, n, k, simbol),
            other_diagonal_check(field, n, k, simbol)]) >= k:
        return f'{simbol} выиграли!!!'


def check_full(field, n):  # проверка заполненности
    return not any([EMPTY_CHAR in field[i] for i in range(n)])


def check_end(field, n, k, simbol):  # проверка на законченность игры
    result = check_win(field, n, k, simbol)
    if result:
        return result
    if check_full(field, n):
        return 'Ничья!'


class Board:
    def __init__(self, n):
        self.n = n
        self.board = [[EMPTY_CHAR for __ in range(n)] for _ in range(n)]

    def __repr__(self):
        print_board = ''
        print_board += ' '.join(
            [str(i).ljust(len(str(self.n))) for i in range(self.n + 1)]) + '\n'
        for i in range(self.n):
            print_board += str(i + 1).rjust(len(str(self.n))) + ' ' + ' '.join(
                [elem.ljust(len(str(self.n))) for elem in self.board[i]]) + '\n'
        return print_board


class Player:
    def __init__(self, simbol):
        self.simbol = simbol

    def make_step(self, field, n, k):  # ход игрока
        x, y = map(int,
                   input('Введите координаты точки через пробел: ').split())
        while field[x - 1][y - 1] != EMPTY_CHAR:
            x, y = map(int,
                       input('Введите координаты точки через пробел: ').split())
        field[x - 1][y - 1] = self.simbol


class Computer:
    def __init__(self, simbol):
        self.simbol = simbol

    def make_step(self, field, n, k):  # ход компьютера
        board = deepcopy(field)

        if field[n // 2][
            n // 2] == EMPTY_CHAR:  # устанавливаем координаты по умолчанию
            max_count = 1
            max_coordinates = (n // 2, n // 2)
        else:
            max_count = 0
            max_coordinates = ()
        for i in range(n):
            for j in range(n):
                if board[i][j] == EMPTY_CHAR:

                    board[i][j] = CHARS[self.simbol]  # проверяем, выграет ли соперник

                    if check_win(board, n, k, board[i][j]):
                        count = sys.maxsize - 1
                        if count > max_count:
                            max_count = count
                            max_coordinates = (i, j)
                        continue
                    # сравниваем максимумы подряд идущих для каждой клетки
                    board[i][j] = self.simbol
                    count = max([horizontal_check(board, n, k, self.simbol),
                                 vertical_check(board, n, k, self.simbol),
                                 main_diagonal_check(board, n, k,
                                                     self.simbol),
                                 other_diagonal_check(board, n, k,
                                                      self.simbol)])
                    if count >= k:
                        max_count = sys.maxsize
                        max_coordinates = (i, j)
                    if count > max_count:
                        max_count = count
                        max_coordinates = (i, j)
                    board[i][j] = EMPTY_CHAR

        x, y = max_coordinates
        print(f'Компьютер походил в точку: {x + 1} {y + 1}')
        field[x][y] = self.simbol


def game(queue, n, k):  # игровой цикл
    board = Board(n)
    i = 0
    print(board)
    while True:
        queue[i % 2].make_step(board.board, n, k)
        print(board)
        result = check_end(board.board, n, k, queue[i % 2].simbol)
        if result:
            print(result)
            return
        i += 1


def start():  # настройки игры
    d_queue = {'1': [Player(PLAYER_CHAR), Player(COMPUTER_CHAR)],
               '2': [Computer(PLAYER_CHAR), Player(COMPUTER_CHAR)],
               '3': [Computer(PLAYER_CHAR), Computer(COMPUTER_CHAR)]}
    n = int(input('Введите размер стороны поля: '))
    k = int(input('Введите количество знаков для победы: '))
    if k > n:
        print('!Слишком много знаков!')
        return
    print('1. 2 игрока', '2. Против компьютера', '3. Только компьютер',
          sep='\t')
    variant = input("Выберите вариант игры: ")
    game(d_queue[variant], n, k)


if __name__ == '__main__':
    start()
    print('Конец игры.')
