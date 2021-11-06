import pygame
from copy import deepcopy
from random import choice, randrange

tiles_x, tiles_y = 10, 20
size = 50
resolution = tiles_x * size, tiles_y * size
fps = 60

pygame.init()

window = pygame.display.set_mode(resolution)
clock = pygame.time.Clock()

grid = [pygame.Rect(x * size, y * size, size, size) for x in range(tiles_x) for y in range(tiles_y)]

figures_position = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                    [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                    [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                    [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                    [(0, 0), (0, -1), (0, 1), (-1, -1)],
                    [(0, 0), (0, -1), (0, 1), (1, -1)],
                    [(0, 0), (0, -1), (0, 1), (-1, 0)]]

figures = [[pygame.Rect(x + tiles_x // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_position]
figure_rect = pygame.Rect(0, 0, size - 2, size - 2)
field = [[0 for i in range(tiles_x)] for j in range(tiles_y)]

anim_count, anim_speed, anim_limit = 0, 60, 2000

get_color = lambda: [randrange(30, 256), randrange(30, 256), randrange(30, 256)]

figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
color, next_color = get_color(), get_color()

lines = 0

# game over font
font_game_over = pygame.font.SysFont("Arial", 60, bold=True)


def check_borders():
    if figure[i].x < 0 or figure[i].x > tiles_x - 1:
        return False
    elif figure[i].y > tiles_y - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True


run = True

while run:
    dx, rotate = 0, False
    window.fill((0, 0, 0))

    # delay for full lines
    for i in range(lines):
        pygame.time.wait(200)
    # control
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 100
            elif event.key == pygame.K_UP:
                rotate = True
    # move x
    figure_old = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
    # move y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for i in range(4):
                    field[figure_old[i].y][figure_old[i].x] = color
                figure, color = next_figure, next_color
                next_figure, next_color = deepcopy(choice(figures)), get_color()
                anim_limit = 2000
                break
    # rotate
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate:
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break
    # check lines
    line, lines = tiles_y - 1, 0
    for row in range(tiles_y - 1, -1, -1):
        count = 0
        for i in range(tiles_x):
            if field[row][i]:
                count += 1
            field[line][i] = field[row][i]
        if count < tiles_x:
            line -= 1
        else:
            anim_speed += 3
            lines += 1

    # draw grid
    [pygame.draw.rect(window, (40, 40, 40), i_rect, 1) for i_rect in grid]
    # draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * size
        figure_rect.y = figure[i].y * size
        pygame.draw.rect(window, color, figure_rect)
    # draw field
    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * size, y * size
                pygame.draw.rect(window, col, figure_rect)

    # game over
    for i in range(tiles_x):
        if field[0][i]:
            field = [[0 for i in range(tiles_x)] for i in range(tiles_y)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000

            while run:
                render_end = font_game_over.render("GAME OVER", 1, (255, 255, 255))
                window.blit(render_end, (resolution[0] // 2 - 150, resolution[1] // 3))
                pygame.display.flip()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False

    pygame.display.flip()
    clock.tick(fps)
