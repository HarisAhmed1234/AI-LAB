class IDDFSSolver:
    def __init__(self, graph):
        self.graph = graph
        self.search_log = []

    def iddfs(self, start, target, max_depth):
        print(f"\nIDDFS from {start} to {target} (Max Depth: {max_depth})")
        for depth in range(max_depth + 1):
            result, path = self._depth_limited_search(start, target, depth, [start])
            self.search_log.append(f"Depth {depth}: {path}")
            print(f"Trying depth {depth}: {' -> '.join(map(str, path))}")
            if result:
                print(f"Target found at depth {depth}!")
                return path
        print("Target not found within depth limit")
        return None

    def _depth_limited_search(self, node, target, depth, path):
        if node == target:
            return True, path
        if depth <= 0:
            return False, path
            
        for neighbor in self.graph.get(node, []):
            new_path = path + [neighbor]
            found, final_path = self._depth_limited_search(neighbor, target, depth-1, new_path)
            if found:
                return True, final_path
        return False, path

tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H'],
    'E': [],
    'F': ['I'],
    'G': [],
    'H': [],
    'I': []
}

print("=== Iterative Deepening DFS (Tree) ===")
solver = IDDFSSolver(tree)
path = solver.iddfs('A', 'I', 4)
print(f"\nFinal Path: {' -> '.join(path)}" if path else "No path found")
print(f"Search Log: {solver.search_log}")
