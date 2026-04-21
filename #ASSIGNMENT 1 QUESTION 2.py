#ASSIGNMENT 1 QUESTION 2
from collections import deque

graph = {
    "Raj": ["Priya", "Akash"],
    "Priya": ["Raj", "Aarav", "Neha1"],
    "Akash": ["Raj", "Sunil"],
    "Sunil": ["Akash", "Sneha"],
    "Sneha": ["Sunil", "Rahul"],
    "Rahul": ["Sneha", "Neha1", "Pooja", "Maya"],
    "Neha1": ["Priya", "Rahul", "Aarav"],
    "Aarav": ["Priya", "Neha2"],
    "Neha2": ["Aarav", "Arjun"],
    "Arjun": ["Neha2", "Pooja"],
    "Pooja": ["Arjun", "Rahul"],
    "Maya": ["Rahul"]
}

# BFS
def bfs(start):
    visited = set()
    q = deque([start])
    print("BFS order:")

    while q:
        node = q.popleft()
        if node not in visited:
            print(node, end=" ")
            visited.add(node)
            for nbr in graph[node]:
                if nbr not in visited:
                    q.append(nbr)
    print()

# DFS
def dfs(node, visited):
    print(node, end=" ")
    visited.add(node)
    for nbr in graph[node]:
        if nbr not in visited:
            dfs(nbr, visited)

# Run
start = "Raj"
bfs(start)

print("DFS order:")
dfs(start, set())
print("\n")
