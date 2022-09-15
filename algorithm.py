import pygame
from queue import PriorityQueue


# Manhattan Distance Formula // Taxicab // Heuristic
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# The current node starts at the end node, and we will traverse from
# the end node back to the start node.
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()  # PriorityQueue() uses the HeapSort Algorithm
    open_set.put((0, count, start))  # open_set stores the f(n), count, and node.
    came_from = {}  # Keeps track of what nodes came from where.

    # G(n) will keep track of the current shortest distance from
    # the start node to the current node.
    g_score = {spot: float("inf") for row in grid for spot in row}  # Keep
    g_score[start] = 0

    # F(n) keeps track of the predicted distance from the current node to the end.
    # F(n) == Heuristic calc. so that an estimate can be made of how far the start node
    # is from the end node when we begin.
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    # Set is being created to check what is in the queue.
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Indexing at 2 the get the node.
        current = open_set.get()[2]
        open_set_hash.remove(current)

        # Make path.
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            # If a better path has been found, update path and store it.
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())

                # Make current neighbor "closed" so that it is not reconsidered.
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        draw()

        # Node has already been considered.
        if current != start:
            current.make_closed()

    return False
