from queue import PriorityQueue

class Node:
    def __init__(self, position, parent=None, goals_visited=frozenset()):
        self.position = position
        self.parent = parent
        self.goals_visited = goals_visited
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def heuristic(current_pos, remaining_goals):
    if not remaining_goals:
        return 0
    return min(abs(current_pos[0] - g[0]) + abs(current_pos[1] - g[1]) for g in remaining_goals)

def best_first_search_multi_goal(maze, start, goal_points):
    rows, cols = len(maze), len(maze[0])
    start_node = Node(start)
    frontier = PriorityQueue()
    frontier.put((0, start_node))
    visited = set()

    while not frontier.empty():
        _, current_node = frontier.get()
        current_pos = current_node.position
        current_goals = current_node.goals_visited

        if current_goals == frozenset(goal_points):
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        if (current_pos, current_goals) in visited:
            continue
        visited.add((current_pos, current_goals))

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_pos = (current_pos[0] + dx, current_pos[1] + dy)
            if 0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and maze[new_pos[0]][new_pos[1]] == 0:
                new_goals = current_goals | {new_pos} if new_pos in goal_points else current_goals
                new_node = Node(new_pos, current_node, new_goals)
                new_node.g = current_node.g + 1
                new_node.h = heuristic(new_pos, goal_points - new_goals)
                new_node.f = new_node.g + new_node.h
                frontier.put((new_node.f, new_node))

    return None

maze = [
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0]
]

start = (0, 0)
goal_points = {(4, 4), (1, 3)}

path = best_first_search_multi_goal(maze, start, goal_points)
print("Shortest Path Covering All Goals:", path if path else "No path found")
