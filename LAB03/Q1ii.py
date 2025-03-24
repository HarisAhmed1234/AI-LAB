class DLSAgent:
   
    def __init__(self, target, depth_limit):
        self.target = target
        self.depth_limit = depth_limit
        self.exploration_log = []

    def formulate_goal(self, node):
        return node == self.target

    def act(self, environment, start_state):
        return environment.dls_search(start_state, self.target, self.depth_limit, self.exploration_log)

class DLSEnvironment:
    def __init__(self, graph):
        self.graph = graph
        
    def dls_search(self, start, target, max_depth, log):
        def dls_recursive(node, path, depth):
            log.append(f"{node} (D:{depth})")
            current_path = path + [node]
            
            print(f"[DLS] Current: {node} \t Depth: {depth} \t Path: {' → '.join(current_path)}")
            
            if node == target:
                return True, current_path
                
            if depth >= max_depth:
                return False, None
                
            for child in self.graph.get(node, []):
                found, final_path = dls_recursive(child, current_path, depth + 1)
                if found:
                    return True, final_path
            return False, None

        found, path = dls_recursive(start, [], 0)
        if found:
            return (
                f"Target '{target}' found within depth {max_depth}!\n"
                f"Path: {' → '.join(path)}\n"
                f"Nodes explored: {len(log)}"
            )
        return (
            f"Target '{target}' not found within depth limit {max_depth}\n"
            f"Nodes explored: {len(log)}"
        )

if __name__ == "__main__":
    city_graph = {
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

    print("\n=== DLS Agent Demonstration ===")
    dls_agent = DLSAgent('I', 3)
    dls_env = DLSEnvironment(city_graph)
    result = dls_agent.act(dls_env, 'A')
    print("\n" + result)
    print(f"Exploration log: {dls_agent.exploration_log}")
