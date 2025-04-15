import numpy as np

states = ['Sunny', 'Cloudy', 'Rainy']
transition_matrix = np.array([
    [0.6, 0.3, 0.1],
    [0.4, 0.4, 0.2],
    [0.2, 0.3, 0.5]
])

def simulate_weather(start_state, days):
    current = start_state
    sequence = [current]
    for _ in range(days - 1):
        current_idx = states.index(current)
        current = np.random.choice(states, p=transition_matrix[current_idx])
        sequence.append(current)
    return sequence

print("Sample 10-day weather:")
seq = simulate_weather('Sunny', 10)
print(seq)

num_simulations = 10000
count = 0
for _ in range(num_simulations):
    seq = simulate_weather('Sunny', 10)
    if seq.count('Rainy') >= 3:
        count += 1
print(f"P(at least 3 rainy days) ≈ {count/num_simulations:.4f}")