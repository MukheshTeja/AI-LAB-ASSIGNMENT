from collections import deque
import time

# --- Helper Functions ---

def print_board(board):
    """Prints the 3x3 board in a readable format."""
    for row in board:
        print(" | ".join(str(x) if x != 0 else "_" for x in row))
    print("-" * 9)

def find_blank(board):
    """Finds the position (row, col) of the blank space (represented by 0)."""
    for r in range(3):
        for c in range(3):
            if board[r][c] == 0:
                return r, c
    return None

def get_neighbors(state):
    """
    Generates all possible next states from the current state.
    Returns a list of valid board configurations.
    """
    neighbors = []
    blank_r, blank_c = find_blank(state)
    
    # Possible moves: Up, Down, Left, Right
    # (row_change, col_change)
    moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] 

    for dr, dc in moves:
        new_r, new_c = blank_r + dr, blank_c + dc

        # Check if the new position is inside the 3x3 grid
        if 0 <= new_r < 3 and 0 <= new_c < 3:
            # Create a copy of the board to modify
            # (We convert to list of lists to be mutable)
            new_board = [list(row) for row in state]
            
            # Swap the blank space with the target tile
            new_board[blank_r][blank_c], new_board[new_r][new_c] = \
            new_board[new_r][new_c], new_board[blank_r][blank_c]
            
            # Convert back to tuple of tuples so it can be stored in a set
            neighbors.append(tuple(tuple(row) for row in new_board))
            
    return neighbors

def bfs_solver(start_state, goal_state):
    """
    Solves the 8-puzzle using Breadth-First Search (BFS).
    Returns the number of states explored and the depth (moves) of the solution.
    """
    # Queue stores: (current_board_state, depth_level)
    queue = deque([(start_state, 0)])
    
    # Visited set stores states we have already seen to avoid loops
    # Using a set is crucial for performance!
    visited = set()
    visited.add(start_state)
    
    states_explored_count = 0
    
    print("BFS Algorithm Started...")
    print("Searching for the goal (this might take a few seconds)...")
    
    start_time = time.time()

    while queue:
        current_state, depth = queue.popleft()
        states_explored_count += 1
        
        # Check if we have reached the goal
        if current_state == goal_state:
            end_time = time.time()
            print(f"\nSUCCESS! Goal found.")
            print(f"Time taken: {end_time - start_time:.4f} seconds")
            return states_explored_count, depth

        # Get all valid next moves
        next_states = get_neighbors(current_state)
        
        for state in next_states:
            if state not in visited:
                visited.add(state)
                queue.append((state, depth + 1))
                
    return -1, -1 # Should not happen if a solution exists

# --- Main Execution Block ---

if __name__ == "__main__":
    # 0 represents the empty/blank space
    
    # Start State from your image
    # 7 2 4
    # 5 0 6
    # 8 3 1
    start_matrix = (
        (7, 2, 4),
        (5, 0, 6),
        (8, 3, 1)
    )

    # Goal State from your image
    # 0 1 2
    # 3 4 5
    # 6 7 8
    goal_matrix = (
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8)
    )

    print("--- Start State ---")
    print_board(start_matrix)
    print("\n--- Goal State ---")
    print_board(goal_matrix)
    print("\n-------------------")

    explored, moves = bfs_solver(start_matrix, goal_matrix)

    print("\n--- Final Results ---")
    print(f"Total States Explored (Nodes visited): {explored}")
    print(f"Minimum Moves Required (Depth): {moves}")