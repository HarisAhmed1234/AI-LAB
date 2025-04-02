import heapq
import random
import time

class Node:
    def __init__(self, position, g=0, h=0):
        self.position = position
        self.g = g  # Cost from start
        self.h = h  # Heuristic
        self.f = g + h  # Total cost
        self.parent = None

    def __lt__(self, other):
        return self.f < other.f  # For priority queue

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])  # Manhattan distance

def get_neighbors(pos, maze):
    rows, cols = len(maze), len(maze[0])
    moves = [(1,0), (-1,0), (0,1), (0,-1)]
    neighbors = []
    for dx, dy in moves:
        x, y = pos[0] + dx, pos[1] + dy
        if 0 <= x < rows and 0 <= y < cols and maze[x][y] == 0:
            neighbors.append((x, y))
    return neighbors

def a_star_dynamic(maze, start, goal):
    rows, cols = len(maze), len(maze[0])
    open_set = []
    heapq.heappush(open_set, Node(start, 0, heuristic(start, goal)))
    edge_costs = {}  # Default cost=1 unless changed
    visited = {}

    # Background thread to change costs randomly
    def update_costs():
        while True:
            x, y = random.randint(0, rows-1), random.randint(0, cols-1)
            edge_costs[(x, y)] = random.randint(1, 5)  # New cost: 1-5
            time.sleep(1)  # Change every second

    import threading
    threading.Thread(target=update_costs, daemon=True).start()

    while open_set:
        current = heapq.heappop(open_set)

        if current.position == goal:
            path = []
            while current:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        if current.position in visited and visited[current.position] <= current.g:
            continue
        visited[current.position] = current.g

        for neighbor in get_neighbors(current.position, maze):
            cost = edge_costs.get(neighbor, 1)  # Default cost=1
            new_g = current.g + cost
            if neighbor not in visited or new_g < visited[neighbor]:
                new_node = Node(neighbor, new_g, heuristic(neighbor, goal))
                new_node.parent = current
                heapq.heappush(open_set, new_node)

    return None  # No path found

#(0=free, 1=blocked)
maze = [
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0]
]

start = (0, 0)
goal = (4, 4)
path = a_star_dynamic(maze, start, goal)
print("Path:", path if path else "No path")
