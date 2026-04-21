import random

# ── Distance matrix (8 cities: A‑H) ─────────────────────────────
DIST = [
    [0,  10, 15, 20, 25, 30, 35, 40],   # A
    [12,  0, 35, 15, 20, 25, 30, 45],   # B
    [25, 30,  0, 10, 40, 20, 15, 35],   # C
    [18, 25, 12,  0, 15, 30, 20, 10],   # D
    [22, 18, 28, 20,  0, 15, 25, 30],   # E
    [35, 22, 18, 28, 12,  0, 40, 20],   # F
    [30, 35, 22, 18, 28, 32,  0, 15],   # G
    [40, 28, 35, 22, 18, 25, 12,  0],   # H
]
CITIES = list(range(len(DIST)))
CITY_NAMES = "ABCDEFGH"


def tour_cost(tour):
    """Total round-trip cost for a given tour (list of city indices)."""
    cost = sum(DIST[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))
    cost += DIST[tour[-1]][tour[0]]       # return to start
    return cost


def random_tour():
    """Generate a random permutation of all cities."""
    t = list(CITIES)
    random.shuffle(t)
    return t


def get_neighbours(tour):
    """Generate neighbours by swapping every pair of cities."""
    neighbours = []
    n = len(tour)
    for i in range(n):
        for j in range(i + 1, n):
            nb = list(tour)
            nb[i], nb[j] = nb[j], nb[i]
            neighbours.append(nb)
    return neighbours


# ── Local Beam Search ────────────────────────────────────────────
def local_beam_search(k, max_iter=500, seed=42):
    """
    Local beam search for TSP.
    k       : beam width (number of states kept at each step)
    Returns : (best_tour, best_cost, history_of_best_cost_per_iter, iterations)
    """
    random.seed(seed)

    # 1. Start with k random tours
    beams = [random_tour() for _ in range(k)]
    best_tour = min(beams, key=tour_cost)
    best_cost = tour_cost(best_tour)
    history = [best_cost]

    for it in range(1, max_iter + 1):
        # 2. Generate ALL neighbours of all k states
        all_neighbours = []
        for tour in beams:
            all_neighbours.extend(get_neighbours(tour))

        # 3. Pick the k best neighbours
        all_neighbours.sort(key=tour_cost)
        beams = all_neighbours[:k]

        # Track the best so far
        current_best = beams[0]
        current_cost = tour_cost(current_best)
        if current_cost < best_cost:
            best_cost = current_cost
            best_tour = list(current_best)

        history.append(best_cost)

        # 4. Convergence check — stop if no improvement for 20 steps
        if len(history) > 20 and history[-1] == history[-21]:
            break

    return best_tour, best_cost, history, it


def format_tour(tour):
    return " -> ".join(CITY_NAMES[c] for c in tour) + " -> " + CITY_NAMES[tour[0]]


# ── Run & Compare k = 3, 5, 10 ──────────────────────────────────
if __name__ == "__main__":
    print("TSP — Local Beam Search (8 cities A-H)\n")
    print(f"{'k':>4} | {'Cost':>6} | {'Iters':>5} | Best Tour")
    print("-" * 55)

    results = {}
    for k in [3, 5, 10]:
        tour, cost, history, iters = local_beam_search(k)
        results[k] = (tour, cost, history, iters)
        print(f"{k:>4} | {cost:>6} | {iters:>5} | {format_tour(tour)}")

    print(f"\nDoes convergence depend on k?")
    costs = {k: results[k][1] for k in results}
    if costs[3] == costs[5] == costs[10]:
        print("All beam widths converged to the same cost — for this small")
        print("problem even k=3 suffices. Larger k helps on bigger instances.")
    else:
        print("Yes — wider beams find better solutions by exploring more")
        print("neighbours per iteration, avoiding local minima.")