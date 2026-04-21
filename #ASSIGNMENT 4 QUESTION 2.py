grid = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]

rows = 10
cols = 20

START = (8, 4)
GOAL = (4, 18)

class Node:
    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost

class PriorityQueue:
    def __init__(self, f):
        self.data = []
        self.f = f

    def add(self, node):
        self.data.append(node)
        self.data.sort(key=self.f)

    def pop(self):
        return self.data.pop(0)

    def top(self):
        return self.data[0]

    def is_empty(self):
        return len(self.data) == 0

class Problem:
    def __init__(self, initial, goal, grid):
        self.initial = initial
        self.goal = goal
        self.grid = grid

    def is_goal(self, state):
        return state == self.goal

    def ACTIONS(self, state):
        r, c = state
        actions = []
        moves = [
            ("Down",  (1, 0)),
            ("Up",    (-1, 0)),
            ("Right", (0, 1)),
            ("Left",  (0, -1))
        ]
        
        for name, (dr, dc) in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if self.grid[nr][nc] == 0:
                    actions.append(name)
        return actions

    def RESULT(self, state, action):
        r, c = state
        if action == "Down":  return (r + 1, c)
        if action == "Up":    return (r - 1, c)
        if action == "Right": return (r, c + 1)
        if action == "Left":  return (r, c - 1)
        return state

    def ACTION_COST(self, s, action, s_prime):
        return 1

def heuristic(node):
    r1, c1 = node.state
    r2, c2 = GOAL
    return abs(r1 - r2) + abs(c1 - c2)

def f(node):
    return heuristic(node)

def EXPAND(problem, node):
    s = node.state
    for action in problem.ACTIONS(s):
        s_prime = problem.RESULT(s, action)
        cost = node.path_cost + problem.ACTION_COST(s, action, s_prime)
        yield Node(state=s_prime, parent=node, action=action, path_cost=cost)

def BEST_FIRST_SEARCH(problem, f):
    node = Node(problem.initial)
    frontier = PriorityQueue(f)
    frontier.add(node)
    
    reached = [[None for _ in range(cols)] for _ in range(rows)]
    reached[node.state[0]][node.state[1]] = node
    
    explored = 0
    
    while not frontier.is_empty():
        node = frontier.pop()
        explored += 1
        
        if problem.is_goal(node.state):
            return node, explored
        
        for child in EXPAND(problem, node):
            r, c = child.state
            if reached[r][c] is None or child.path_cost < reached[r][c].path_cost:
                reached[r][c] = child
                frontier.add(child)
                
    return None, explored

def get_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]

def print_grid_with_path(grid, path):
    print("\nEvaluated Path on Grid:")
    path_set = set(path)
    
    print("   ", end="")
    for c in range(cols): print(f"{c%10}", end=" ")
    print()
    
    for r in range(rows):
        print(f"{r:<2} ", end="")
        for c in range(cols):
            if (r, c) == START:
                print("S", end=" ")
            elif (r, c) == GOAL:
                print("E", end=" ")
            elif (r, c) in path_set:
                print(".", end=" ")
            elif grid[r][c] == 1:
                print("#", end=" ")
            else:
                print(" ", end=" ")
        print()

if __name__ == "__main__":
    problem = Problem(START, GOAL, grid)
    
    print("Starting Best First Search (Greedy)...")
    print(f"Start: {START}, Goal: {GOAL}")
    
    solution, explored = BEST_FIRST_SEARCH(problem, f)
    
    if solution:
        path = get_path(solution)
        print("\nGoal Found!")
        print(f"Path Length: {len(path)}")
        print(f"Total Cost: {solution.path_cost}")
        print(f"Nodes Explored: {explored}")
        
        print_grid_with_path(grid, path)
        
        print("\nPath Steps:")
        curr = solution
        steps = []
        while curr.parent:
            steps.append(f"{curr.action} -> {curr.state}")
            curr = curr.parent
        for s in reversed(steps):
            print(s)
            
        print("\nEvaluation Cost Function Justification:")
        print("Function: Manhattan Distance f(n) = |x1 - x2| + |y1 - y2|")
        print("Reason: Since robots move in 4 cardinal directions,")
        print("Manhattan distance perfectly estimates the minimum number of steps to reach the goal")
        print("ignoring obstacles. It is simpler to calculate than Euclidean distance and")
        print("more accurate for grid-based movement.")
        
    else:
        print("No path found!")