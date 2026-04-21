import random
import math

def heuristic(board):
    conflicts = 0
    n = len(board)
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                conflicts += 1
    return conflicts

def generate_random_board(n=8):
    return [random.randint(0, n - 1) for _ in range(n)]

def get_neighbors(board):
    neighbors = []
    n = len(board)
    for col in range(n):
        for row in range(n):
            if board[col] != row:
                new_board = list(board)
                new_board[col] = row
                neighbors.append(new_board)
    return neighbors

def first_choice_hill_climbing(board):
    current = list(board)
    current_h = heuristic(current)
    steps = 0
    n = len(current)

    while True:
        found = False
        attempts = 0
        max_attempts = n * (n - 1)

        while attempts < max_attempts:
            col = random.randint(0, n - 1)
            row = random.randint(0, n - 1)
            if row == current[col]:
                attempts += 1
                continue
            neighbor = list(current)
            neighbor[col] = row
            h = heuristic(neighbor)
            attempts += 1
            if h < current_h:
                steps += 1
                current = neighbor
                current_h = h
                found = True
                break

        if not found:
            break
        if current_h == 0:
            break

    return current, current_h, steps

def random_restart_hill_climbing(max_restarts=100):
    total_steps = 0
    restart_count = 0

    while restart_count <= max_restarts:
        board = generate_random_board()
        current = list(board)
        current_h = heuristic(current)
        steps = 0

        while True:
            neighbors = get_neighbors(current)
            best_neighbor = None
            best_h = current_h

            for neighbor in neighbors:
                h = heuristic(neighbor)
                if h < best_h:
                    best_h = h
                    best_neighbor = neighbor

            if best_neighbor is None:
                break

            steps += 1
            current = best_neighbor
            current_h = best_h

            if current_h == 0:
                break

        total_steps += steps

        if current_h == 0:
            return current, current_h, total_steps, restart_count

        restart_count += 1

    return current, current_h, total_steps, restart_count

def simulated_annealing(board, initial_temp=4.0, cooling_rate=0.995, min_temp=0.0001):
    current = list(board)
    current_h = heuristic(current)
    temperature = initial_temp
    steps = 0
    n = len(current)

    while temperature > min_temp:
        col = random.randint(0, n - 1)
        row = random.randint(0, n - 1)
        while row == current[col]:
            row = random.randint(0, n - 1)

        neighbor = list(current)
        neighbor[col] = row
        neighbor_h = heuristic(neighbor)
        delta = neighbor_h - current_h

        if delta < 0:
            accept = True
        else:
            probability = math.exp(-delta / temperature)
            accept = random.random() < probability

        steps += 1

        if accept:
            current = neighbor
            current_h = neighbor_h

        temperature *= cooling_rate

        if current_h == 0:
            break

    return current, current_h, steps


fc_results = []
fc_solved = 0

rr_results = []
rr_solved = 0

sa_results = []
sa_solved = 0

for trial in range(1, 51):
    board = generate_random_board()
    initial_h = heuristic(board)

    final_board, final_h, num_steps = first_choice_hill_climbing(board)
    status = "Solved" if final_h == 0 else "Failed"
    if final_h == 0:
        fc_solved += 1
    fc_results.append((trial, initial_h, final_h, num_steps, status))

    final_board, final_h, total_steps, restarts = random_restart_hill_climbing()
    status = "Solved" if final_h == 0 else "Failed"
    if final_h == 0:
        rr_solved += 1
    rr_results.append((trial, final_h, total_steps, restarts, status))

    board = generate_random_board()
    initial_h = heuristic(board)
    final_board, final_h, num_steps = simulated_annealing(board)
    status = "Solved" if final_h == 0 else "Failed"
    if final_h == 0:
        sa_solved += 1
    sa_results.append((trial, initial_h, final_h, num_steps, status))


print("First Choice Hill Climbing")
print(f"{'Trial':<8} {'Initial H':<12} {'Final H':<10} {'Steps':<8} {'Status'}")
print("-" * 50)
for trial, init_h, fin_h, steps, status in fc_results:
    print(f"{trial:<8} {init_h:<12} {fin_h:<10} {steps:<8} {status}")
fc_avg_steps = sum(r[3] for r in fc_results) / 50
print(f"\nSolved: {fc_solved}/50  |  Success Rate: {(fc_solved/50)*100:.1f}%  |  Avg Steps: {fc_avg_steps:.1f}")


print("\nRandom Restart Hill Climbing")
print(f"{'Trial':<8} {'Final H':<10} {'Total Steps':<14} {'Restarts':<10} {'Status'}")
print("-" * 50)
for trial, fin_h, steps, restarts, status in rr_results:
    print(f"{trial:<8} {fin_h:<10} {steps:<14} {restarts:<10} {status}")
rr_avg_steps = sum(r[2] for r in rr_results) / 50
rr_avg_restarts = sum(r[3] for r in rr_results) / 50
print(f"\nSolved: {rr_solved}/50  |  Success Rate: {(rr_solved/50)*100:.1f}%  |  Avg Steps: {rr_avg_steps:.1f}  |  Avg Restarts: {rr_avg_restarts:.1f}")


print("\nSimulated Annealing")
print(f"{'Trial':<8} {'Initial H':<12} {'Final H':<10} {'Steps':<8} {'Status'}")
print("-" * 50)
for trial, init_h, fin_h, steps, status in sa_results:
    print(f"{trial:<8} {init_h:<12} {fin_h:<10} {steps:<8} {status}")
sa_avg_steps = sum(r[3] for r in sa_results) / 50
print(f"\nSolved: {sa_solved}/50  |  Success Rate: {(sa_solved/50)*100:.1f}%  |  Avg Steps: {sa_avg_steps:.1f}")


print("\nComparison Summary")
print(f"{'Algorithm':<25} {'Solved':<10} {'Success %':<12} {'Avg Steps'}")
print("-" * 55)
print(f"{'First Choice HC':<25} {fc_solved:<10} {(fc_solved/50)*100:<12.1f} {fc_avg_steps:.1f}")
print(f"{'Random Restart HC':<25} {rr_solved:<10} {(rr_solved/50)*100:<12.1f} {rr_avg_steps:.1f}")
print(f"{'Simulated Annealing':<25} {sa_solved:<10} {(sa_solved/50)*100:<12.1f} {sa_avg_steps:.1f}")