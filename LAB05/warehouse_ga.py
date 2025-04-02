import random
"""
Lab 05: Warehouse Layout Optimization using Genetic Algorithm
Author: Haris Ahmed
"""

products = [
    {"frequency": 15, "volume": 2},
    {"frequency": 8, "volume": 1},
    {"frequency": 20, "volume": 3}
]

slots = [
    {"distance": 1, "capacity": 3},
    {"distance": 2, "capacity": 3},
    {"distance": 3, "capacity": 3}
]


POPULATION_SIZE = 50
MAX_GENERATIONS = 100
MUTATION_RATE = 0.1
EARLY_STOPPING = 20   

def calculate_fitness(chromosome):
    total_cost = 0
    slot_volumes = [0] * len(slots)
    
    for product_idx, slot_idx in enumerate(chromosome):
        product = products[product_idx]
        slot = slots[slot_idx - 1]
        total_cost += slot["distance"] * product["frequency"]
        slot_volumes[slot_idx - 1] += product["volume"]
    
    penalty = 0
    for slot_idx in range(len(slots)):
        if slot_volumes[slot_idx] > slots[slot_idx]["capacity"]:
            penalty += 1000
    
    return total_cost + penalty

def create_random_solution():
    return [random.randint(1, len(slots)) for _ in range(len(products))]

def select_parent(population, fitness_scores):
    candidates = random.sample(list(zip(population, fitness_scores)), 5)
    return min(candidates, key=lambda x: x[1])[0]

def crossover(parent1, parent2):
    point = random.randint(1, len(products) - 1)
    return parent1[:point] + parent2[point:]

def mutate(chromosome):
    idx1, idx2 = random.sample(range(len(chromosome)), 2)
    chromosome[idx1], chromosome[idx2] = chromosome[idx2], chromosome[idx1]
    return chromosome

def run_genetic_algorithm():
    population = [create_random_solution() for _ in range(POPULATION_SIZE)]
    best_fitness = float('inf')
    best_solution = None
    no_improvement_count = 0

    for generation in range(MAX_GENERATIONS):
        fitness_scores = [calculate_fitness(chromosome) for chromosome in population]
        
        valid_solutions = [(score, sol) for score, sol in zip(fitness_scores, population) if score < 1000]
        if valid_solutions:
            current_best_fitness, current_best_solution = min(valid_solutions, key=lambda x: x[0])
            
            if current_best_fitness < best_fitness:
                best_fitness = current_best_fitness
                best_solution = current_best_solution
                no_improvement_count = 0
            else:
                no_improvement_count += 1
        else:
            no_improvement_count += 1

        # Early stoping
        if no_improvement_count >= EARLY_STOPPING:
            print(f"\nEarly stopping at generation {generation + 1}")
            break

        # Selection and reproduction
        new_population = []
        for _ in range(POPULATION_SIZE):
            parent1 = select_parent(population, fitness_scores)
            parent2 = select_parent(population, fitness_scores)
            child = crossover(parent1, parent2)
            
            if random.random() < MUTATION_RATE:
                child = mutate(child)
            
            new_population.append(child)
        
        population = new_population

        # Print_progress
        if valid_solutions:
            print(f"Gen {generation + 1:2d} | Best: {current_best_fitness:3d} | Solution: {current_best_solution}")
        else:
            print(f"Gen {generation + 1:2d} | No valid solutions")

    # Final results
    print("\n=== Optimal Solution ===")
    print(f"Total Cost: {best_fitness}")
    for i, slot in enumerate(best_solution):
        print(f"Product {i+1} → Slot {slot} (Distance: {slots[slot-1]['distance']}, Freq: {products[i]['frequency']}, Vol: {products[i]['volume']})")

    # Calculate slot volumes
    slot_volumes = [0] * len(slots)
    for product_idx, slot_idx in enumerate(best_solution):
        slot_volumes[slot_idx - 1] += products[product_idx]["volume"]
    
    print("\nSlot Capacities:")
    for i, vol in enumerate(slot_volumes):
        print(f"Slot {i+1}: {vol}/{slots[i]['capacity']}")

run_genetic_algorithm()
