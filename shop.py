import pygame


def buy(pokeball):
    pygame.display.set_caption('Покецентр')
    screen4 = pygame.display.set_mode((900, 500))
    pygame.init()
    screen4.fill((204, 204, 204))
    font = pygame.font.Font("data/corbell.ttf", 35)
    font.bold = True
    font2 = pygame.font.Font("data/corbell.ttf", 20)
    font2.bold = False
    bg = pygame.image.load("data/red.png")
    text = font.render("Покеболл", True, (0, 0, 0))
    text2 = font2.render(
        "Стандартный покеболл. Шанс поймать покемона 60%.", True, (0, 0, 0))
    screen4.blit(text2, (150, 110))
    screen4.blit(text, (150, 70))
    screen4.blit(bg, (20, 50))
    screen4.fill((255, 0, 0), pygame.Rect(650, 60, 200, 70))
    text = font.render("Бесплатно", True, (255, 255, 255))
    screen4.blit(text, (660, 80))
    bg = pygame.image.load("data/blue.png")
    text = font.render("Мегаболл", True, (0, 0, 0))
    text2 = font2.render(
        "Улучшенный покеболл. Шанс поймать покемона 80%.", True, (0, 0, 0))
    screen4.blit(text2, (150, 210))
    screen4.blit(text, (150, 170))
    screen4.blit(bg, (20, 150))
    screen4.fill((255, 0, 0), pygame.Rect(650, 160, 200, 70))
    text = font.render("30 руб.", True, (255, 255, 255))
    screen4.blit(text, (690, 180))
    bg = pygame.image.load("data/yellow.png")
    text = font.render("Ультраболл", True, (0, 0, 0))
    text2 = font2.render(
        "Улучшенный покеболл. Шанс поймать покемона 95%.", True, (0, 0, 0))
    screen4.blit(text2, (150, 310))
    screen4.blit(text, (150, 270))
    screen4.blit(bg, (20, 250))
    screen4.fill((255, 0, 0), pygame.Rect(650, 260, 200, 70))
    text = font.render("60 руб.", True, (255, 255, 255))
    screen4.blit(text, (690, 280))
    bg = pygame.image.load("data/incense.png")
    text = font.render("Ладан", True, (0, 0, 0))
    text2 = font2.render(
        "Ладан. Шанс найти покемона увеличиватся до 60%.", True, (0, 0, 0))
    screen4.blit(text2, (150, 410))
    screen4.blit(text, (150, 370))
    screen4.blit(bg, (20, 350))
    screen4.fill((255, 0, 0), pygame.Rect(650, 360, 200, 70))
    text = font.render("50 руб.", True, (255, 255, 255))
    screen4.blit(text, (690, 380))

    text1 = font2.render("Ошибка оплаты. Мы уже её решаем...", True, (0, 0, 0))
    text3 = font2.render("Закончились бесплатные покеболлы", True, (0, 0, 0))

    d = 10
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                return pokeball
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                screen4.fill((204, 204, 204), pygame.Rect(20, 460, 700, 70))
                if 650 < x < 850 and 60 < y < 130:
                    if d > 0:
                        pokeball = pokeball + 1
                        d = d - 1
                        text2 = font2.render(
                            "Получен 1 покеболл. Осталось: " + str(d), True, (0, 0, 0))
                        screen4.blit(text2, (20, 460))
                    else:
                        screen4.blit(text3, (20, 460))
                elif 650 < x < 850 and 160 < y < 230:
                    screen4.blit(text1, (20, 460))
                elif 650 < x < 850 and 260 < y < 330:
                    screen4.blit(text1, (20, 460))
                elif 650 < x < 850 and 360 < y < 430:
                    screen4.blit(text1, (20, 460))
        pygame.display.flip()
    pygame.quit()
