import sqlite3
import pygame
from random import randrange, choice

size = 600, 600
screen1 = pygame.display.set_mode(size)
pygame.init()
pygame.display.set_caption('Choose your Pokemon')


def catch(region):
    global screen1
    elements = []
    f = randrange(100)
    if f < 85:
        rarity = "стандартный"
    elif f < 95:
        rarity = "легендарный"
    else:
        rarity = "мифический"
    con = sqlite3.connect("Pokemon.db")
    cur = con.cursor()
    if region == "Kanto":
        elements = list(cur.execute(
            f"SELECT name, element FROM Kanto WHERE rarity = '{rarity}'").fetchall())
    elif region == "Johto":
        elements = list(cur.execute(
            f"SELECT name, element FROM Johto WHERE rarity = '{rarity}'").fetchall())
    elif region == "Hoenn":
        elements = list(cur.execute(
            f"SELECT name, element FROM Hoenn WHERE rarity = '{rarity}'").fetchall())
    if not elements:
        print(rarity)
    total = list(choice(elements))
    screen1.fill((204, 204, 204))
    font = pygame.font.Font(None, 30)
    text = font.render("Вы встретили нового покемона: " + total[0], True, (0, 0, 0))
    screen1.blit(text, (40, 20))
    text = font.render("Выберите своего покемона:", True, (0, 0, 0))
    screen1.blit(text, (40, 60))
    pokemons = cur.execute("SELECT name, element FROM Collection").fetchall()
    image = pygame.image.load("data/pokeball.png")
    font = pygame.font.Font(None, 30)
    for i, line in enumerate(pokemons):
        text = font.render(line[0] + "," + line[1], True, (0, 0, 255))
        screen1.blit(text, (100, 110 + 90 * i))
        screen1.blit(image, (40, 100 + 90 * i))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and 10 <= list(event.pos)[0] <= 90:
                x, y = event.pos
                for i, pokemon in enumerate(pokemons):
                    if 110 + 90 * i <= y < 200 + 90 * i:
                        print(total)
                        battle(total, pokemon)
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
    image1 = pygame.image.load(f"data/{pokemon1[0]}")
    image2 = pygame.image.load(f"data/{pokemon2[0]}")
    screen1.blit(image1, 300, 100)
    screen1.blit(image2, 450, 100)
    pygame.draw.rect(screen1, (255, 0, 0), (300, 90, 90, 5))
    pygame.draw.rect(screen1, (255, 0, 0), (450, 90, 90, 5))
    hp1 = 10000
    hp2 = 10000
    pygame.draw.rect(screen1, (255, 0, 0), (350, 220, 50, 20))
    font = pygame.font.Font(None, 10)
    text = font.render("Атака", True, (0, 0, 0))
    screen1.blit(text, (360, 225))
    running = True
    win = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and 10 <= list(event.pos)[0] <= 90:
                x, y = event.pos
                if 220 < y < 240:
                    dmg1 = (atk if randrange(100) > crit_rate else atk * (1 + crit_dmg) / 100) \
                           * (1 + bonus_dmg) / 100
                    dmg2 = 1000
                    pygame.draw.rect(screen1, (204, 204, 204), (390 - dmg1 / hp1 * 90, 90, dmg1 / hp1 * 90, 5))
                    pygame.draw.rect(screen1, (255, 204, 204), (450 - dmg2 / hp2 * 90, 90, dmg2 / hp2 * 90, 5))
                    hp1 -= dmg1
                    hp2 -= dmg2
                    if hp1 <= 0 or hp2 <= 0:
                        if hp2:
                            win = True
                        running = False
            pygame.display.flip()
    if win:
        con = sqlite3.connect("Pokemon.db")
        cur = con.cursor()
        cur.execute(f"INSERT INTO Collection VALUES ({pokemon1[0]}, {pokemon1[1]})")
        text = font.render("Победа", True, (0, 255, 0))
        screen1.blit(text, (360, 325))
    else:
        text = font.render("Поражение", True, (0, 255, 0))
        screen1.blit(text, (360, 325))
    pygame.quit()
