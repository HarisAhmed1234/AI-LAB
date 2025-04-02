import heapq

def greedy_delivery_search(start, deliveries):
    remaining = deliveries.copy()
    route = [start]
    current_pos = start

    while remaining:
        remaining.sort(key=lambda x: (x[1][1], abs(current_pos[0]-x[0][0]) + abs(current_pos[1]-x[0][1])))
        next_pos, _ = remaining.pop(0)
        route.append(next_pos)
        current_pos = next_pos

    return route

start = (0, 0)
delivery_points = [
    ((4, 4), (8, 12)),
    ((1, 3), (5, 9)),
    ((3, 2), (3, 7)),
    ((2, 4), (4, 10))
]

route = greedy_delivery_search(start, delivery_points)
print(route)
