def backward_chaining(goal, facts, rules, checked):
    if goal in facts:
        print(goal, "is a fact")
        return True

    if goal in checked:
        return False

    checked.append(goal)

    for conditions, result in rules:
        if result == goal:
            print("To prove", goal)
            all_true = True

            for condition in conditions:
                if not backward_chaining(condition, facts, rules, checked):
                    all_true = False
                    break

            if all_true:
                print(goal, "is proved")
                return True

    return False

def solve(name, facts, rules, goal):
    print(name)

    if backward_chaining(goal, facts, rules, []):
        print("Conclusion:", goal, "is true")
    else:
        print("Conclusion:", goal, "is false")

    print()

rules_a = [
    (["P"], "Q"),
    (["R"], "Q"),
    (["A"], "P"),
    (["B"], "R")
]

facts_a = ["A", "B"]

rules_b = [
    (["A"], "B"),
    (["B", "C"], "D"),
    (["E"], "C")
]

facts_b = ["A", "E"]

solve("a", facts_a, rules_a, "Q")
solve("b", facts_b, rules_b, "D")