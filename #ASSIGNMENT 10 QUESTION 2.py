def and_or_search(problem):
    return or_search(problem, problem['initial'], [])

def or_search(problem, state, path):
    if problem['is_goal'](state):
        return []
    if state in path:
        return 'failure'
    for action in problem['actions'](state):
        plan = and_search(problem, problem['results'](state, action), [state] + path)
        if plan != 'failure':
            return [action] + plan
    return 'failure'

def and_search(problem, states, path):
    plans = []
    for s in states:
        plan = or_search(problem, s, path)
        if plan == 'failure':
            return 'failure'
        plans.append((s, plan))
    return plans

def is_goal(state):
    return state['A'] == 'clean' and state['B'] == 'clean'

def actions(state):
    if state['loc'] == 'A':
        return ['clean', 'right']
    else:
        return ['clean', 'left']

def results(state, action):
    loc = state['loc']
    A = state['A']
    B = state['B']

    if action == 'clean':
        if loc == 'A':
            if A == 'dirty':
                return [
                    {'loc': 'A', 'A': 'clean', 'B': B},
                    {'loc': 'A', 'A': 'clean', 'B': 'clean'}
                ]
            else:
                return [
                    {'loc': 'A', 'A': 'clean', 'B': B},
                    {'loc': 'A', 'A': 'dirty', 'B': B}
                ]
        else:
            if B == 'dirty':
                return [
                    {'loc': 'B', 'A': A, 'B': 'clean'},
                    {'loc': 'B', 'A': 'clean', 'B': 'clean'}
                ]
            else:
                return [
                    {'loc': 'B', 'A': A, 'B': 'clean'},
                    {'loc': 'B', 'A': A, 'B': 'dirty'}
                ]
    elif action == 'right':
        return [{'loc': 'B', 'A': A, 'B': B}]
    elif action == 'left':
        return [{'loc': 'A', 'A': A, 'B': B}]

def format_state(s):
    return f"[Loc={s['loc']}, A={s['A']}, B={s['B']}]"

def print_plan(plan, indent=0):
    prefix = "  " * indent
    i = 0
    while i < len(plan):
        item = plan[i]
        if isinstance(item, str):
            print(f"{prefix}Action: {item}")
            branches = []
            while i + 1 < len(plan) and isinstance(plan[i + 1], tuple):
                branches.append(plan[i + 1])
                i += 1
            if branches:
                for state, subplan in branches:
                    print(f"{prefix}  IF outcome {format_state(state)}:")
                    if subplan:
                        print_plan(subplan, indent + 2)
                    else:
                        print(f"{prefix}    -> Goal reached")
        i += 1


initial_state = {'loc': 'A', 'A': 'dirty', 'B': 'dirty'}

problem = {
    'initial': initial_state,
    'is_goal': is_goal,
    'actions': actions,
    'results': results
}

print(f"Initial State: {format_state(initial_state)}")
print(f"Goal: Both tiles A and B should be clean")
print()

plan = and_or_search(problem)

if plan == 'failure':
    print("No conditional plan found.")
else:
    print("Conditional Plan:")
    print("-" * 30)
    print_plan(plan)