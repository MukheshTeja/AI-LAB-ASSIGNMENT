cities = [
    "Syracuse", "Buffalo", "Pittsburgh", "Cleveland", "Columbus",
    "Detroit", "Chicago", "Indianapolis", "Boston", "New York",
    "Philadelphia", "Providence", "Baltimore", "Portland"
]

INF = 9999
n = 14
adj_matrix = [[INF] * n for _ in range(n)]


def connect(city1, city2, miles):
    idx1 = cities.index(city1)
    idx2 = cities.index(city2)
    adj_matrix[idx1][idx2] = miles
    adj_matrix[idx2][idx1] = miles

connect("Syracuse", "Buffalo", 150)
connect("Syracuse", "Boston", 312)
connect("Syracuse", "New York", 254)
connect("Syracuse", "Philadelphia", 253)
connect("Buffalo", "Detroit", 256)
connect("Buffalo", "Cleveland", 189)
connect("Buffalo", "Pittsburgh", 215)
connect("Boston", "New York", 215)
connect("Boston", "Providence", 50)
connect("Boston", "Portland", 107)
connect("New York", "Philadelphia", 97)
connect("New York", "Providence", 181)
connect("Philadelphia", "Baltimore", 101)
connect("Philadelphia", "Pittsburgh", 305)
connect("Baltimore", "Pittsburgh", 247)
connect("Pittsburgh", "Cleveland", 134)
connect("Pittsburgh", "Columbus", 185)
connect("Cleveland", "Detroit", 169)
connect("Cleveland", "Columbus", 144)
connect("Cleveland", "Chicago", 345) 
connect("Detroit", "Chicago", 283)
connect("Columbus", "Indianapolis", 176)
connect("Indianapolis", "Chicago", 182)


class Node:
    def __init__(self, state_index, parent, path_cost):
        self.STATE = state_index
        self.PARENT = parent
        self.PATH_COST = path_cost

def EXPAND(node_u):
    child_nodes = []
    u_index = node_u.STATE
    
   
    for v_index in range(n):
        distance = adj_matrix[u_index][v_index]
        
        
        if distance != INF:
        
            new_cost = node_u.PATH_COST + distance
            child = Node(v_index, node_u, new_cost)
            child_nodes.append(child)
            
    return child_nodes

def BEST_FIRST_SEARCH(start_city_name, goal_city_name):
    start_index = cities.index(start_city_name)
    goal_index = cities.index(goal_city_name)

    
    start_node = Node(start_index, None, 0)

    frontier = [start_node]

    reached = {start_index: start_node}

    nodes_explored = 0

    print(f"Searching path from {start_city_name} to {goal_city_name}...")

    while len(frontier) > 0:

        frontier.sort(key=lambda x: x.PATH_COST)

        node = frontier.pop(0)
        nodes_explored += 1
        
        current_city = cities[node.STATE]

        if node.STATE == goal_index:
            return node, nodes_explored


        for child in EXPAND(node):
            s = child.STATE

            if (s not in reached) or (child.PATH_COST < reached[s].PATH_COST):
                

                reached[s] = child

                frontier.append(child)

    return None, nodes_explored


solution_node, count = BEST_FIRST_SEARCH("Syracuse", "Chicago")

print("-" * 30)
if solution_node:
    path = []
    current = solution_node
    while current is not None:
        path.append(cities[current.STATE])
        current = current.PARENT
    path.reverse()
    
    print("Success!")
    print("Path taken:", " -> ".join(path))
    print("Total Miles:", solution_node.PATH_COST)
    print("Total nodes explored (popped):", count)
else:   
    print("Failure: No path found.")