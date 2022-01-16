import pygame
import os
from random import randrange
from сapture import fishing


def background():  # отрисовывание поля
    screen.fill((255, 204, 0), pygame.Rect(10, 20, 700, 560))
    # вертикальные линии
    for i in range(0, 11):
        pygame.draw.line(screen, (255, 0, 0), (70 * i + 10, 20),
                         (70 * i + 10, 580), width=5)
    # горизонтальные линии
    for i in range(0, 9):
        pygame.draw.line(screen, (255, 0, 0), (10, 70 * i + 20),
                         (710, 70 * i + 20), width=5)


if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Pokemon Yellow')
    size = width, height = 1000, 750
    screen = pygame.display.set_mode(size)
    screen.fill((204, 204, 204))
    background()

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
                    background()
                    screen.blit(image, (pos_x, pos_y))
                if event.key == pygame.K_RIGHT and pos_x < 640:
                    pos_x += 70
                    background()
                    screen.blit(image, (pos_x, pos_y))
                if event.key == pygame.K_UP and pos_y > 20:
                    pos_y -= 70
                    background()
                    screen.blit(image, (pos_x, pos_y))
                if event.key == pygame.K_DOWN and pos_y < 510:
                    pos_y += 70
                    background()
                    screen.blit(image, (pos_x, pos_y))
                if randrange(100) < 15:  # есть покемон или нет
                    fishing("Kanto")
        pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
