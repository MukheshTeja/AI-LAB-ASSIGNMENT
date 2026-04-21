letters = ["S", "E", "N", "D", "M", "O", "R", "Y"]


def choices(letter, assignment, used):
    if letter in assignment:
        return [assignment[letter]]
    if letter in ("S", "M"):
        return [digit for digit in range(1, 10) if digit not in used]
    return [digit for digit in range(10) if digit not in used]


def put(letter, digit, assignment, used):
    if letter in assignment:
        return assignment[letter] == digit, False
    if digit in used:
        return False, False
    if letter in ("S", "M") and digit == 0:
        return False, False
    assignment[letter] = digit
    used.add(digit)
    return True, True


def remove(letter, digit, added, assignment, used):
    if added:
        del assignment[letter]
        used.remove(digit)


def solve_thousands(carry, assignment, used):
    for s in choices("S", assignment, used):
        ok_s, added_s = put("S", s, assignment, used)
        if not ok_s:
            continue

        for m in choices("M", assignment, used):
            ok_m, added_m = put("M", m, assignment, used)
            if ok_m:
                total = assignment["S"] + assignment["M"] + carry
                if total % 10 == assignment["O"] and total // 10 == assignment["M"]:
                    return True
            remove("M", m, added_m, assignment, used)

        remove("S", s, added_s, assignment, used)

    return False


def solve_hundreds(carry, assignment, used):
    for o in choices("O", assignment, used):
        ok_o, added_o = put("O", o, assignment, used)
        if not ok_o:
            continue

        total = assignment["E"] + assignment["O"] + carry
        if total % 10 == assignment["N"]:
            next_carry = total // 10
            if solve_thousands(next_carry, assignment, used):
                return True

        remove("O", o, added_o, assignment, used)

    return False


def solve_tens(carry, assignment, used):
    for n in choices("N", assignment, used):
        ok_n, added_n = put("N", n, assignment, used)
        if not ok_n:
            continue

        for r in choices("R", assignment, used):
            ok_r, added_r = put("R", r, assignment, used)
            if ok_r:
                total = assignment["N"] + assignment["R"] + carry
                if total % 10 == assignment["E"]:
                    next_carry = total // 10
                    if solve_hundreds(next_carry, assignment, used):
                        return True
            remove("R", r, added_r, assignment, used)

        remove("N", n, added_n, assignment, used)

    return False


def solve_units(assignment, used):
    for d in choices("D", assignment, used):
        ok_d, added_d = put("D", d, assignment, used)
        if not ok_d:
            continue

        for e in choices("E", assignment, used):
            ok_e, added_e = put("E", e, assignment, used)
            if ok_e:
                total = assignment["D"] + assignment["E"]
                y = total % 10
                carry = total // 10
                ok_y, added_y = put("Y", y, assignment, used)
                if ok_y and solve_tens(carry, assignment, used):
                    return True
                remove("Y", y, added_y, assignment, used)
            remove("E", e, added_e, assignment, used)

        remove("D", d, added_d, assignment, used)

    return False


def word_value(word, assignment):
    number = ""
    for letter in word:
        number += str(assignment[letter])
    return int(number)


def main():
    assignment = {}
    used = set()

    if not solve_units(assignment, used):
        print("No solution found.")
        return

    send = word_value("SEND", assignment)
    more = word_value("MORE", assignment)
    money = word_value("MONEY", assignment)

    print("Solution found")
    print("SEND =", send)
    print("MORE =", more)
    print("MONEY =", money)
    print("Letter values:")

    for letter in letters:
        print(f"{letter} = {assignment[letter]}")


if __name__ == "__main__":
    main()