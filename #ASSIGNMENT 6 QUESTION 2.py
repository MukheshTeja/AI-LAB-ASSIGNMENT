grid = [
    [2,0,0,0,1],
    [0,1,0,0,3],
    [0,3,0,1,1],
    [0,1,0,0,1],
    [3,0,0,0,3]
]

ROWS = len(grid)
COLS = len(grid[0])

#find start and rewards
rewards = []
for r in range(ROWS):
    for c in range(COLS):
        if grid[r][c] == 2:
            start = (r,c)
        if grid[r][c] == 3:
            rewards.append((r,c))

#manhattan heuristic
def heuristic(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

#valid neighbors
def neighbors(node):
    r,c = node
    moves = [(-1,0),(1,0),(0,-1),(0,1)]
    result = []
    for dr,dc in moves:
        nr,nc = r+dr, c+dc
        if 0<=nr<ROWS and 0<=nc<COLS and grid[nr][nc] != 1:
            result.append((nr,nc))
    return result

# remove lowest f(n)
def pop_lowest(frontier, f_cost):
    lowest_index = 0
    for i in range(1,len(frontier)):
        if f_cost[frontier[i]] < f_cost[frontier[lowest_index]]:
            lowest_index = i
    return frontier.pop(lowest_index)


def astar(start, goal):

    frontier = [start]
    came_from = {}
    g_cost = {start:0}
    f_cost = {start:heuristic(start,goal)}
    visited_tiles = []

    while frontier:

        current = pop_lowest(frontier, f_cost)
        visited_tiles.append(current)

        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1], visited_tiles

        for nb in neighbors(current):

            temp_g = g_cost[current] + 1

            if nb not in g_cost or temp_g < g_cost[nb]:
                came_from[nb] = current
                g_cost[nb] = temp_g
                f_cost[nb] = temp_g + heuristic(nb,goal)

                if nb not in frontier:
                    frontier.append(nb)

    return None, visited_tiles


#collect all rewards
current_position = start
total_path = []
all_visited = []

while rewards:

    #choose nearest reward
    nearest = rewards[0]
    min_dist = heuristic(current_position, nearest)

    for r in rewards:
        d = heuristic(current_position, r)
        if d < min_dist:
            min_dist = d
            nearest = r

    path, visited = astar(current_position, nearest)

    if path is None:
        print("No solution")
        break

    total_path += path[1:]
    all_visited += visited

    current_position = nearest
    rewards.remove(nearest)

print("Final Path:", total_path)
print("Visited Tiles:", all_visited)
print("Total Cost:", len(total_path))