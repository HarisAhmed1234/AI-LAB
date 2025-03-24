from itertools import permutations
import math

def print_tsp_result(method_name, path, distance):
    print(f"\n{method_name}:")
    print(f"️ Optimal Route: {' → '.join(map(str, path))}")
    print(f" Total Distance: {distance}")

def brute_force_tsp(graph, start):
    if start not in graph:
        raise ValueError(f"Start node '{start}' not in graph!")
    
    nodes = list(graph.keys())
    nodes.remove(start)
    min_distance = math.inf
    optimal_path = None

    for sequence in permutations(nodes):
        current_path = [start]
        total_distance = 0
        current = start
        
        for city in sequence:
            total_distance += graph[current][city]
            current = city
            current_path.append(city)
        
        total_distance += graph[current][start]
        current_path.append(start)

        if total_distance < min_distance:
            min_distance = total_distance
            optimal_path = current_path

    return optimal_path, min_distance

def nearest_neighbor_tsp(graph, start):
    if start not in graph:
        raise ValueError(f"Start node '{start}' not in graph!")
    
    remaining = set(graph.keys())
    remaining.remove(start)
    path = [start]
    current = start
    total_distance = 0

    while remaining:
        closest = min(remaining, key=lambda city: graph[current][city])
        total_distance += graph[current][closest]
        path.append(closest)
        remaining.remove(closest)
        current = closest

    total_distance += graph[current][start]
    path.append(start)
    return path, total_distance

distance_graph = {
    1: {2: 10, 3: 15, 4: 20},
    2: {1: 10, 3: 35, 4: 25},
    3: {1: 15, 2: 35, 4: 30},
    4: {1: 20, 2: 25, 3: 30}
}

start_point = 1

bf_path, bf_dist = brute_force_tsp(distance_graph, start_point)
print_tsp_result("Brute Force TSP", bf_path, bf_dist)

nn_path, nn_dist = nearest_neighbor_tsp(distance_graph, start_point)
print_tsp_result("Nearest Neighbor TSP", nn_path, nn_dist)
