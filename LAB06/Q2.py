import random, math

def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def total_distance(route):
    return sum(distance(route[i], route[i + 1]) for i in range(len(route) - 1))

def nearest_neighbor_start(points):
    unvisited = points[:]
    start = unvisited.pop(0)  
    route = [start]

    while unvisited:
        next_city = min(unvisited, key=lambda city: distance(route[-1], city))
        route.append(next_city)
        unvisited.remove(next_city)
    
    return route

def get_neighbors(route):
    neighbors = []
    for _ in range(len(route) // 2):  
        i, j = sorted(random.sample(range(len(route)), 2))
        neighbor = route[:i] + route[i:j+1][::-1] + route[j+1:]
        neighbors.append(neighbor)
    return neighbors

def hill_climbing(points, max_iter=500):
    current = nearest_neighbor_start(points)  
    current_distance = total_distance(current)

    for _ in range(max_iter):
        neighbors = get_neighbors(current)
        next_route = min(neighbors, key=total_distance, default=current)
        next_distance = total_distance(next_route)

        if next_distance >= current_distance:  
            break  

        current, current_distance = next_route, next_distance

    return current, current_distance

locations = [(random.randint(0, 100), random.randint(0, 100)) for _ in range(5)]
optimized_route, min_distance = hill_climbing(locations)

print("Optimized route:", optimized_route)
print("Total distance:", round(min_distance,2))
