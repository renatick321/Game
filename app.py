import pygame
import random
import sys
import os


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def complexity_canvas(screen, x=40, y=40):
    pygame.draw.rect(screen, 
        (0, 155, 0), 
        (45, 45, 500, 10))
    
    pygame.draw.rect(screen, 
        (0, 55, 0), 
        (x, y, 20, 20))

    pygame.draw.rect(screen, 
        (19, 19, 19), 
        (x, y, 20, 20), 9)

    # Надпись
    font = pygame.font.Font(None, 50)
    text1 = "Сложность: {}".format(x - 25)
    sg = font.render(text1, True, (100, 255, 100))
    sg_x = 45
    sg_y = 90
    sg_w = sg.get_width()
    sg_h = sg.get_height()
    screen.blit(sg, (sg_x, sg_y))

    pygame.draw.rect(screen, (0, 255, 0), 
        (sg_x - 10, sg_y - 10, 
            sg_w + 20, sg_h + 20), 1)
    pygame.display.flip()
    return x - 25 # Возвращаем сложность


class Board:
    # создание поля
    def __init__(self, height, width, complexity):
        self.width = width
        self.height = height
        # Всё поле чёрное
        self.board = [[0] * width for _ in range(height)]
        # Отступы
        self.left = 20
        self.top = 20
        # Размер клетки
        self.cell_size = 30
        # Сложность
        self.complexity = complexity
        self.clicks = 0


    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size


    def render(self, screen):
        for row in range(self.height):
            for cell in range(self.width):
                y = self.top + row * self.cell_size
                x = self.left + cell * self.cell_size
                # Создаём клетку
                pygame.draw.rect(screen, (0, 0, 0), 
                    ((x, y), 
                        (self.cell_size, self.cell_size)))
                # Создаём рамочку для клетки
                pygame.draw.rect(screen, (255, 255, 255), 
                    ((x, y), 
                        (self.cell_size, self.cell_size)), 1)


    def create(self):
        # Создание поля
        for i in range(self.complexity):
            y = self.top + self.cell_size * random.randint(0, self.height - 1)
            x = self.left + self.cell_size * random.randint(0, self.width - 1)
            self.clicks = -1
            board.on_click((x, y))
        self.clicks = 0


    def on_click(self, coords):
        # Нажатие на поле при помощи следующей механики:
        # O O O     O X O
        # O O O --> X X X
        # O O O     O X O
        x, y = coords
        x1, y1 = x - self.left, y - self.top
        x_index = (x1 // self.cell_size)
        y_index = (y1 // self.cell_size)
        if self.height > y_index >= 0 and self.width > x_index >= 0:
            self.cell_staining((x, y))
            self.cell_staining((x + self.cell_size, y))
            self.cell_staining((x, y + self.cell_size))
            self.cell_staining((x - self.cell_size, y))
            self.cell_staining((x, y - self.cell_size))

            self.clicks += 1
            pygame.draw.rect(screen, (0, 0, 0), (15, 325, 625, 380))
            font = pygame.font.Font(None, 50)
            text1 = "Количество нажатий: {}/{}".format(self.clicks, int(self.complexity * 3 / 2))
            sg = font.render(text1, True, (100, 255, 100))
            sg_x = 20
            sg_y = 340
            sg_w = sg.get_width()
            sg_h = sg.get_height()
            screen.blit(sg, (sg_x, sg_y))


    def cell_staining(self, cell_coords):
        # Инверсия клетки
        x, y = cell_coords[0] - self.left, cell_coords[1] - self.top
        x_index = (x // self.cell_size)
        y_index = (y // self.cell_size)
        if self.height > y_index >= 0 and self.width > x_index >= 0:
            color = self.get_color(x_index, y_index)
            rev_color = self.reverse_color(color)
            self.edit_color(x_index, y_index, rev_color)
            x = self.top + (x // self.cell_size) * self.cell_size
            y = self.left + (y // self.cell_size) * self.cell_size

            pygame.draw.rect(screen, (rev_color, rev_color, rev_color), 
                ((x, y), 
                    (self.cell_size, self.cell_size)))

            pygame.draw.rect(screen, (color, color, color), 
                ((x, y), 
                    (self.cell_size, self.cell_size)), 1)


    def get_color(self, x_index, y_index):
        return self.board[y_index][x_index]


    def reverse_color(self, color):
        return (color + 1) % 2 * 255


    def edit_color(self, x_index, y_index, color):
        self.board[y_index][x_index] = color


    def check(self):
        for row in self.board:
            for i in row:
                if i % 2 == 1:
                    return False
        return True


# Константы для настройки класса Board
BOARD_HEIGHT = 10
BOARD_WIDTH = 20
LEFT = 10
TOP = 10
CELL_SIZE = 30


running = True
start = True
clicks = 0


pygame.init()
pygame.display.set_caption('Обратный кубик Рубика')
size = width, height = 640, 380
screen = pygame.display.set_mode(size)


# Надписи:
# Начать игру
font = pygame.font.Font(None, 50)
text1 = "Начать игру"
sg = font.render(text1, True, (100, 255, 100))
sg_x = width // 2 - sg.get_width() // 2
sg_y = 90
sg_w = sg.get_width()
sg_h = sg.get_height()
screen.blit(sg, (sg_x, sg_y))
pygame.draw.rect(screen, (0, 255, 0), 
    (sg_x - 10, sg_y - 10, 
        sg_w + 20, sg_h + 20), 1)

# Создать игру
font = pygame.font.Font(None, 50)
text2 = "Создать игру"
cgl = font.render(text2, True, (100, 255, 100))
cgl_x = width // 2 - cgl.get_width() // 2
cgl_y = 180
cgl_w = cgl.get_width()
cgl_h = cgl.get_height()
screen.blit(cgl, (cgl_x, cgl_y))
pygame.draw.rect(screen, (0, 255, 0), 
    (cgl_x - 10, cgl_y - 10, 
        cgl_w + 20, cgl_h + 20), 1)

pygame.display.flip()

# Настройка сложности
buttonon = False
buttonmotion = False

# Цикл меню
while start:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Завершаем бесконечный цикл
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            if buttonon:
                start = False
                break
            else:
                x, y = event.pos
                if sg_x + 20 + sg_w > x > sg_x - 10 and sg_y + 46 > y > sg_y - sg_h + 26:
                    start = False
                    complexity = 100
                elif cgl_x + 20 + cgl_w > x > cgl_x - 10 and cgl_y + 46 > y > cgl_y - cgl_h + 26:
                    screen.fill((0, 0, 0))
                    complexity = complexity_canvas(screen)
        elif event.type == pygame.MOUSEMOTION:
            if buttonon:
                if 525 >= event.pos[0] >= 40:
                    screen.fill((0, 0, 0))
                    complexity = complexity_canvas(screen, event.pos[0])
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if 60 > x > 40 and 60 > y > 40:
                buttonon = True


board = Board(BOARD_HEIGHT, BOARD_WIDTH, complexity)
running = True
screen.fill((0, 0, 0))
board.render(screen)
board.create()

# Основной игровой цикл
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            board.on_click(event.pos)
            if board.check():
                running = False
    pygame.display.flip()


screen.fill((0, 0, 0))


# Накидываем изображение
back = load_image('bg.png')
back_ = back.get_rect(
    bottomright=(width, height)
    )
screen.blit(back, back_)
pygame.display.update()


# Задаём статус
if board.complexity >= board.clicks:
    text2 = "Absolute winner"
elif int(board.complexity * 3 / 2) >= board.clicks:
    text2 = "Winner"
else:
    text2 = "Loser"

# Устанавливаем надпись со статусом игрока
font = pygame.font.Font(None, 50)
cgl = font.render(text2, True, (100, 255, 100))
cgl_x = width // 2 - cgl.get_width() // 2
cgl_y = height // 2 - cgl.get_height() // 2
cgl_w = cgl.get_width()
cgl_h = cgl.get_height()
screen.blit(cgl, (cgl_x, cgl_y))
pygame.draw.rect(screen, (0, 255, 0), 
    (cgl_x - 10, cgl_y - 10, cgl_w + 20, cgl_h + 20), 1
    )
pygame.display.flip()


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # Завершаем бесконечный цикл
            sys.exit()