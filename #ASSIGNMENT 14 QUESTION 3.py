def neg(value):
    if value[0] == "~":
        return value[1:]
    return "~" + value

def clause_text(clause):
    if len(clause) == 0:
        return "{}"
    return " v ".join(sorted(clause, key=lambda value: value.replace("~", "")))

def has_opposite(clause):
    for value in clause:
        if neg(value) in clause:
            return True
    return False

def resolve(first, second):
    answers = []

    for value in first:
        opposite = neg(value)

        if opposite in second:
            new_clause = set(first)
            new_clause.remove(value)

            for item in second:
                if item != opposite:
                    new_clause.add(item)

            if not has_opposite(new_clause):
                answers.append(frozenset(new_clause))

    return answers

def resolution(name, clauses, goal):
    print(name)

    all_clauses = []
    for clause in clauses:
        all_clauses.append(frozenset(clause))

    all_clauses.append(frozenset([neg(goal)]))

    print("Clauses")
    for clause in all_clauses:
        print(clause_text(clause))

    print("Resolving")

    while True:
        added = []

        for i in range(len(all_clauses)):
            for j in range(i + 1, len(all_clauses)):
                new_clauses = resolve(all_clauses[i], all_clauses[j])

                for new_clause in new_clauses:
                    if len(new_clause) == 0:
                        print("Empty clause")
                        print("Conclusion:", goal, "is proved")
                        print()
                        return

                    if new_clause not in all_clauses and new_clause not in added:
                        added.append(new_clause)
                        print(clause_text(new_clause))

        if len(added) == 0:
            print("No contradiction")
            print("Conclusion:", goal, "is not proved")
            print()
            return

        for clause in added:
            all_clauses.append(clause)

clauses_a = [
    ["P", "Q"],
    ["~P", "R"],
    ["~Q", "S"],
    ["~R", "S"]
]

clauses_b = [
    ["~P", "Q"],
    ["~Q", "R"],
    ["~S", "~R"],
    ["P"]
]

resolution("a", clauses_a, "S")
resolution("b", clauses_b, "S")