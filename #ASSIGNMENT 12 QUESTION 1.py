graph = {
    "P1": ["P2", "P3", "P6"],
    "P2": ["P1", "P3", "P4"],
    "P3": ["P1", "P2", "P5"],
    "P4": ["P2", "P6"],
    "P5": ["P3", "P6"],
    "P6": ["P1", "P4", "P5"]
}

rooms = ["R1", "R2", "R3"]


def make_domains():
    domains = {}
    for team in graph:
        domains[team] = rooms[:]
    return domains


def revise(domains, xi, xj):
    removed = []
    current_values = domains[xi][:]

    for value in current_values:
        supported = False
        for other in domains[xj]:
            if value != other:
                supported = True
                break
        if not supported:
            domains[xi].remove(value)
            removed.append(value)

    return len(removed) > 0, removed


def ac3(domains):
    queue = []
    for xi in graph:
        for xj in graph[xi]:
            queue.append((xi, xj))

    trace = []

    while queue:
        xi, xj = queue.pop(0)
        changed, removed = revise(domains, xi, xj)

        if len(trace) < 5:
            if removed:
                trace.append("Arc (" + xi + ", " + xj + ") checked, removed " + ", ".join(removed) + " from " + xi)
            else:
                trace.append("Arc (" + xi + ", " + xj + ") checked, no change")

        if len(domains[xi]) == 0:
            return False, trace, domains

        if changed:
            for xk in graph[xi]:
                if xk != xj:
                    queue.append((xk, xi))

    return True, trace, domains


def is_arc_consistent(domains):
    for xi in graph:
        for xj in graph[xi]:
            for value in domains[xi]:
                found = False
                for other in domains[xj]:
                    if value != other:
                        found = True
                        break
                if not found:
                    return False
    return True


def show_domains(domains):
    for team in domains:
        print(team, ":", "{" + ", ".join(domains[team]) + "}")


def is_safe(team, room, assignment):
    for neighbor in graph[team]:
        if neighbor in assignment and assignment[neighbor] == room:
            return False
    return True


def solve(order, domains, assignment, index):
    if index == len(order):
        return True

    team = order[index]

    for room in domains[team]:
        if is_safe(team, room, assignment):
            assignment[team] = room
            if solve(order, domains, assignment, index + 1):
                return True
            assignment.pop(team)

    return False


def main():
    initial_domains = make_domains()
    ok1, trace1, final1 = ac3(initial_domains)

    print("Initial domains")
    show_domains(make_domains())
    print()

    print("First 5 arc checks")
    for step in trace1:
        print(step)
    print()

    print("Domains after AC-3")
    show_domains(final1)
    print()

    if ok1 and is_arc_consistent(final1):
        print("The problem is arc-consistent.")
    else:
        print("The problem is not arc-consistent.")
    print()

    assigned_domains = make_domains()
    assigned_domains["P1"] = ["R1"]
    ok2, trace2, final2 = ac3(assigned_domains)

    print("After assigning P1 to R1")
    print("First 5 arc checks")
    for step in trace2:
        print(step)
    print()

    print("Domains after AC-3")
    show_domains(final2)
    print()

    if not ok2:
        print("AC-3 detects failure after assigning P1 to R1.")
    else:
        print("AC-3 does not detect failure after assigning P1 to R1.")
        print("A valid set of domains remains for the remaining teams.")
        print()

        order = sorted(graph, key=lambda team: len(final2[team]))
        assignment = {}
        if solve(order, final2, assignment, 0):
            print("One valid room assignment is")
            for team in graph:
                print(team, "->", assignment[team])


if __name__ == "__main__":
    main()