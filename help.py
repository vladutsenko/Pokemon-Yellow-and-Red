import pygame


def blit_text(surface, text, pos):
    font = pygame.font.Font("data/corbell.ttf", 20)
    font.bold = True
    space = font.size(' ')[0]
    w, h = surface.get_size()
    x, y = pos
    ww, wh = 0, 0
    for line in text.splitlines():
        for word in line.split(' '):
            ws = font.render(word, True, (227, 8, 0))
            ww, wh = ws.get_size()
            if x + ww >= w:
                x = pos[0]
                y += wh
            surface.blit(ws, (x, y))
            x += ww + space
        x = pos[0]
        y += wh / 2


def info():
    pygame.display.set_caption("Help")
    screen3 = pygame.display.set_mode((900, 600))
    bg = pygame.image.load("data/Pallet-Town.png")
    screen3.blit(bg, (0, 0))
    pygame.init()
    text = """Добро пожаловать в Pokemon: Yellow and Red!\n
В этой игре вам предстоит перемещаться по клетчатому полю и ловить покемонов. Перемещение по клеткам осуществляется с помощью клавиш W, A, S, D.\n
В каждой клетке с вероятностью 20% можно встретить покемона. В этом случае вы можете сразиться с ним, чтобы заполучить его в свою коллекцию. В битве можно использовать тех покемонов, которых вы уже поймали. Изначально у вас есть 1 начальный покемон в коллекции – Бульбазавр (травяной). Всех пойманных покемонов можно увидеть, нажав на рюкзак на начальном экране.\n
Чтобы шансы на победу были выше, нужно использовать подходящий тип покемонов. По умолчанию у вашего покемона есть сила атаки, равная 1000, шанс крит. попадания 5%, крит. урон 50% и бонус урона 0%. В зависимости от типа вашего покемона и того покемона, которого вы ловите, могут быть получены следующие дополнительные эффекты:\n
o   Если использовать огненного покемона против травяного, сила атаки вашего покемона увеличивается на 25%\n
o   Если использовать водного покемона против огненного, бонус урона увеличивается на 100%\n
o   Если использовать огненного покемона против водного, бонус урона увеличивается на 50%\n
o   Если использовать нормального покемона против насекомого, крит. урон увеличивается на 20%\n
o   Если использовать водного покемона против насекомого, шанс крит. попадания увеличивается на 15%\n
o   Если использовать насекомого против травяного покемона, шанс крит. попадания уменьшается на 5%, а крит. урон увеличивается на 50%\n
Кроме того, существует 10% вероятность попасть в ловушку и 10% вероятность найти ладан. Попадание в ловушку отбирает у вас 1 случайного покемона, а ладан делает следующую поимку покемона заведомо успешной.
"""
    blit_text(screen3, text, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 4:
                screen3.scroll(0, 20)
            if event.type == pygame.MOUSEBUTTONUP and event.button == 5:
                screen3.scroll(0, -20)
        pygame.display.flip()
    pygame.quit()
