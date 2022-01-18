import binascii
import pygame
import os
from random import randrange


# from сapture import fishing


def background(region):  # отрисовывание поля
    size = 900, 600
    screen = pygame.display.set_mode(size)
    screen.fill((204, 204, 204))
    screen.fill((255, 204, 0), pygame.Rect(10, 20, 700, 560))
    # вертикальные линии
    for i in range(0, 11):
        pygame.draw.line(screen, (255, 0, 0), (70 * i + 10, 20),
                         (70 * i + 10, 580), width=5)
    # горизонтальные линии
    for i in range(0, 9):
        pygame.draw.line(screen, (255, 0, 0), (10, 70 * i + 20),
                         (710, 70 * i + 20), width=5)

    if region == "kanto":
        font = pygame.font.Font(None, 50)
        text = font.render("Паллет-таун", True, (0, 0, 0))
        screen.blit(text, (750, 40))
    elif region == "johto":
        font = pygame.font.Font(None, 40)
        text = font.render("Петалбург-Сити", True, (0, 0, 0))
        screen.blit(text, (750, 40))
    elif region == "hoenn":
        font = pygame.font.Font(None, 50)
        text = font.render("Литлрут-Таун", True, (0, 0, 0))
        screen.blit(text, (750, 40))


def hello():
    pygame.init()
    pygame.display.set_caption('Pokemon Yellow')
    size = 900, 600
    screen = pygame.display.set_mode(size)
    screen.fill((204, 204, 204))
    intro_text = ["      ВЫБЕРИТЕ РЕГИОН", "",
                  "      Канто", "      Джото", "      Хоенн"]
    fullname = os.path.join('data', "pokeball.png")
    image = pygame.image.load(fullname)
    screen.blit(image, (10, 200))
    screen.blit(image, (10, 290))
    screen.blit(image, (10, 380))
    font = pygame.font.Font(None, 90)
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
            if event.type == pygame.MOUSEBUTTONDOWN and 10 <= list(event.pos)[0] <= 90:
                if 200 <= list(event.pos)[1] <= 280:
                    basic("kanto")
                elif 290 <= list(event.pos)[1] <= 370:
                    basic("johto")
                elif 380 <= list(event.pos)[1] <= 460:
                    basic("hoenn")
            pygame.display.flip()


def basic(region):
    size = 900, 600
    screen = pygame.display.set_mode(size)
    background(region)

    # перемещение героя
    fullname = os.path.join('data', "trainer.png")
    image = pygame.image.load(fullname)
    screen.blit(image, (10, 20))
    pos_x = 10
    pos_y = 20
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and pos_x > 10:
                    pos_x -= 70
                    background(region)
                    screen.blit(image, (pos_x, pos_y))
                if event.key == pygame.K_RIGHT and pos_x < 640:
                    pos_x += 70
                    background(region)
                    screen.blit(image, (pos_x, pos_y))
                if event.key == pygame.K_UP and pos_y > 20:
                    pos_y -= 70
                    background(region)
                    screen.blit(image, (pos_x, pos_y))
                if event.key == pygame.K_DOWN and pos_y < 510:
                    pos_y += 70
                    background(region)
                    screen.blit(image, (pos_x, pos_y))
                if randrange(100) < 15:  # есть покемон или нет
                    # fishing(region)
                    pass
            if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and list(event.pos)[0] >= 750
                    and list(event.pos)[0] <= 1000
                    and list(event.pos)[1] >= 40
                    and list(event.pos)[1] <= 100
            ):
                hello()
            pygame.display.flip()


if __name__ == '__main__':
    r = hello()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
