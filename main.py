# Код программы Тетрис

# Импортируем библиотеку pygame — основной модуль для создания игр на Python
import pygame
# Импортируем random — чтобы случайным образом выбирать фигуры и цвета
import random

# Инициализируем pygame (всё, что связано с графикой и звуком)
pygame.init()

# Настройки окна
WIDTH, HEIGHT = 300, 600         # Ширина и высота игрового окна в пикселях
BLOCK_SIZE = 30                   # Размер одного блока (ширина и высота квадрата)
COLUMNS = WIDTH // BLOCK_SIZE     # Количество столбцов в сетке (10)
ROWS = HEIGHT // BLOCK_SIZE       # Количество строк в сетке (20)

# Цвета, заданные в формате RGB (красный, зелёный, синий)
BLACK = (0, 0, 0)                 # Чёрный — фон и пустые ячейки
GRAY = (100, 100, 100)            # Серый — границы клеток
WHITE = (255, 255, 255)           # Белый — может использоваться как временный цвет

# Создание экрана — вот где появляется переменная screen!
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создаём окно с заданными размерами
pygame.display.set_caption("Tetris")               # Устанавливаем заголовок окна

# Формы фигур (тетромино)
SHAPES = [
    [[1]],[[1]],[[1]],[[1]],                  # ❌ Ошибка: это не корректная форма I
    [[1, 0, 0], [1, 1, 1]],          # J
    [[0, 0, 1], [1, 1, 1]],          # L
    [[1, 1], [1, 1]],                # O
    [[0, 1, 1], [1, 1, 0]],          # S
    [[0, 1, 0], [1, 1, 1]],          # T
    [[1, 1, 0], [0, 1, 1]]           # Z
]

# Цвета для каждой формы
COLORS = [
    (0, 255, 255),  # Голубой — I
    (0, 0, 255),    # Синий — J
    (255, 165, 0),  # Оранжевый — L
    (255, 255, 0),  # Жёлтый — O
    (0, 255, 0),    # Зелёный — S
    (128, 0, 128),  # Фиолетовый — T
    (255, 0, 0)     # Красный — Z
]


def create_grid(locked_positions={}):
    # Создаём сетку из чёрных квадратов
    grid = [[BLACK for x in range(COLUMNS)] for y in range(ROWS)]
    # Если есть зафиксированные блоки (уже упавшие), рисуем их
    for (x, y), color in locked_positions.items():
        if y >= 0:
            grid[y][x] = color
    return grid


def valid_space(shape, offset, grid):
    # Проверяем, можно ли переместить/повернуть фигуру
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = off_x + x
                new_y = off_y + y
                # Проверка выхода за границы
                if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS:
                    return False
                # Проверка, занята ли ячейка
                if grid[new_y][new_x] != BLACK:
                    return False
    return True


def rotate(shape):
    # Поворачивает фигуру на 90 градусов
    return [list(row)[::-1] for row in zip(*shape)]


class Piece:
    def __init__(self, x, y, shape, color):
        # Конструктор класса "Фигура"
        self.x = x              # Начальная координата X
        self.y = y              # Начальная координата Y
        self.shape = shape      # Форма фигуры
        self.color = color      # Цвет фигуры
        self.rotation = 0       # Текущее состояние поворота

    def image(self):
        # Возвращает текущую ориентацию фигуры (с учётом поворотов)
        rotated = self.shape
        for _ in range(self.rotation % 4):  # Поворачиваем до нужного состояния
            rotated = rotate(rotated)
        return rotated


def draw_grid(surface, grid):
    # Рисует всю сетку с заполненными блоками
    for y in range(ROWS):
        for x in range(COLUMNS):
            pygame.draw.rect(surface, grid[y][x],
                             (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    # Рисует сетку (вертикальные линии)
    for x in range(COLUMNS):
        pygame.draw.line(surface, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, HEIGHT))
    # Рисует сетку (горизонтальные линии)
    for y in range(ROWS):
        pygame.draw.line(surface, GRAY, (0, y * BLOCK_SIZE), (WIDTH, y * BLOCK_SIZE))


def clear_rows(grid, locked):
    # Очищает полностью заполненные ряды
    cleared = 0
    for y in range(ROWS - 1, -1, -1):  # Проходим снизу вверх
        if BLACK not in grid[y]:       # Если ряд полностью заполнен
            cleared += 1
            for x in range(COLUMNS):
                if (x, y) in locked:
                    del locked[(x, y)]  # Удаляем блоки из словаря

    if cleared > 0:
        # Перемещаем все блоки выше очищенных рядов вниз
        for key in sorted(list(locked), key=lambda pos: pos[1])[::-1]:
            x, y = key
            if y < ROWS:
                new_key = (x, y + cleared)
                locked[new_key] = locked.pop(key)
    return cleared


def main():
    # Основная функция игры
    clock = pygame.time.Clock()   # Объект часов для контроля FPS
    fall_time = 0                 # Время падения фигуры
    fall_speed = 0.5              # Скорость падения (в секундах)
    grid = create_grid()          # Создаём начальную сетку
    locked_positions = {}         # Храним уже упавшие блоки
    # Создаём первую фигуру со случайной формой и цветом
    current_piece = Piece(3, 0, random.choice(SHAPES), random.choice(COLORS))
    running = True                # Состояние игры (игра продолжается)

    while running:
        grid = create_grid(locked_positions)  # Обновляем сетку
        fall_time += clock.get_rawtime()        # Добавляем время, прошедшее с последнего тика
        clock.tick()                            # Обновляем часы

        # Проверяем, пора ли опустить фигуру
        if fall_time / 1000 > fall_speed:
            fall_time = 0
            current_piece.y += 1
            # Проверяем, не вышла ли фигура за пределы или не столкнулась с другими блоками
            if not valid_space(current_piece.image(), (current_piece.x, current_piece.y), grid):
                current_piece.y -= 1
                # Фиксируем фигуру на поле
                for y, row in enumerate(current_piece.image()):
                    for x, cell in enumerate(row):
                        if cell:
                            locked_positions[(current_piece.x + x, current_piece.y + y)] = current_piece.color
                clear_rows(grid, locked_positions)  # Очищаем заполненные строки
                # Создаём новую фигуру
                current_piece = Piece(3, 0, random.choice(SHAPES), random.choice(COLORS))

        # Обработка событий (нажатие клавиш, закрытие окна и т.д.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece.image(), (current_piece.x, current_piece.y), grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece.image(), (current_piece.x, current_piece.y), grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece.image(), (current_piece.x, current_piece.y), grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece.image(), (current_piece.x, current_piece.y), grid):
                        current_piece.rotation -= 1

        # Рисуем текущую фигуру на сетке
        for y, row in enumerate(current_piece.image()):
            for x, cell in enumerate(row):
                if cell and current_piece.y + y >= 0:
                    grid[current_piece.y + y][current_piece.x + x] = current_piece.color

        # Отрисовываем обновлённую сетку
        draw_grid(screen, grid)
        # Обновляем экран
        pygame.display.update()

    # Выходим из pygame
    pygame.quit()


# Точка входа в программу
if __name__ == "__main__":
    main()
