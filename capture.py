import sqlite3
import pygame
from random import randrange, choice


def catch(region):
    variants = None
    f = randrange(100)
    if f < 85:
        rarity = "ordinary"
    elif f < 95:
        rarity = "legendary"
    else:
        rarity = "mythical"
    con = sqlite3.connect("Pokemon.db")
    cur = con.cursor()
    if region == "Kanto":
        variants = list(cur.execute(
            f"SELECT name, element FROM Kanto WHERE rarity = '{rarity}'").fetchall())
    elif region == "Johto":
        variants = list(cur.execute(
            f"SELECT name, element FROM Johto WHERE rarity = '{rarity}'").fetchall())
    elif region == "Hoenn":
        variants = list(cur.execute(
            f"SELECT name, element FROM Hoenn WHERE rarity = '{rarity}'").fetchall())
    total = list(choice(variants))
    pygame.init()
    pygame.display.set_caption('Choose your Pokemon')
    size = 900, 600
    screen = pygame.display.set_mode(size)
    screen.fill((204, 204, 204))
    font = pygame.font.Font(None, 50)
    text = font.render("Вы встретили нового покемона: " + total[0], True, (0, 0, 0))
    screen.blit(text, (140, 80))
    text = font.render("Выберите тип своего покемона:", True, (0, 0, 0))
    screen.blit(text, (210, 250))
    con = sqlite3.connect("Caught.db")
    cur = con.cursor()
    variants = list(cur.execute("SELECT element FROM Caught").fetchall())
    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()


catch("Kanto")
