raw_graph = {
    "Kachchh": ["Surendranagar", "Patan", "Jamnagar"],
    "Banaskantha": ["Patan", "Mehsana", "Sabarkantha"],
    "Patan": ["Banaskantha", "Mehsana", "Surendranagar", "Kachchh"],
    "Mehsana": ["Banaskantha", "Patan", "Sabarkantha", "Gandhinagar", "Ahmedabad"],
    "Sabarkantha": ["Banaskantha", "Mehsana", "Gandhinagar", "Kheda", "Panchmahal"],
    "Gandhinagar": ["Mehsana", "Sabarkantha", "Ahmedabad", "Kheda"],
    "Kheda": ["Sabarkantha", "Gandhinagar", "Ahmedabad", "Anand", "Vadodara", "Panchmahal"],
    "Panchmahal": ["Sabarkantha", "Kheda", "Vadodara", "Dahod"],
    "Dahod": ["Panchmahal", "Vadodara"],
    "Ahmedabad": ["Mehsana", "Gandhinagar", "Kheda", "Anand", "Surendranagar"],
    "Anand": ["Ahmedabad", "Kheda", "Vadodara", "Bharuch"],
    "Vadodara": ["Kheda", "Anand", "Panchmahal", "Dahod", "Narmada", "Bharuch"],
    "Narmada": ["Vadodara", "Bharuch", "Surat", "Dangs"],
    "Bharuch": ["Vadodara", "Anand", "Narmada", "Surat"],
    "Surat": ["Bharuch", "Narmada", "Navsari", "Dangs"],
    "Navsari": ["Surat", "Valsad", "Dangs"],
    "Valsad": ["Navsari", "Dangs"],
    "Dangs": ["Narmada", "Surat", "Navsari", "Valsad"],
    "Surendranagar": ["Kachchh", "Patan", "Ahmedabad", "Rajkot", "Bhavnagar", "Jamnagar"],
    "Jamnagar": ["Kachchh", "Rajkot", "Porbandar", "Surendranagar"],
    "Rajkot": ["Surendranagar", "Jamnagar", "Porbandar", "Junagadh", "Amreli"],
    "Porbandar": ["Jamnagar", "Rajkot", "Junagadh"],
    "Junagadh": ["Porbandar", "Rajkot", "Amreli"],
    "Amreli": ["Rajkot", "Junagadh", "Bhavnagar"],
    "Bhavnagar": ["Surendranagar", "Amreli", "Anand", "Vadodara"]
}


def make_graph(data):
    graph = {}
    for district, neighbors in data.items():
        graph.setdefault(district, set()).update(neighbors)
        for neighbor in neighbors:
            graph.setdefault(neighbor, set()).add(district)
    return {district: sorted(neighbors) for district, neighbors in graph.items()}


def is_safe(district, color, assignment, graph):
    for neighbor in graph[district]:
        if assignment.get(neighbor) == color:
            return False
    return True


def backtrack(index, order, colors, assignment, graph):
    if index == len(order):
        return True

    district = order[index]

    for color in colors:
        if is_safe(district, color, assignment, graph):
            assignment[district] = color
            if backtrack(index + 1, order, colors, assignment, graph):
                return True
            assignment.pop(district)

    return False


def solve_map(graph):
    color_names = ["Red", "Green", "Blue", "Yellow"]
    order = sorted(graph, key=lambda district: len(graph[district]), reverse=True)

    for count in range(1, len(color_names) + 1):
        assignment = {}
        if backtrack(0, order, color_names[:count], assignment, graph):
            return count, assignment

    return None, None


def main():
    graph = make_graph(raw_graph)
    min_colors, assignment = solve_map(graph)

    if assignment is None:
        print("No solution found.")
        return

    print("Gujarat map coloring")
    print("Minimum colors needed:", min_colors)
    print()
    print("District colors:")

    for district in raw_graph:
        print(district + ": " + assignment[district])


if __name__ == "__main__":
    main()