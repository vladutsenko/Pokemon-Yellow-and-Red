import sqlite3
import pygame
from random import randrange, choice

screen1 = pygame.display.set_mode((680, 400))


def catch(region):
    global screen1
    pygame.display.set_caption('Catch the Pokemon!')
    screen1 = pygame.display.set_mode((680, 400))
    pygame.init()

    elements = []
    con = sqlite3.connect("Pokemon.db")
    cur = con.cursor()
    if region == "Kanto":
        elements = list(cur.execute(
            f"SELECT name, element FROM Kanto WHERE name NOT IN (SELECT name FROM Collection)").fetchall())
    elif region == "Johto":
        elements = list(cur.execute(
            f"SELECT name, element FROM Johto WHERE name NOT IN (SELECT name FROM Collection)").fetchall())
    elif region == "Hoenn":
        elements = list(cur.execute(
            f"SELECT name, element FROM Hoenn WHERE name NOT IN (SELECT name FROM Collection)").fetchall())
    total = list(choice(elements))
    bg = pygame.image.load("data/battle-background.png")
    screen1.blit(bg, (0, 0))
    font = pygame.font.Font("data/corbell.ttf", 20)
    font.bold = True
    text = font.render(f"Вы встретили нового покемона: {total[0]} (тип - {total[1]})", True, (227, 8, 0))
    screen1.blit(text, (40, 20))
    text = font.render("Выберите своего покемона:", True, (227, 8, 0))
    screen1.blit(text, (40, 60))
    pokemons = cur.execute("SELECT name, element FROM Collection").fetchall()
    image = pygame.image.load("data/pokeball.png")
    font = pygame.font.Font("data/corbell.ttf", 20)
    font.bold = True
    for i, line in enumerate(pokemons):
        text = font.render(line[0] + "," + line[1], True, (227, 8, 0))
        screen1.blit(text, (100, 110 + 50 * i))
        screen1.blit(image, (40, 100 + 50 * i))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i, pokemon in enumerate(pokemons):
                    if 110 + 50 * i <= y < 160 + 50 * i and 40 < x < 140:
                        battle(total, pokemon)
                        running = False
                        break
        if not running:
            break
        pygame.display.flip()
    pygame.quit()


def battle(pokemon1, pokemon2):
    global screen1
    atk = 1000
    crit_rate = 15
    crit_dmg = 50
    bonus_dmg = 0
    if pokemon1[1] == "травяной" and pokemon2[1] == "огненный":
        atk *= 1.25
    elif pokemon1[1] == "огненный" and pokemon2[1] == "водный":
        bonus_dmg = 100
    elif pokemon1[1] == "водный" and pokemon2[1] == "огненный":
        bonus_dmg = 50
    elif pokemon1[1] == "насекомое" and pokemon2[1] == "нормальный":
        crit_dmg += 20
    elif pokemon1[1] == "насекомое" and pokemon2[1] == "водный":
        crit_rate += 15
    elif pokemon1[1] == "травяной" and pokemon2[1] == "насекомое":
        crit_rate -= 5
        crit_dmg += 50
    image1 = pygame.image.load(f"data/{pokemon1[0]}.png")
    image2 = pygame.image.load(f"data/{pokemon2[0]}.png")
    screen1.blit(image1, (400, 100))
    screen1.blit(image2, (550, 100))
    pygame.draw.rect(screen1, (255, 0, 0), (400, 90, 90, 5))
    pygame.draw.rect(screen1, (255, 0, 0), (550, 90, 90, 5))
    hp1 = 10000
    hp2 = 10000
    pygame.draw.rect(screen1, (255, 0, 0), (450, 220, 80, 40))
    font = pygame.font.Font("data/corbell.ttf", 20)
    font.bold = True
    text = font.render("Атака", True, (0, 0, 0))
    screen1.blit(text, (465, 230))
    running = True
    win = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # print("hit")
                x, y = event.pos
                if 450 < x < 530 and 220 < y < 260:
                    dmg1 = (atk if randrange(100) > crit_rate else atk * (1 + crit_dmg / 100)) \
                           * (1 + bonus_dmg / 100)
                    dmg2 = 1000
                    pygame.draw.rect(screen1, (92, 215, 90),
                                     (490 - min(90.0, dmg1 / hp1 * 90), 90, min(90.0, dmg1 / hp1 * 90), 5))
                    pygame.draw.rect(screen1, (92, 215, 90),
                                     (640 - min(90.0, dmg2 / hp2 * 90), 90, min(90.0, dmg2 / hp2 * 90), 5))
                    hp1 -= dmg1
                    if hp1 <= 0 and hp2:
                        win = True
                        running = False
                    hp2 -= dmg2
                    if hp1 and hp2 <= 0:
                        running = False
            pygame.display.flip()
    if win:
        con = sqlite3.connect("Pokemon.db")
        cur = con.cursor()
        cur.execute(f"INSERT INTO Collection (name, element) VALUES ('{pokemon1[0]}', '{pokemon1[1]}')")
        con.commit()
        text = font.render("Победа", True, (0, 0, 0))
        screen1.blit(text, (460, 325))
        con.close()
    else:
        text = font.render("Поражение", True, (0, 255, 0))
        screen1.blit(text, (460, 325))
    pygame.time.delay(2000)
    pygame.quit()
