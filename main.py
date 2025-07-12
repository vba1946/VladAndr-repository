# Полный код игры Тетрис
import pygame
import random

pygame.init()

# Настройки окна
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLUMNS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE

# Цвета
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
WHITE = (255, 255, 255)

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Формы фигур (тетромино)
SHAPES = [
    [[1]],[[1]],[[1]],[[1]],             # I
    [[1, 0, 0], [1, 1, 1]],     # J
    [[0, 0, 1], [1, 1, 1]],     # L
    [[1, 1], [1, 1]],           # O
    [[0, 1, 1], [1, 1, 0]],     # S
    [[0, 1, 0], [1, 1, 1]],     # T
    [[1, 1, 0], [0, 1, 1]]      # Z
]

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
    grid = [[BLACK for _ in range(COLUMNS)] for _ in range(ROWS)]
    for (x, y), color in locked_positions.items():
        if y >= 0:
            grid[y][x] = color
    return grid

def valid_space(shape, offset, grid):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                new_x = off_x + x
                new_y = off_y + y
                if new_x < 0 or new_x >= COLUMNS or new_y >= ROWS:
                    return False
                if grid[new_y][new_x] != BLACK:
                    return False
    return True

def rotate(shape):
    return [list(row)[::-1] for row in zip(*shape)]

class Piece:
    def __init__(self, x, y, shape, color):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = color
        self.rotation = 0

    def image(self):
        rotated = self.shape
        for _ in range(self.rotation % 4):
            rotated = rotate(rotated)
        return rotated

def draw_text_middle(surface, text, size, color, x, y):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, True, color)
    surface.blit(label, (x, y))

def draw_grid(surface, grid):
    for y in range(ROWS):
        for x in range(COLUMNS):
            pygame.draw.rect(surface, grid[y][x],
                             (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

    for x in range(COLUMNS):
        pygame.draw.line(surface, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, HEIGHT))
    for y in range(ROWS):
        pygame.draw.line(surface, GRAY, (0, y * BLOCK_SIZE), (WIDTH, y * BLOCK_SIZE))

def clear_rows(grid, locked):
    cleared = 0
    for y in range(ROWS - 1, -1, -1):
        if BLACK not in grid[y]:
            cleared += 1
            for x in range(COLUMNS):
                if (x, y) in locked:
                    del locked[(x, y)]

    if cleared > 0:
        for key in sorted(list(locked), key=lambda pos: pos[1])[::-1]:
            x, y = key
            if y < ROWS:
                new_key = (x, y + cleared)
                locked[new_key] = locked.pop(key)
    return cleared

def main():
    clock = pygame.time.Clock()
    fall_time = 0
    fall_speed = 0.5
    grid = create_grid()
    locked_positions = {}
    current_piece = Piece(3, 0, random.choice(SHAPES), random.choice(COLORS))
    running = True
    score = 0
    paused = False
    accelerating = False  # Для ускоренного падения

    while running:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        clock.tick()

        if not paused:
            speed = fall_speed / 5 if accelerating else fall_speed
            if fall_time / 1000 > speed:
                fall_time = 0
                current_piece.y += 1
                if not valid_space(current_piece.image(), (current_piece.x, current_piece.y), grid):
                    current_piece.y -= 1
                    for y, row in enumerate(current_piece.image()):
                        for x, cell in enumerate(row):
                            if cell:
                                locked_positions[(current_piece.x + x, current_piece.y + y)] = current_piece.color
                    cleared = clear_rows(grid, locked_positions)
                    score += cleared * 100
                    current_piece = Piece(3, 0, random.choice(SHAPES), random.choice(COLORS))
                    if not valid_space(current_piece.image(), (current_piece.x, current_piece.y), grid):
                        print("Игра окончена!")
                        draw_text_middle(screen, "Игра окончена!", 40, WHITE, WIDTH // 2 - 100, HEIGHT // 2)
                        pygame.display.update()
                        pygame.time.delay(2000)
                        running = False

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Выход из игры при закрытии окна

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                elif event.key == pygame.K_DOWN:
                    accelerating = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    accelerating = False

            if not paused and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece.image(), (current_piece.x, current_piece.y), grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece.image(), (current_piece.x, current_piece.y), grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotation += 1
                    if not valid_space(current_piece.image(), (current_piece.x, current_piece.y), grid):
                        current_piece.rotation -= 1

        # Рисуем текущую фигуру
        for y, row in enumerate(current_piece.image()):
            for x, cell in enumerate(row):
                if cell and current_piece.y + y >= 0:
                    grid[current_piece.y + y][x + current_piece.x] = current_piece.color

        # Отрисовка
        draw_grid(screen, grid)
        draw_text_middle(screen, f"Счёт: {score}", 24, WHITE, WIDTH // 2 - 70, 10)

        if paused:
            draw_text_middle(screen, "ПАУЗА", 40, WHITE, WIDTH // 2 - 60, HEIGHT // 2)
            pygame.display.update()
            continue

        pygame.display.update()

def main_menu():
    run = True
    while run:
        screen.fill(BLACK)
        draw_text_middle(screen, "Нажмите любую клавишу, чтобы начать", 24, WHITE, WIDTH // 2 - 180, HEIGHT // 2)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                main()
                run = False  # Останавливаем меню после запуска игры

    pygame.quit()

if __name__ == "__main__":
    main_menu()

# C:\Users\VA_Biryukov\AppData\Local\Programs\Python\Python310\python.exe D:\Documents\GitHub\VladAndr-repository\test3.py
# pygame 2.6.1 (SDL 2.28.4, Python 3.10.1)
# Hello from the pygame community. https://www.pygame.org/contribute.html
# Игра окончена!
# Process finished with exit code 0

