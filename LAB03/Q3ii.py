from collections import deque

class BidirectionalSearch:
    def __init__(self, graph):
        self.graph = graph
        self.forward_visited = {}
        self.backward_visited = {}

    def search(self, start, target):
        print(f"\nBidirectional Search: {start} <-> {target}")
        if start == target:
            return [start]

        forward_queue = deque([start])
        backward_queue = deque([target])
        self.forward_visited = {start: None}
        self.backward_visited = {target: None}

        while forward_queue and backward_queue:
            if self._expand_layer(forward_queue, self.forward_visited, self.backward_visited):
                path = self._reconstruct_path()
                print(f"Collision Detected! Full Path: {' -> '.join(map(str, path))}")
                return path

            if self._expand_layer(backward_queue, self.backward_visited, self.forward_visited):
                path = self._reconstruct_path()
                print(f"Collision Detected! Full Path: {' -> '.join(map(str, path))}")
                return path

        print("No connecting path exists")
        return None

    def _expand_layer(self, queue, visited, other_visited):
        level_size = len(queue)
        for _ in range(level_size):
            current = queue.popleft()
            print(f"Exploring: {current}")

            for neighbor in self.graph.get(current, []):
                if neighbor not in visited:
                    visited[neighbor] = current
                    queue.append(neighbor)
                    if neighbor in other_visited:
                        return True  
        return False

    def _reconstruct_path(self):
        intersect = set(self.forward_visited) & set(self.backward_visited)
        meeting_point = intersect.pop()

        forward_path = []
        node = meeting_point
        while node is not None:
            forward_path.append(node)
            node = self.forward_visited.get(node)
        forward_path.reverse()

        backward_path = []
        node = meeting_point
        while node is not None:
            backward_path.append(node)
            node = self.backward_visited.get(node)

        return forward_path + backward_path[1:]

graph = {
    0: [1, 2],
    1: [0, 3, 4],
    2: [0, 5],
    3: [1],
    4: [1, 6],
    5: [2, 7],
    6: [4],
    7: [5]
}

print("=== Bidirectional Search (Graph) ===")
bs = BidirectionalSearch(graph)
path = bs.search(0, 7)
print(f"\nShortest Path: {' -> '.join(map(str, path))}" if path else "")
