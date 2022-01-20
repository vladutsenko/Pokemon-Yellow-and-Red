import pygame
import sqlite3


def display():
    pygame.display.set_caption("Collection")
    screen2 = pygame.display.set_mode((600, 400))
    bg = pygame.image.load("data/battle-background.png")
    screen2.blit(bg, (0, 0))
    pygame.init()
    c = sqlite3.connect("Pokemon.db")
    cur = c.cursor()
    font = pygame.font.Font("data/corbell.ttf", 15)
    font.bold = True
    info = cur.execute("SELECT * FROM Collection").fetchall()
    for i in range(len(info) // 3):
        image = pygame.image.load(f"data/{info[i * 3][0]}.png")
        screen2.blit(image, (50, 50 + i * 125))
        text = font.render(f"{info[i * 3][0]} ({info[i * 3][1]})", True, (227, 8, 0))
        screen2.blit(text, (50, 150 + i * 125))
        image = pygame.image.load(f"data/{info[i * 3 + 1][0]}.png")
        screen2.blit(image, (250, 50 + i * 125))
        text = font.render(f"{info[i * 3 + 1][0]} ({info[i * 3 + 1][1]})", True, (227, 8, 0))
        screen2.blit(text, (250, 150 + i * 125))
        image = pygame.image.load(f"data/{info[i * 3 + 2][0]}.png")
        screen2.blit(image, (450, 50 + i * 125))
        text = font.render(f"{info[i * 3 + 2][0]} ({info[i * 3 + 2][1]})", True, (227, 8, 0))
        screen2.blit(text, (450, 150 + i * 125))
    for i in range(len(info) % 3):
        image = pygame.image.load(f"data/{info[i + len(info) // 3 * 3][0]}.png")
        screen2.blit(image, (50 + 200 * i, 50 + len(info) // 3 * 125))
        text = font.render(f"{info[i + len(info) // 3 * 3][0]} ({info[i + len(info) // 3 * 3][1]})", True, (227, 8, 0))
        screen2.blit(text, (50 + 200 * i, 150 + len(info) // 3 * 125))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 4:
                screen2.scroll(0, 20)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 5:
                screen2.scroll(0, -20)
        pygame.display.flip()
    pygame.quit()
