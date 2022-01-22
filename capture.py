import sqlite3
import pygame
from random import randrange, choice
import logging

screen1 = pygame.display.set_mode((680, 400))
hp1 = 10000
hp2 = 10000
all_sprites = pygame.sprite.Group()
logging.basicConfig(filename='pokemons.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('capture-logger')
logger.setLevel(logging.DEBUG)


class Pokemon(pygame.sprite.Sprite):
    def __init__(self, image, pos, d, opponent=None):
        super().__init__(all_sprites)
        self.image = image
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos
        self.x0 = pos[0]
        self.dir = d
        self.opponent = opponent
        self.collision = False

    def update(self):
        if pygame.sprite.collide_mask(self, self.opponent):
            self.dir = -self.dir
            self.collision = True
        self.rect = self.rect.move(self.dir, 0)


def catch(region, pokeball):
    global screen1
    pygame.display.set_caption('Catch the Pokemon!')
    screen1 = pygame.display.set_mode((680, 400))
    pygame.init()
    elements = []
    con = sqlite3.connect("Pokemon.db")
    cur = con.cursor()
    if region == "Kanto":
        elements = list(cur.execute(
            f"SELECT name, element, rarity FROM Kanto WHERE name NOT IN (SELECT name FROM Collection)").fetchall())
    elif region == "Johto":
        elements = list(cur.execute(
            f"SELECT name, element, rarity FROM Johto WHERE name NOT IN (SELECT name FROM Collection)").fetchall())
    elif region == "Hoenn":
        elements = list(cur.execute(
            f"SELECT name, element, rarity FROM Hoenn WHERE name NOT IN (SELECT name FROM Collection)").fetchall())
    pokemon = list(choice(elements))
    redraw(pokemon)
    font = pygame.font.Font("data/corbell.ttf", 20)
    font.bold = True
    text = font.render("Выберите своего покемона:", True, (227, 8, 0))
    screen1.blit(text, (40, 70))
    pokemons = cur.execute("SELECT name, element FROM Collection").fetchall()
    image = pygame.image.load("data/pokeball.png")
    font.bold = True
    for i, line in enumerate(pokemons):
        text = font.render(line[0] + "," + line[1], True, (227, 8, 0))
        screen1.blit(text, (100, 110 + 50 * i))
        screen1.blit(image, (40, 100 + 50 * i))
    running = True
    p = -1
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                for i, p in enumerate(pokemons):
                    if 110 + 50 * i <= y < 160 + 50 * i and 40 < x < 140:
                        p = battle(pokemon, p, region, pokeball)
                        running = False
                        break
        if not running:
            break
        pygame.display.flip()
    pygame.quit()
    return p


def battle(pokemon1, pokemon2, region, pokeball):
    global screen1, hp1, hp2
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
    logger.debug(f"started battle, hp1 = {hp1}, hp2 = {hp2}")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if 450 < x < 530 and 220 < y < 260:
                    res = attack(pokemon1, pokemon2, region)
                    logger.debug(f"hp1 = {hp1}, hp2 = {hp2}")
                    logger.debug(f"total damage: 1 - {min(10000, 10000 - hp1)}, 2 - {min(10000, 10000 - hp2)}")
                    logger.debug(f"damage bar length: 1 - {min(10000, 10000 - hp1) / hp1 * 90}, "
                                 f"2 - {min(10000, 10000 - hp2) / hp2 * 90}")
                    pygame.draw.rect(screen1, (92, 215, 90),
                                     (490 - min(10000, 10000 - hp1) / 10000 * 90, 90,
                                      min(10000, 10000 - hp1) / 10000 * 90, 5))
                    pygame.draw.rect(screen1, (92, 215, 90),
                                     (640 - min(10000, 10000 - hp2) / 10000 * 90, 90,
                                      min(10000, 10000 - hp2) / 10000 * 90, 5))
                    pygame.display.flip()
                    logger.debug("hp bar updated in battle()")
                    if res == 1:
                        win = True
                        running = False
                    elif res == -1:
                        running = False
            image1 = pygame.image.load(f"data/{pokemon1[0]}.png")
            image2 = pygame.image.load(f"data/{pokemon2[0]}.png")
            screen1.blit(image1, (400, 100))
            screen1.blit(image2, (550, 100))
            pygame.display.flip()
    if win:
        text = font.render("Победа", True, (0, 0, 0))
        screen1.blit(text, (460, 325))
        pygame.display.flip()
        pygame.time.delay(2000)
        bg = pygame.image.load("data/battle-background.png")
        screen1.blit(bg, (0, 0))
        font = pygame.font.Font("data/corbell.ttf", 20)
        font.bold = True
        text = font.render("Выбрите свой покеболл:", True, (0, 0, 0))
        screen1.blit(text, (20, 20))
        f = pygame.image.load("data/red.png")
        screen1.blit(f, (20, 50))
        f = pygame.image.load("data/blue.png")
        screen1.blit(f, (220, 50))
        f = pygame.image.load("data/yellow.png")
        screen1.blit(f, (420, 50))
        pygame.display.flip()
        font = pygame.font.Font("data/corbell.ttf", 20)
        font.bold = True
        text2 = font.render("Покемон пойман", True, (0, 0, 0))
        text3 = font.render("Покемон сбежал", True, (0, 0, 0))
        text4 = font.render("У вас нет этого покеболла", True, (0, 0, 0))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = event.pos
                    if 5 < y < 150:
                        bg = pygame.image.load("data/battle-background.png")
                        screen1.blit(bg, (0, 0))
                        font = pygame.font.Font("data/corbell.ttf", 20)
                        font.bold = True
                        text = font.render(
                            "Выберите свой покеболл:", True, (0, 0, 0))
                        screen1.blit(text, (20, 20))
                        f = pygame.image.load("data/red.png")
                        screen1.blit(f, (20, 50))
                        f = pygame.image.load("data/blue.png")
                        screen1.blit(f, (220, 50))
                        f = pygame.image.load("data/yellow.png")
                        screen1.blit(f, (420, 50))
                        pygame.display.flip()
                        if 20 < x < 120 and pokeball > 0:
                            f = randrange(100)
                            if f <= 100:
                                screen1.blit(text2, (20, 300))
                                con = sqlite3.connect("Pokemon.db")
                                cur = con.cursor()
                                cur.execute(
                                    f"INSERT INTO Collection (name, element) VALUES ('{pokemon1[0]}', '{pokemon1[1]}')")
                                con.commit()
                                con.close()
                                running = False
                                break
                            else:
                                screen1.blit(text3, (20, 300))
                                running = False
                                break
                        elif 220 < x < 320 or 420 < x < 520 or pokeball == 0:
                            screen1.blit(text4, (20, 300))
            pygame.display.flip()
        pygame.time.delay(1000)
        pygame.quit()

    else:
        text = font.render("Поражение", True, (227, 8, 0))
        pygame.time.delay(1000)
        screen1.blit(text, (460, 325))
        pygame.display.flip()
        pygame.quit()
    return pokeball


def redraw(pokemon):
    global screen1
    bg = pygame.image.load("data/battle-background.png")
    screen1.blit(bg, (0, 0))
    font = pygame.font.Font("data/corbell.ttf", 20)
    font.bold = True
    text = font.render(
        f"Вы встретили {pokemon[2][:-2]}ого покемона: ", True, (227, 8, 0))
    screen1.blit(text, (40, 20))
    text = font.render(f"{pokemon[0]} ({pokemon[1]})", True, (227, 8, 0))
    screen1.blit(text, (40, 40))


def attack(pokemon1, pokemon2, region):
    global hp1, hp2, screen1
    logger.debug("Attack sequence started")
    atk = 1000
    crit_rate = 15
    crit_dmg = 50
    bonus_dmg = 0
    if pokemon2[0] != "Бульбазавр":
        c = sqlite3.connect("Pokemon.db")
        cur = c.cursor()
        stats = cur.execute(f"SELECT atk, crit_rate, crit_dmg FROM {region} WHERE name = '{pokemon2[0]}'").fetchall()[0]
        atk, crit_rate, crit_dmg = stats
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
    sprite1 = Pokemon(image1, (400, 100), 1)
    sprite2 = Pokemon(image2, (550, 100), -1)
    sprite1.opponent = sprite2
    sprite2.opponent = sprite1
    all_sprites.add(sprite1)
    all_sprites.add(sprite2)
    running = True
    clock = pygame.time.Clock()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        all_sprites.update()
        if sprite1.collision and sprite1.rect.x <= 400:
            running = False
        redraw(pokemon1)
        pygame.draw.rect(screen1, (255, 0, 0), (400, 90, 90, 5))
        pygame.draw.rect(screen1, (255, 0, 0), (550, 90, 90, 5))
        pygame.draw.rect(screen1, (255, 0, 0), (450, 220, 80, 40))
        pygame.draw.rect(screen1, (92, 215, 90),
                         (490 - min(10000, 10000 - hp1) / 10000 * 90, 90,
                          min(10000, 10000 - hp1) / 10000 * 90, 5))
        pygame.draw.rect(screen1, (92, 215, 90),
                         (640 - min(10000, 10000 - hp2) / 10000 * 90, 90,
                          min(10000, 10000 - hp2) / 10000 * 90, 5))
        font = pygame.font.Font("data/corbell.ttf", 20)
        font.bold = True
        text = font.render("Атака", True, (0, 0, 0))
        screen1.blit(text, (465, 230))
        all_sprites.draw(screen1)
        pygame.display.flip()
        clock.tick(300)
    all_sprites.remove(sprite1)
    all_sprites.remove(sprite2)
    dmg1 = (atk if randrange(100) > crit_rate else atk * (1 + crit_dmg / 100)) * (1 + bonus_dmg / 100)
    dmg2 = 1110
    hp1 -= dmg1
    if hp1 <= 0 and hp2:
        return 1
    hp2 -= dmg2
    if hp1 and hp2 <= 0:
        return -1
    return 0
