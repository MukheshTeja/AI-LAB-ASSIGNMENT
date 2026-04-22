def forward_chaining(facts, rules, goal):
    known = facts[:]
    changed = True

    while changed:
        changed = False

        for conditions, result in rules:
            all_present = True

            for condition in conditions:
                if condition not in known:
                    all_present = False
                    break

            if all_present and result not in known:
                known.append(result)
                print(result)
                changed = True

                if result == goal:
                    return True, known

    return goal in known, known

def solve(name, facts, rules, goal):
    print(name)
    print("Facts:", ", ".join(facts))

    found, known = forward_chaining(facts, rules, goal)

    if found:
        print(goal, "is proved")
    else:
        print(goal, "is not proved")

    print("Final facts:", ", ".join(known))
    print()

rules_a = [
    (["P"], "Q"),
    (["L", "M"], "P"),
    (["A", "B"], "L")
]

facts_a = ["A", "B", "M"]

rules_b = [
    (["A"], "B"),
    (["B"], "C"),
    (["C"], "D"),
    (["D", "E"], "F")
]

facts_b = ["A", "E"]

solve("a", facts_a, rules_a, "Q")
solve("b", facts_b, rules_b, "F")