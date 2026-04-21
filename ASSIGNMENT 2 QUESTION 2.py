import collections

class SearchAlgorithmAnalyzer:
    def __init__(self):
        self.graph = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F'],
            'D': [],
            'E': ['G'],
            'F': [],
            'G': []
        }
    
    def run_dfs(self, start_node, goal_node):
        print(f"\n--- Running DFS from '{start_node}' to find '{goal_node}' ---")
        
        stack = [(start_node, 0)]  
        visited = set()
        states_explored = 0
        
        while stack:
            current_node, depth = stack.pop()
            
            if current_node in visited:
                continue
            
            states_explored += 1
            visited.add(current_node)
            print(f"  Exploring: {current_node} (Depth: {depth})")
            
            if current_node == goal_node:
                print(f"  >> Goal '{goal_node}' found!")
                return {
                    "algorithm": "DFS",
                    "states_explored": states_explored,
                    "cost": depth,
                    "status": "Found"
                }
            
            neighbors = self.graph.get(current_node, [])
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.append((neighbor, depth + 1))
                    
        return {"algorithm": "DFS", "status": "Not Found"}

    def run_bfs(self, start_node, goal_node):
        print(f"\n--- Running BFS from '{start_node}' to find '{goal_node}' ---")
        
        queue = collections.deque([(start_node, 0)])
        visited = set()
        visited.add(start_node)
        states_explored = 0
        
        while queue:
            current_node, depth = queue.popleft()
            states_explored += 1
            
            print(f"  Exploring: {current_node} (Depth: {depth})")
            
            if current_node == goal_node:
                print(f"  >> Goal '{goal_node}' found!")
                return {
                    "algorithm": "BFS",
                    "states_explored": states_explored,
                    "cost": depth,
                    "status": "Found"
                }
            
            neighbors = self.graph.get(current_node, [])
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, depth + 1))
                    
        return {"algorithm": "BFS", "status": "Not Found"}

analyzer = SearchAlgorithmAnalyzer()

start = 'A'
goal = 'G'

dfs_result = analyzer.run_dfs(start, goal)
bfs_result = analyzer.run_bfs(start, goal)

print("\n" + "="*40)
print("       FINAL COMPARISON RESULTS       ")
print("="*40)
print(f"{'Metric':<20} | {'DFS':<10} | {'BFS':<10}")
print("-" * 46)
print(f"{'States Explored':<20} | {dfs_result['states_explored']:<10} | {bfs_result['states_explored']:<10}")
print(f"{'Cost (Depth)':<20} | {dfs_result['cost']:<10} | {bfs_result['cost']:<10}")
print("="*40)

print("\n[Comparison Explanation]")
if bfs_result['cost'] < dfs_result['cost']:
    print(f"BFS found a path with LOWER cost ({bfs_result['cost']}) than DFS ({dfs_result['cost']}).")
    print("This demonstrates that BFS is 'Optimal' for unweighted graphs—it always finds the shallowest goal.")
elif bfs_result['cost'] == dfs_result['cost']:
    print("Both algorithms found the goal at the same depth.")
else:
    print("DFS happened to find a path, but BFS guarantees the shortest path in terms of depth.")

print(f"BFS explored {bfs_result['states_explored']} states vs DFS's {dfs_result['states_explored']} states.")