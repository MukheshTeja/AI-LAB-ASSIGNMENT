scenarios = [
    [0, 0, 0],  # Case 0: Everything is normal
    [1, 0, 0],  # Case 1: Train detected (Lower Gate)
    [1, 1, 0],  # Case 2: Train detected BUT track is blocked (Safety First!)
    [0, 0, 1]   # Case 3: Manual Emergency Lever pulled
]

class RailwayAgent:
    def decide(self, percept):
        train, obstacle, emergency = percept

        if emergency == 1 or obstacle == 1:
            return ["RAISE", "RED", "ON"]
        
        if train == 1:
            return ["LOWER", "GREEN", "ON"]
        
        return ["RAISE", "GREEN", "OFF"]

agent = RailwayAgent()

print("--- INDIAN RAILWAYS LEVEL CROSSING SIMULATION ---")
print(f"{'Percept (T,O,E)':<18} | {'Gate':<8} | {'Signal':<8} | {'Hooter'}")
print("-" * 60)

for p in scenarios:
    act = agent.decide(p)
    print(f"{str(p):<18} | {act[0]:<8} | {act[1]:<8} | {act[2]}")