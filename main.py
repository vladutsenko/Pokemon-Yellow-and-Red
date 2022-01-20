import pygame
import os
import sqlite3
from random import randrange

from capture import catch
from backpack import display
from help import info

class Field:
    def __init__(self, n, m):
        self.rows = n
        self.cols = m
        self.grid = [[0] * m for _ in range(n)]
        self.place()

    def place(self):
        for i in range(self.rows):
            for j in range(self.cols):
                r = randrange(100)
                if r < 20:
                    self.grid[i][j] = 1
                elif 20 <= r < 30:
                    self.grid[i][j] = 2  # ловушка
                elif 30 <= r < 40:
                    self.grid[i][j] = 3  # ладан

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


def background(region):
    size = 1000, 600
    pygame.init()
    screen = pygame.display.set_mode(size)
    bg = pygame.image.load("data/Pallet-Town.png")
    screen.blit(bg, (0, 0))

    field.render(screen)
    if region == "kanto":
        font = pygame.font.Font("data/corbell.ttf", 50)
        font.bold = True
        text = font.render("Паллет-таун", True, (0, 0, 0))
        screen.blit(text, (750, 40))
    elif region == "johto":
        font = pygame.font.Font("data/corbell.ttf", 40)
        font.bold = True
        text = font.render("Петалбург-Сити", True, (0, 0, 0))
        screen.blit(text, (750, 40))
    elif region == "hoenn":
        font = pygame.font.Font("data/corbell.ttf", 50)
        font.bold = True
        text = font.render("Литлрут-Таун", True, (0, 0, 0))
        screen.blit(text, (750, 40))

    image = pygame.image.load("data/backpack.png")
    screen.blit(image, (870, 100))
    image = pygame.image.load("data/question-mark.png")
    screen.blit(image, (870, 480))
    font = pygame.font.Font("data/corbell.ttf", 50)
    font.bold = True
    con = sqlite3.connect("Pokemon.db")
    cur = con.cursor()
    cath = len(list(cur.execute("SELECT * FROM Collection").fetchall()))
    al = len(list(cur.execute("SELECT * FROM Kanto").fetchall())) + len(list(cur.execute(
        "SELECT * FROM Johto").fetchall())) + len(list(cur.execute("SELECT * FROM Hoenn").fetchall()))
    font = pygame.font.Font("data/corbell.ttf", 35)
    font.bold = True
    text = font.render("Поймано", True, (0, 0, 0))
    screen.blit(text, (730, 100))
    text = font.render(f"       {cath}", True, (0, 0, 0))
    screen.blit(text, (730, 135))
    text = font.render("      из", True, (0, 0, 0))
    screen.blit(text, (730, 170))
    text = font.render(f"       {al}", True, (0, 0, 0))
    screen.blit(text, (730, 205))
    text = font.render("покемонов", True, (0, 0, 0))
    screen.blit(text, (730, 240))


def hello():
    pygame.init()
    pygame.display.set_caption('Pokemon Yellow')
    size = 900, 600
    screen = pygame.display.set_mode(size)
    bg = pygame.image.load("data/Pallet-Town.png")
    screen.blit(bg, (0, 0))
    intro_text = ["      ВЫБЕРИТЕ РЕГИОН", "",
                  "      Канто", "      Джото", "      Хоенн"]
    fullname = os.path.join('data', "pokeball.png")
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
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                exit(0)
            if event.type == pygame.MOUSEBUTTONDOWN and 10 <= list(event.pos)[0] <= 90:
                if 200 <= list(event.pos)[1] <= 280:
                    basic("Kanto")
                elif 290 <= list(event.pos)[1] <= 370:
                    basic("Johto")
                elif 380 <= list(event.pos)[1] <= 460:
                    basic("Hoenn")
            pygame.display.flip()


def basic(region, x=10, y=20):
    size = 900, 600
    screen = pygame.display.set_mode(size)
    background(region)
    pygame.init()
    # перемещение героя
    fullname = os.path.join('data', "trainer.png")
    image = pygame.image.load(fullname)
    screen.blit(image, (x, y))
    pos_x = x
    pos_y = y
    i, j = 0, 0
    running = True
    while running:
        for event in pygame.event.get():
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
                if field.grid[i][j] == 1:  # есть покемон или нет
                    catch(region)
                    basic(region, pos_x, pos_y)
                elif field.grid[i][j] == 2:  # ловушка
                    pass
                elif field.grid[i][j] == 3:  # ладан
                    pass
            if event.type == pygame.MOUSEBUTTONDOWN and 750 <= list(event.pos)[0] <= 1000 and \
                    40 <= list(event.pos)[1] <= 100:
                hello()
            elif event.type == pygame.MOUSEBUTTONDOWN and 730 <= list(event.pos)[0] <= 1000 and \
                    100 <= list(event.pos)[1] <= 260:
                display()
                basic(region, pos_x, pos_y)
            elif event.type == pygame.MOUSEBUTTONDOWN and 730 <= list(event.pos)[0] <= 1000 and \
                    480 <= list(event.pos)[1] <= 580:
                info()
                basic(region, pos_x, pos_y)
        pygame.display.flip()


if __name__ == '__main__':
    hello()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
    
