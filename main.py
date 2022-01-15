import pygame

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Pokemon Yellow')
    size = width, height = 1000, 750
    screen = pygame.display.set_mode(size)

    screen.fill((204, 204, 204))
    screen.fill((255, 204, 0), pygame.Rect(10, 20, 700, 560))

    # вертикальные линии
    for i in range(0, 11):
        pygame.draw.line(screen, (255, 0, 0), (70 * i + 10, 20),
                         (70 * i + 10, 580), width=5)

    # горизонтальные линии
    for i in range(0, 9):
        pygame.draw.line(screen, (255, 0, 0), (10, 70 * i + 20),
                         (710, 70 * i + 20), width=5)

    pygame.display.flip()
    while pygame.event.wait().type != pygame.QUIT:
        pass
    pygame.quit()
