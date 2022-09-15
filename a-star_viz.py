import pygame
from algorithm import algorithm
from drawing import make_grid, draw, get_clicked_pos

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finder")


def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)

    start = end = None
    run = True

    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:  # LEFT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                grid_square = grid[row][col]
                if not start and grid_square != end:
                    start = grid_square
                    start.make_start()

                elif not end and grid_square != start:
                    end = grid_square
                    end.make_end()

                elif grid_square != end and grid_square != start:
                    grid_square.make_barrier()

            elif pygame.mouse.get_pressed()[2]:  # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                grid_square = grid[row][col]
                grid_square.reset()
                if grid_square == start:
                    start = None
                elif grid_square == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for grid_square in row:
                            grid_square.update_neighbors(grid)

                    # Using lambda to pass draw function as an argument to another function
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)


if __name__ == "__main__":
    main(WIN, WIDTH)
