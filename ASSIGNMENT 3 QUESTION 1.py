import random

class VacuumEnvironment:
    def __init__(self):
        self.location_states = {
            'A': 1,
            'B': 1,
            'C': 1
        }
        self.agent_location = 'A'
        self.performance_score = 0

    def get_percept(self):
        status = 'Dirty' if self.location_states[self.agent_location] == 1 else 'Clean'
        return (self.agent_location, status)

    def execute_action(self, action):
        cost = 0

        if action == 'Suck':
            if self.location_states[self.agent_location] == 1:
                self.location_states[self.agent_location] = 0
                cost = 10
                print(f"  Action Effect: Room {self.agent_location} is now CLEAN.")
            else:
                cost = -1
                print("  Action Effect: Wasted energy (Room was already clean).")

        elif action == 'Right':
            if self.agent_location == 'A':
                self.agent_location = 'B'
                cost = -1
            elif self.agent_location == 'B':
                self.agent_location = 'C'
                cost = -1
            else:
                cost = -1
            print(f"  Action Effect: Moved Right to {self.agent_location}.")

        elif action == 'Left':
            if self.agent_location == 'C':
                self.agent_location = 'B'
                cost = -1
            elif self.agent_location == 'B':
                self.agent_location = 'A'
                cost = -1
            else:
                cost = -1
            print(f"  Action Effect: Moved Left to {self.agent_location}.")

        elif action == 'NoOp':
            cost = 0

        self.performance_score += cost
        return cost

class SimpleReflexAgent:
    def __init__(self):
        self.rules = {
            ('A', 'Dirty'): 'Suck',
            ('A', 'Clean'): 'Right',
            ('B', 'Dirty'): 'Suck',
            ('B', 'Clean'): 'Left',
            ('C', 'Dirty'): 'Suck',
            ('C', 'Clean'): 'Left'
        }

    def select_action(self, percept):
        location, status = percept
        if (location, status) in self.rules:
            return self.rules[(location, status)]
        else:
            return 'NoOp'

def run_simulation(steps=10):
    print("--- Starting Vacuum World Simulation (3 Rooms) ---")

    env = VacuumEnvironment()
    agent = SimpleReflexAgent()

    print("\n[Agent's Internal Rule Table]")
    print(f"{'Percept (Loc, Status)':<25} | {'Action':<10}")
    print("-" * 40)
    for percept, action in agent.rules.items():
        print(f"{str(percept):<25} | {action:<10}")
    print("-" * 40 + "\n")

    for step in range(1, steps + 1):
        print(f"Step {step}:")
        percept = env.get_percept()
        print(f"  Percept:  Agent sees {percept}")
        action = agent.select_action(percept)
        print(f"  Action:   Agent decides to '{action}'")
        step_cost = env.execute_action(action)
        print(f"  Score Change: {step_cost} | Total Performance: {env.performance_score}")
        print("-" * 30)

    print("\n--- Simulation Complete ---")
    print(f"Final Performance Score: {env.performance_score}")

run_simulation(steps=8)