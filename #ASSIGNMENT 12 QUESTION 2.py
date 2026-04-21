puzzle = (
    "000006000"
    "059000008"
    "200008000"
    "045000000"
    "003000000"
    "006003050"
    "000007000"
    "000000000"
    "000050002"
)


def build_peers():
    peers = {}

    for row in range(9):
        for col in range(9):
            cell = row * 9 + col
            peer_set = set()

            for c in range(9):
                if c != col:
                    peer_set.add(row * 9 + c)

            for r in range(9):
                if r != row:
                    peer_set.add(r * 9 + col)

            start_row = (row // 3) * 3
            start_col = (col // 3) * 3
            for r in range(start_row, start_row + 3):
                for c in range(start_col, start_col + 3):
                    other = r * 9 + c
                    if other != cell:
                        peer_set.add(other)

            peers[cell] = sorted(peer_set)

    return peers


def build_domains():
    domains = {}

    for i in range(81):
        value = puzzle[i]
        if value == "0":
            domains[i] = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
        else:
            domains[i] = [value]

    return domains


def build_arcs(peers):
    arcs = []
    for cell in peers:
        for peer in peers[cell]:
            arcs.append((cell, peer))
    return arcs


def count_unique_constraints(peers):
    pairs = set()
    for cell in peers:
        for peer in peers[cell]:
            if cell < peer:
                pairs.add((cell, peer))
    return len(pairs)


def revise(domains, xi, xj):
    removed = 0
    new_domain = []

    for val in domains[xi]:
        supported = False
        for other in domains[xj]:
            if val != other:
                supported = True
                break
        if supported:
            new_domain.append(val)
        else:
            removed += 1

    domains[xi] = new_domain
    return removed


def ac3(domains, peers):
    queue = build_arcs(peers)
    total_removed = 0

    while queue:
        xi, xj = queue.pop(0)
        removed = revise(domains, xi, xj)

        if removed > 0:
            total_removed += removed

            if len(domains[xi]) == 0:
                return False, total_removed

            for xk in peers[xi]:
                if xk != xj:
                    queue.append((xk, xi))

    return True, total_removed


def print_domain_sizes(domains):
    for row in range(9):
        values = []
        for col in range(9):
            cell = row * 9 + col
            values.append(str(len(domains[cell])))
        print(" ".join(values))


def main():
    peers = build_peers()
    domains = build_domains()
    arcs = build_arcs(peers)

    success, total_removed = ac3(domains, peers)

    print("Sudoku AC-3")
    print("Directed arcs generated:", len(arcs))
    print("Unique binary constraints:", count_unique_constraints(peers))
    print("Values removed by AC-3:", total_removed)
    print()
    print("Remaining domain size grid")
    print_domain_sizes(domains)
    print()

    empty_found = False
    solved_all = True

    for cell in domains:
        size = len(domains[cell])
        if size == 0:
            empty_found = True
        if size != 1:
            solved_all = False

    if not success or empty_found:
        print("AC-3 reduced at least one domain to 0.")
        print("The puzzle would be inconsistent with these constraints.")
    elif solved_all:
        print("AC-3 reduced all domains to 1.")
        print("The puzzle is solved completely.")
    else:
        print("AC-3 did not reduce any domain to 0.")
        print("AC-3 also did not solve the puzzle completely.")


if __name__ == "__main__":
    main()