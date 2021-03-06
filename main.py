import pygame
import sqlite3
from random import randrange

from capture import catch
from backpack import display
from help import info
from shop import buy

all_sprites = pygame.sprite.Group()
name = ""


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Field:
    def __init__(self, n, m):
        self.rows = n
        self.cols = m
        self.grid = [[0] * m for _ in range(n)]
        self.place()

    def place(self):
        cnt = 18
        trap = 5
        for i in range(self.rows):
            for j in range(self.cols):
                r = randrange(100)
                if 20 <= r < 30 and trap:
                    self.grid[i][j] = 2
                    trap -= 1  # ловушка
                elif 30 <= r < 40:
                    self.grid[i][j] = 3  # ладан
        while cnt:
            i = randrange(self.rows)
            j = randrange(self.cols)
            while self.grid[i][j] != 0 and (i, j) != (3, 7):
                i = randrange(self.rows)
                j = randrange(self.cols)
            self.grid[i][j] = 1
            cnt -= 1

    def render(self, screen):
        screen.fill((255, 204, 0), pygame.Rect(10, 20, 700, 560))
        # вертикальные линии
        for i in range(0, self.cols):
            pygame.draw.line(screen, (255, 0, 0), (70 * i + 10, 20),
                             (70 * i + 10, 580), width=5)
        # горизонтальные линии
        for i in range(0, self.rows):
            pygame.draw.line(screen, (255, 0, 0), (10, 70 * i + 20),
                             (710, 70 * i + 20), width=5)


field = Field(10, 11)


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = pygame.Color((255, 0, 0))
        self.text = text
        self.font = pygame.font.Font("data/corbell.ttf", 35)
        self.font.bold = True
        self.text_render = self.font.render(text, True, self.color)
        self.active = False
        self.done = False

    def handle_event(self, event):
        global name
        if event.type == pygame.MOUSEBUTTONDOWN and not self.done:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = pygame.Color((0, 255, 0)) if self.active else pygame.Color((255, 0, 0))
        if event.type == pygame.KEYDOWN and not self.done:
            if self.active:
                if event.key == pygame.K_RETURN:
                    name = self.text
                    self.done = True
                    self.color = pygame.Color((0, 0, 255))
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.text_render = self.font.render(self.text, True, self.color)

    def update(self):
        width = max(200, self.text_render.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        screen.blit(self.text_render, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


def background(region):
    size = 1000, 600
    pygame.init()
    screen = pygame.display.set_mode(size)
    bg = pygame.image.load("data/Pallet-Town.png")
    screen.blit(bg, (0, 0))

    field.render(screen)
    shop = pygame.image.load("data/pokecenter.png")
    if region == "Kanto":
        font = pygame.font.Font("data/corbell.ttf", 35)
        font.bold = True
        text = font.render("Паллет-таун", True, (0, 0, 0))
        screen.blit(text, (750, 40))
        screen.blit(shop, (500, 230))
    elif region == "Johto":
        font = pygame.font.Font("data/corbell.ttf", 25)
        font.bold = True
        text = font.render("Петалбург-Сити", True, (0, 0, 0))
        screen.blit(text, (750, 40))
        screen.blit(shop, (640, 510))
    elif region == "Hoenn":
        font = pygame.font.Font("data/corbell.ttf", 35)
        font.bold = True
        text = font.render("Литлрут-Таун", True, (0, 0, 0))
        screen.blit(text, (750, 40))
        screen.blit(shop, (150, 440))

    image = pygame.image.load("data/backpack.png")
    screen.blit(image, (870, 100))
    image = pygame.image.load("data/question-mark.png")
    screen.blit(image, (890, 480))
    font = pygame.font.Font("data/corbell.ttf", 50)
    font.bold = True
    con = sqlite3.connect("Pokemon.db")
    cur = con.cursor()
    caught = len(list(cur.execute("SELECT * FROM Collection").fetchall()))
    quantity = len(list(cur.execute("SELECT * FROM Kanto").fetchall())) + len(list(cur.execute(
        "SELECT * FROM Johto").fetchall())) + len(list(cur.execute("SELECT * FROM Hoenn").fetchall()))
    font = pygame.font.Font("data/corbell.ttf", 35)
    font.bold = True
    text = font.render("Поймано", True, (0, 0, 0))
    screen.blit(text, (730, 100))
    text = font.render(f"       {caught}", True, (0, 0, 0))
    screen.blit(text, (730, 135))
    text = font.render("      из", True, (0, 0, 0))
    screen.blit(text, (730, 170))
    text = font.render(f"      {quantity + 1}", True, (0, 0, 0))
    screen.blit(text, (730, 205))
    text = font.render("покемонов", True, (0, 0, 0))
    screen.blit(text, (730, 240))
    if caught == 18:
        finish()


def finish():
    global name
    pygame.display.set_caption("Вы нашли всех покемонов")
    pygame.init()
    screen0 = pygame.display.set_mode((600, 313))
    image = pygame.image.load("data/celebration.png")
    screen0.blit(image, (0, 0))
    font = pygame.font.Font("data/corbell.ttf", 20)
    font.bold = True
    text = font.render(
        "Вы поймали всех покемонов в этом регионе!", True, (227, 8, 0))
    screen0.blit(text, (10, 10))
    clock = pygame.time.Clock()
    miku = AnimatedSprite(pygame.image.load(
        "data/miku_spritesheet.png"), 5, 1, 420, 200)
    all_sprites.add(miku)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update()
        screen0.blit(image, (0, 0))
        font = pygame.font.Font("data/corbell.ttf", 20)
        font.bold = True
        text = font.render(f"{name}, ты поймал всех покемонов в этом регионе!", True, (227, 8, 0))
        screen0.blit(text, (10, 10))
        all_sprites.draw(screen0)
        pygame.display.flip()
        clock.tick(5)
    pygame.quit()
    hello()


def redraw(screen):
    bg = pygame.image.load("data/Pallet-Town.png")
    screen.blit(bg, (0, 0))
    intro_text = ["      ВЫБЕРИТЕ РЕГИОН", "",
                  "      Канто", "      Джото", "      Хоенн"]
    image = pygame.image.load("data/pokeball.png")
    screen.blit(image, (10, 220))
    screen.blit(image, (10, 295))
    screen.blit(image, (10, 370))
    font = pygame.font.Font("data/corbell.ttf", 60)
    font.bold = True
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, True, (0, 0, 255))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height + 5
        screen.blit(string_rendered, intro_rect)
    font = pygame.font.Font("data/corbell.ttf", 30)
    font.bold = True
    text = font.render("Введите свое имя:", True, (0, 0, 255))
    screen.blit(text, (600, 260))


def hello():
    global name
    pygame.mixer.init()
    pygame.mixer.music.load('data/choose_region.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    pygame.init()
    pygame.display.set_caption('Pokemon Yellow and Red')
    size = 900, 600
    screen = pygame.display.set_mode(size)
    redraw(screen)
    input_box = InputBox(600, 300, 50, 40)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN and 10 <= list(event.pos)[0] <= 90 and input_box.done:
                info(name)
                if 200 <= list(event.pos)[1] <= 280:
                    basic("Kanto")
                elif 290 <= list(event.pos)[1] <= 370:
                    basic("Johto")
                elif 380 <= list(event.pos)[1] <= 460:
                    basic("Hoenn")
            input_box.handle_event(event)
        input_box.update()
        redraw(screen)
        input_box.draw(screen)
        pygame.display.flip()


def basic(region, x=10, y=20, i=0, j=0):
    global name
    size = 900, 600
    screen = pygame.display.set_mode(size)
    background(region)
    pygame.init()
    pygame.mixer.music.load('data/go.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(1.2)
    # перемещение героя
    image = pygame.image.load("data/trainer.png")
    screen.blit(image, (x, y))
    pos_x = x
    pos_y = y
    pokeball = 10
    incense = 0
    running = True
    while running:
        for event in pygame.event.get():
            screen.fill((204, 204, 204), pygame.Rect(730, 290, 240, 180))
            for k in range(0, 3):
                pygame.draw.line(screen, (0, 0, 0), (120 * k + 730, 290),
                                 (120 * k + 730, 470), width=3)
            for k in range(0, 5):
                pygame.draw.line(screen, (0, 0, 0), (730, 45 * k + 290),
                                 (970, 45 * k + 290), width=3)
            font = pygame.font.Font("data/corbell.ttf", 35)
            font.bold = True
            r = pygame.image.load("data/red.png")
            r = pygame.transform.scale(r, (40, 40))
            screen.blit(r, (770, 292))
            text = font.render(str(pokeball), True, (0, 0, 0))
            screen.blit(text, (895, 295))
            r = pygame.image.load("data/blue.png")
            r = pygame.transform.scale(r, (40, 40))
            screen.blit(r, (770, 337))
            text = font.render("0", True, (0, 0, 0))
            screen.blit(text, (895, 340))
            r = pygame.image.load("data/yellow.png")
            r = pygame.transform.scale(r, (40, 40))
            screen.blit(r, (770, 382))
            text = font.render("0", True, (0, 0, 0))
            screen.blit(text, (895, 385))
            r = pygame.image.load("data/incense.png")
            r = pygame.transform.scale(r, (40, 40))
            screen.blit(r, (770, 427))
            text = font.render(str(incense), True, (0, 0, 0))
            screen.blit(text, (895, 430))
            if event.type == pygame.QUIT:
                running = False
                exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and pos_x > 10:
                    pos_x -= 70
                    j -= 1
                    background(region)
                    screen.blit(image, (pos_x, pos_y))
                if event.key == pygame.K_RIGHT and pos_x < 640:
                    pos_x += 70
                    j += 1
                    background(region)
                    screen.blit(image, (pos_x, pos_y))
                if event.key == pygame.K_UP and pos_y > 20:
                    pos_y -= 70
                    i -= 1
                    background(region)
                    screen.blit(image, (pos_x, pos_y))
                if event.key == pygame.K_DOWN and pos_y < 510:
                    pos_y += 70
                    i += 1
                    background(region)
                    screen.blit(image, (pos_x, pos_y))
                if (region == "Kanto" and pos_x == 500 and pos_y == 230) or \
                        (region == "Johto" and pos_x == 640 and pos_y == 510) or \
                        (region == "Hoenn" and pos_x == 150 and pos_y == 440):
                    buy(pokeball)
                    basic(region, pos_x, pos_y, i, j)
                font = pygame.font.Font("data/corbell.ttf", 15)
                font.bold = True
                if field.grid[i][j] == 1:  # есть покемон или нет
                    pokeball = catch(region, pokeball)
                    field.grid[i][j] = 0
                    basic(region, pos_x, pos_y, i, j)
                elif field.grid[i][j] == 2:  # ловушка
                    pygame.draw.rect(screen, (255, 204, 0),
                                     (715, 495, 190, 95))
                    text = font.render(
                        "Ловушка команды R!", True, (255, 0, 0))
                    screen.blit(text, (720, 500))
                    text = font.render(
                        "Вы потеряли покеболлы", True, (0, 0, 0))
                    screen.blit(text, (720, 520))
                    text = font.render(" и ладаны.", True, (0, 0, 0))
                    screen.blit(text, (720, 540))
                    incense = 0
                    pokeball = 0
                elif field.grid[i][j] == 3:  # ладан
                    text = font.render(
                        "Ура, вы нашли сюрприз!", True, (0, 0, 0))
                    screen.blit(text, (720, 500))
                    text = font.render("Здесь 1 ладан.", True, (0, 0, 0))
                    screen.blit(text, (720, 520))
                    text = font.render("Теперь он ваш.", True, (0, 0, 0))
                    screen.blit(text, (720, 540))
                    incense += 1

            if event.type == pygame.MOUSEBUTTONDOWN and 750 <= list(event.pos)[0] <= 1000 and \
                    40 <= list(event.pos)[1] <= 100:
                hello()
            elif event.type == pygame.MOUSEBUTTONDOWN and 730 <= list(event.pos)[0] <= 1000 and \
                    100 <= list(event.pos)[1] <= 260:
                display()
                basic(region, pos_x, pos_y, i, j)
            elif event.type == pygame.MOUSEBUTTONDOWN and 730 <= list(event.pos)[0] <= 1000 and \
                    480 <= list(event.pos)[1] <= 580:
                info(name)
                basic(region, pos_x, pos_y, i, j)
            elif event.type == pygame.MOUSEBUTTONDOWN and 730 <= list(event.pos)[0] <= 1000 and \
                    425 <= list(event.pos)[1] <= 470 and incense > 0:
                font = pygame.font.Font("data/corbell.ttf", 15)
                font.bold = True
                incense = incense - 1
                text = font.render(
                    "Использован ладан.", True, (0, 0, 0))
                screen.blit(text, (720, 500))
                text = font.render("Покемоны будут", True, (0, 0, 0))
                screen.blit(text, (720, 520))
                text = font.render("встречаться чаще.", True, (0, 0, 0))
                screen.blit(text, (720, 540))
        pygame.display.flip()


if __name__ == '__main__':
    c = sqlite3.connect("Pokemon.db")
    cur = c.cursor()
    cur.execute("DELETE FROM Collection WHERE name != 'Бульбазавр' ")
    c.commit()
    c.close()
    hello()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
