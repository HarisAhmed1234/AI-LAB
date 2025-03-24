class DFSAgent:
    
    def __init__(self, target):
        self.target = target
        self.exploration_path = []

    def formulate_goal(self, node):
        return node == self.target

    def act(self, environment, start_state):
        return environment.dfs_search(start_state, self.target, self.exploration_path)

class DFSEnvironment:
    def __init__(self, graph):
        self.graph = graph
        self.visited = set()
        
    def get_percept(self, node):
        return node
        
    def dfs_search(self, start, target, path):
        stack = [(start, [start])]  
        
        while stack:
            current_node, current_path = stack.pop()
            self.visited.add(current_node)
            path.append(current_node)
            
            print(f"[DFS] Current: {current_node} \t Path: {' → '.join(current_path)}")
            
            if current_node == target:
                return (
                    f"Target '{target}' found!\n"
                    f"Full path: {' → '.join(current_path)}\n"
                    f"Nodes explored: {len(self.visited)}"
                )
            
            for child in reversed(self.graph.get(current_node, [])):
                if child not in self.visited:
                    stack.append((child, current_path + [child]))
        
        return f"Target '{target}' not reachable from '{start}'"

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

    print("=== DFS Agent Demonstration ===")
    dfs_agent = DFSAgent('I')
    dfs_env = DFSEnvironment(city_graph)
    result = dfs_agent.act(dfs_env, 'A')
    print("\n" + result)
    print(f"Exploration order: {dfs_agent.exploration_path}")
