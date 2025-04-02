import random
import math

def distance(c1, c2):
    return math.sqrt((c1[0] - c2[0])**2 + (c1[1] - c2[1])**2)

def total_distance(route):
    return sum(distance(route[i], route[i + 1]) for i in range(len(route) - 1))

def nearest_neighbor_route(cities):
    unvisited = cities[:]
    route = [unvisited.pop(0)]
    while unvisited:
        next_city = min(unvisited, key=lambda city: distance(route[-1], city))
        route.append(next_city)
        unvisited.remove(next_city)
    return route

def create_initial_population(cities, pop_size):
    return [create_random_route(cities) if i % 2 == 0 else nearest_neighbor_route(cities) 
            for i in range(pop_size)]

def create_random_route(cities):
    return random.sample(cities, len(cities))

def ordered_crossover(p1, p2):
    size = len(p1)
    start, end = sorted(random.sample(range(size), 2))
    child = [None] * size
    child[start:end] = p1[start:end]
    ptr = end
    for city in p2:
        if city not in child:
            if ptr >= size:
                ptr = 0
            child[ptr] = city
            ptr += 1
    return child

def mutate(route):
    i, j = random.sample(range(len(route)), 2)
    route[i], route[j] = route[j], route[i]
    return route

def tournament_selection(population, k=5):
    return min(random.sample(population, k), key=total_distance)

def genetic_algorithm(cities, pop_size=20, gens=100, mut_rate=0.1, elite_size=1):
    pop = create_initial_population(cities, pop_size)
    
    for _ in range(gens):
        pop = sorted(pop, key=total_distance)
        new_pop = pop[:elite_size]  

        while len(new_pop) < pop_size:
            p1, p2 = tournament_selection(pop), tournament_selection(pop)
            child = ordered_crossover(p1, p2)
            if random.random() < mut_rate:
                child = mutate(child)
            new_pop.append(child)

        pop = new_pop

    return min(pop, key=total_distance)

cities = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(10)]
best_route = genetic_algorithm(cities)
print("Best route:", best_route)
print("Total distance:", round(total_distance(best_route),2))
