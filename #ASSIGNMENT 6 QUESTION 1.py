# list of cities (order matters)
cities = [
    "chicago", "detroit", "cleveland", "indianapolis",
    "columbus", "pittsburgh", "buffalo", "syracuse",
    "new york", "philadelphia", "baltimore",
    "providence", "boston"
]

# adjacency matrix
adj_matrix = [

# chi  det  cle  ind  col  pit  buf  syr  ny   phi  bal  pro  bos

[  0, 283, 345, 182,   0,   0,   0,   0,   0,   0,   0,   0,   0],
[283,   0, 169,   0,   0,   0, 256,   0,   0,   0,   0,   0,   0],
[345, 169,   0,   0, 144, 134,   0,   0,   0,   0,   0,   0,   0],
[182,   0,   0,   0, 176,   0,   0,   0,   0,   0,   0,   0,   0],
[  0,   0, 144, 176,   0, 185,   0,   0,   0,   0,   0,   0,   0],
[  0,   0, 134,   0, 185,   0, 215, 253,   0, 305, 247,   0,   0],
[  0, 256,   0,   0,   0, 215,   0, 150,   0,   0,   0,   0,   0],
[  0,   0,   0,   0,   0, 253, 150,   0, 254,   0,   0,   0, 312],
[  0,   0,   0,   0,   0,   0,   0, 254,   0,  97,   0, 181, 215],
[  0,   0,   0,   0,   0, 305,   0,   0,  97,   0, 101,   0,   0],
[  0,   0,   0,   0,   0, 247,   0,   0,   0, 101,   0,   0,   0],
[  0,   0,   0,   0,   0,   0,   0,   0, 181,   0,   0,   0,  50],
[  0,   0,   0,   0,   0,   0,   0, 312, 215,   0,   0,  50,   0]
]

#heuristic values
h = {
    "boston": 0, "providence": 50, "new york": 215,
    "philadelphia": 270, "baltimore": 360,
    "syracuse": 260, "buffalo": 400,
    "pittsburgh": 470, "cleveland": 550,
    "columbus": 640, "detroit": 610,
    "indianapolis": 780, "chicago": 860
}


def befs(start, goal):
    frontier = [(start, 0, [start])]
    visited = []
    explored = 0

    while frontier:

        #smallest h(n)
        min_index = 0
        for i in range(len(frontier)):
            if h[frontier[i][0]] < h[frontier[min_index][0]]:
                min_index = i

        current, cost, path = frontier.pop(min_index)

        if current in visited:
            continue

        visited.append(current)
        explored += 1

        if current == goal:
            return path, cost, explored

        current_index = cities.index(current)

        #check connected cities
        for i in range(len(cities)):
            if adj_matrix[current_index][i] != 0:
                neighbor = cities[i]

                if neighbor not in visited:
                    frontier.append(
                        (neighbor,
                         cost + adj_matrix[current_index][i],
                         path + [neighbor])
                    )

    return None


def astar(start, goal):
    frontier = [(start, 0, [start])]
    visited = []
    explored = 0

    while frontier:

        #smallest f(n) = g(n) + h(n)
        min_index = 0
        for i in range(len(frontier)):
            g1 = frontier[i][1]
            g2 = frontier[min_index][1]

            if g1 + h[frontier[i][0]] < g2 + h[frontier[min_index][0]]:
                min_index = i

        current, cost, path = frontier.pop(min_index)

        if current in visited:
            continue

        visited.append(current)
        explored += 1

        if current == goal:
            return path, cost, explored

        current_index = cities.index(current)

        #check connected cities
        for i in range(len(cities)):
            if adj_matrix[current_index][i] != 0:
                neighbor = cities[i]

                if neighbor not in visited:
                    new_cost = cost + adj_matrix[current_index][i]

                    frontier.append(
                        (neighbor,
                         new_cost,
                         path + [neighbor])
                    )

    return None


print("greedy search")
path, cost, explored = befs("chicago", "boston")
print("path:", path)
print("cost:", cost)
print("explored:", explored)

print("\na star search")
path, cost, explored = astar("chicago", "boston")
print("path:", path)
print("cost:", cost)
print("explored:", explored)