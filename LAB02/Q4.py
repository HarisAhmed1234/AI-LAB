import random

class SecurityAgent:
    def __init__(self):
        self.resources = {'free_patches': 3, 'premium': False}
    
    def scan(self, system):
        order = sorted(system.items(), key=lambda x: 3 if x[1]=='High Risk' else 2 if x[1]=='Low Risk' else 1, reverse=True)
        for comp, status in order:
            if status == 'Low Risk' and self.resources['free_patches'] > 0:
                system[comp] = 'Safe'
                self.resources['free_patches'] -= 1
                print(f"Patched {comp} (Low Risk)")
            elif status == 'High Risk' and self.resources['premium']:
                system[comp] = 'Safe'
                print(f"Patched {comp} (High Risk)")
            elif status != 'Safe':
                print(f"Couldn't patch {comp} ({status})")

class BackupManager:
    def __init__(self):
        self.tasks = {f"Task{i+1}": random.choice(['Done', 'Failed']) for i in range(5)}
        self.attempts = {}
    
    def retry(self):
        for task, status in self.tasks.items():
            if status == 'Failed':
                self.attempts[task] = self.attempts.get(task, 0) + 1
                self.tasks[task] = 'Done' if random.random() < 0.7 else 'Failed'
                print(f"Retried {task} (Attempt {self.attempts[task]})")

def main():
    print("\nSecurity System:")
    system = {chr(65+i): random.choice(['Safe', 'Low Risk', 'High Risk']) for i in range(9)}
    print("Initial:", system)
    agent = SecurityAgent()
    agent.scan(system)
    print("Final:", system)
    
    print("\nBackup System:")
    backups = BackupManager()
    print("Initial:", backups.tasks)
    backups.retry()
    print("Final:", backups.tasks)

if __name__ == "__main__":
    random.seed(42)
    main()
