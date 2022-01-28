import pygame
import sqlite3

screen2 = pygame.display.set_mode((600, 400))
pygame.init()


def display():
    pygame.mixer.music.load('data/choose_pokemon.mp3')
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)
    pygame.display.set_caption("Collection")
    global screen2
    screen2 = pygame.display.set_mode((600, 400))
    pygame.init()
    bg = pygame.image.load("data/battle-background.png")
    screen2.blit(bg, (0, 0))
    font = pygame.font.Font("data/corbell.ttf", 15)
    font.bold = True
    pygame.draw.rect(screen2, (255, 0, 0), (575, 60, 20, 20))
    text = font.render("1", True, (255, 255, 255))
    screen2.blit(text, (585, 65))
    c = sqlite3.connect("Pokemon.db")
    cur = c.cursor()
    info = cur.execute("SELECT * FROM Collection").fetchall()
    if len(info) > 9:
        pygame.draw.rect(screen2, (255, 0, 0), (575, 90, 20, 20))
        text = font.render("2", True, (255, 255, 255))
        screen2.blit(text, (585, 95))
    show(info, 1)
    t = 1
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 575 <= x <= 595:
                    if 60 <= y <= 80:
                        t = 1
                    elif 90 <= y <= 110 and len(info) >= 12:
                        t = 2
        bg = pygame.image.load("data/battle-background.png")
        screen2.blit(bg, (0, 0))
        show(info, t)
        pygame.display.flip()
    pygame.quit()


def show(info, t):
    global screen2

    font = pygame.font.Font("data/corbell.ttf", 15)
    font.bold = True
    if t == 1:
        pygame.draw.rect(screen2, (255, 0, 0), (575, 60, 20, 20))
        text = font.render("1", True, (255, 255, 255))
        screen2.blit(text, (585, 65))
        pygame.draw.rect(screen2, (148, 19, 19), (575, 90, 20, 20))
        text = font.render("2", True, (255, 255, 255))
        screen2.blit(text, (585, 95))
        for i in range(len(info) // 3):
            image = pygame.image.load(f"data/{info[i * 3][0]}.png")
            screen2.blit(image, (20, 20 + i * 125))
            text = font.render(
                f"{info[i * 3][0]} ({info[i * 3][1]})", True, (227, 8, 0))
            screen2.blit(text, (20, 120 + i * 125))
            image = pygame.image.load(f"data/{info[i * 3 + 1][0]}.png")
            screen2.blit(image, (220, 20 + i * 125))
            text = font.render(
                f"{info[i * 3 + 1][0]} ({info[i * 3 + 1][1]})", True, (227, 8, 0))
            screen2.blit(text, (220, 120 + i * 125))
            image = pygame.image.load(f"data/{info[i * 3 + 2][0]}.png")
            screen2.blit(image, (420, 20 + i * 125))
            text = font.render(
                f"{info[i * 3 + 2][0]} ({info[i * 3 + 2][1]})", True, (227, 8, 0))
            screen2.blit(text, (420, 120 + i * 125))
        for i in range(len(info) % 3):
            image = pygame.image.load(
                f"data/{info[i + len(info) // 3 * 3][0]}.png")
            screen2.blit(image, (20 + 200 * i, 20 + len(info) // 3 * 125))
            text = font.render(
                f"{info[i + len(info) // 3 * 3][0]} ({info[i + len(info) // 3 * 3][1]})", True, (227, 8, 0))
            screen2.blit(text, (20 + 200 * i, 120 + len(info) // 3 * 125))
    else:
        pygame.draw.rect(screen2, (148, 19, 19), (575, 60, 20, 20))
        text = font.render("1", True, (255, 255, 255))
        screen2.blit(text, (585, 65))
        pygame.draw.rect(screen2, (255, 0, 0), (575, 90, 20, 20))
        text = font.render("2", True, (255, 255, 255))
        screen2.blit(text, (585, 95))
        for i in range((len(info) - 9) // 3):
            image = pygame.image.load(f"data/{info[i * 3 + 9][0]}.png")
            screen2.blit(image, (20, 20 + i * 125))
            text = font.render(
                f"{info[i * 3 + 9][0]} ({info[i * 3 + 9][1]})", True, (227, 8, 0))
            screen2.blit(text, (20, 120 + i * 125))
            image = pygame.image.load(f"data/{info[i * 3 + 10][0]}.png")
            screen2.blit(image, (220, 20 + i * 125))
            text = font.render(
                f"{info[i * 3 + 10][0]} ({info[i * 3 + 10][1]})", True, (227, 8, 0))
            screen2.blit(text, (220, 120 + i * 125))
            image = pygame.image.load(f"data/{info[i * 3 + 11][0]}.png")
            screen2.blit(image, (420, 20 + i * 125))
            text = font.render(
                f"{info[i * 3 + 11][0]} ({info[i * 3 + 11][1]})", True, (227, 8, 0))
            screen2.blit(text, (420, 120 + i * 125))
        for i in range(len(info) % 3):
            image = pygame.image.load(
                f"data/{info[i + len(info) // 3 * 3][0]}.png")
            screen2.blit(image, (20 + 200 * i, 20 + len(info) // 3 * 125))
            text = font.render(
                f"{info[i + len(info) // 3 * 3][0]} ({info[i + len(info) // 3 * 3][1]})", True, (227, 8, 0))
            screen2.blit(text, (20 + 200 * i, 120 + len(info) // 3 * 125))
