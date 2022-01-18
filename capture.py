import sqlite3
import pygame
from random import randrange, choice


def fishing(region):
    if __name__ != '__main__':
        return

    f = randrange(100)
    if f < 85:
        type = "ordinary"
    elif f < 95:
        type = "legendary"
    else:
        type = "mythical"

    con = sqlite3.connect("Pokemon.db")
    cur = con.cursor()
    if region == "Kanto":
        variants = list(cur.execute(
            "SELECT name, element FROM Kanto WHERE type == ?", (type, )).fetchall())
    elif region == "Johto":
        variants = list(cur.execute(
            "SELECT name, element FROM Johto WHERE type == ?", (type, )).fetchall())
    elif region == "Hoenn":
        variants = list(cur.execute(
            "SELECT name, element FROM Hoenn WHERE type == ?", (type, )).fetchall())
    total = list(choice(variants))
    pygame.init()
    pygame.display.set_caption('Choose your Pokemon')
    size = width, height = 1000, 750
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


fishing("Kanto")
