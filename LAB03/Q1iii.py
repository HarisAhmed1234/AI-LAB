import heapq

class UCSAgent:
    def __init__(self, target):
        self.target = target
        self.cost_log = {}

    def formulate_goal(self, node):
        return node == self.target

    def act(self, environment, start_state):
        return environment.ucs_search(start_state, self.target, self.cost_log)

class UCSEnvironment:
    def __init__(self, graph):
        self.graph = graph
        
    def ucs_search(self, start, target, cost_log):
        heap = [(0, start, [])] 
        visited = {}
        
        while heap:
            cost, node, path = heapq.heappop(heap)
            
            if node in visited and visited[node] <= cost:
                continue
                
            visited[node] = cost
            cost_log[node] = cost
            current_path = path + [node]
            
            print(f"[UCS] Current: {node} \t Cost: {cost} \t Path: {' → '.join(current_path)}")
            
            if node == target:
                return (
                    f"Optimal path to '{target}' found!\n"
                    f"Total cost: {cost}\n"
                    f"Path: {' → '.join(current_path)}\n"
                    f"Nodes cost: {cost_log}"
                )
            
            for neighbor, edge_cost in self.graph.get(node, {}).items():
                new_cost = cost + edge_cost
                new_path = path + [node]
                heapq.heappush(heap, (new_cost, neighbor, new_path))
        
        return f"Target '{target}' not reachable from '{start}'"

if __name__ == "__main__":
    weighted_graph = {
        'A': {'B': 2, 'C': 1},
        'B': {'D': 4, 'E': 3},
        'C': {'F': 1, 'G': 5},
        'D': {'H': 2},
        'E': {},
        'F': {'I': 6},
        'G': {},
        'H': {},
        'I': {}
    }

    print("\n=== UCS Agent Demonstration ===")
    ucs_agent = UCSAgent('I')
    ucs_env = UCSEnvironment(weighted_graph)
    result = ucs_agent.act(ucs_env, 'A')
    print("\n" + result)
