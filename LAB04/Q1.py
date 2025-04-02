from queue import PriorityQueue

def heuristic(pos, goals):
    """Manhattan distance to the closest unvisited goal"""
    if not goals:
        return 0
    return min(abs(pos[0]-g[0]) + abs(pos[1]-g[1]) for g in goals)

def multi_goal_search(maze, start, goals):
    rows = len(maze)
    cols = len(maze[0]) if rows > 0 else 0
    
    frontier = PriorityQueue()
    frontier.put((0, frozenset(goals), start, [start]))
    
    visited = set()

    while not frontier.empty():
        _, goals_left, pos, path = frontier.get()
        
        if not goals_left:  # All goals visited
            return path
        
        if (pos, goals_left) in visited:
            continue
        visited.add((pos, goals_left))
        
        # Check if curent position is a goal
        new_goals = goals_left - {pos} if pos in goals_left else goals_left
        
        # Explore neighbors
        for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
            x, y = pos[0]+dx, pos[1]+dy
            if 0 <= x < rows and 0 <= y < cols and maze[x][y] == 0:
                new_pos = (x, y)
                new_path = path + [new_pos]
                h = heuristic(new_pos, new_goals)
                frontier.put((len(new_path) + h, new_goals, new_pos, new_path))
    
    return None  # No path found

maze = [
    [0, 0, 1, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0]
]

start = (0, 0)
goals = {(4, 4), (1, 3)}

path = multi_goal_search(maze, start, goals)
print("Path visiting all goals:", path if path else "No path found")
