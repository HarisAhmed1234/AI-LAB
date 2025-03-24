import random

class LoadBalancerAgent:
    def __init__(self, servers):
        self.servers = servers
        self.actions = []

    def analyze_load(self):
        self.overloaded = [s for s, l in self.servers.items() if l == "Overloaded"]
        self.underloaded = [s for s, l in self.servers.items() if l == "Underloaded"]
        
    def balance_load(self):
        self.analyze_load()
        paired = min(len(self.overloaded), len(self.underloaded))
        
        if paired == 0:
            status = "⚠️  No balancing possible - "
            if not self.overloaded: status += "No overloaded servers"
            else: status += "No underloaded servers"
            self.actions.append(status)
            return

        print(f"\nBalancing {paired} server pair(s):")
        for i in range(paired):
            source = self.overloaded[i]
            target = self.underloaded[i]
            self.servers[source] = self.servers[target] = "Balanced"
            action = f"{source} → {target} | Both balanced"
            print(f"- {action}")
            self.actions.append(action)

    def display_status(self, phase):
        header = f"{phase} Server Status:"
        print(f"\n{header}\n" + "="*(len(header)-1))
        for server, load in self.servers.items():
            print(f"• {server}: {load.center(11)}")
        if self.actions:
            print("\nActions Taken:")
            for action in self.actions:
                print(f"  {action}")

def initialize_servers():
    return {f'Server {chr(65+i)}': random.choice(['Underloaded', 'Balanced', 'Overloaded']) 
            for i in range(5)}

def main():
    servers = initialize_servers()
    agent = LoadBalancerAgent(servers)
    
    agent.display_status("Initial")
    agent.balance_load()
    agent.display_status("Post-Balancing")

if __name__ == "__main__":
    main()
